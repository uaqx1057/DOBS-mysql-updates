# Digital (OTP-based) Signing for Driver Contracts & Promissory Notes

> Status: **planning only** — not yet implemented. Saved here for reference so the plan survives across sessions; refine further before building.

## Context

Today, HR generates a Company Contract PDF and a Promissory Note PDF (`services/contracts.py`), prints them, the driver wet-signs on paper, and HR scans/photographs the signed copy back into the system (`blueprints/hr/routes.py::approve_driver`, Step 2 of the HR modal). This works but is slow, easy to lose track of, and produces no real evidence beyond "someone uploaded a photo."

The user wants a digital signing option alongside this, and specifically asked how to make it legally defensible under Saudi Labor Law. Research into Saudi's Electronic Transactions Law (Royal Decree M/18, 2007) shows electronic signatures are valid for commercial/HR documents when they meet Article 14: uniquely linked to the signer, under the signer's sole control, and tamper-evidently bound to the document. Since May 2022, the *formal* employment contract for company-sponsored ("Sponsor" type) drivers must additionally be authenticated through the government Qiwa platform — that requirement is untouched by this feature; it already exists in this codebase (`Driver.qiwa_contract_created`, `qiwa_contract_status`, `DriverTypeSettings.requires_qiwa_contract`) and this plan does not read or write those fields. A fully "Qualified Electronic Signature" (CITC-licensed CA, NAFATH identity binding — e.g. emdha, Signit) would be the strongest possible tier, but the user explicitly chose the cheaper in-house route instead: an SMS-OTP-based "simple electronic signature," built around Twilio, with a strong audit trail (IP, timestamp, document hashes, OTP possession-of-phone proof). **This lands at "simple e-signature," not "qualified" — get KSA legal counsel to confirm this tier is adequate for these specific documents before relying on it in a dispute.** The architecture keeps the "prove signer identity" step narrow so a licensed provider could be swapped in later without reworking the rest.

Scope (per user): Company Contract (both freelancer and sponsor-type) and Promissory Note now, designed generically so more document kinds can be added later. The existing physical print → wet-sign → scan → upload flow stays exactly as-is, permanently, as a fallback alongside the new digital option.

## Key existing pieces this reuses

- `SharedGeneratedDriverContract` (`models.py`) already has `signed_status`/`signed_at`/`signed_copy_path` columns from a prior migration — currently vestigial (`signed_status="pending"` is set once at creation in `services/contracts.py::_store_generated_contract_record` and never updated). This becomes the live "current signing state" summary.
- **Bug/gap to fix first:** `generate_promissory_note` (`services/contracts.py`) never calls `_store_generated_contract_record`, so promissory notes have no `SharedGeneratedDriverContract` row today — only contracts do. Fix this so both document kinds share one polymorphic "signable document" anchor.
- `Driver.absher_number` is already the driver's personal Saudi mobile number in practice (collected as "Absher Number (Mobile)" at public registration, `templates/register.html`, pattern `05XXXXXXXX`, `required`; already read as `driver.absher_number or "N/A"` for "driver mobile" in `ops_manager/routes.py`). No new column needed — add a `Driver.personal_mobile_number` read-only property aliasing it for clarity in new code.
- OTP pattern to model after (not reuse as-is): `blueprints/auth/routes.py::_issue_otp`/`_otp_valid` — `secrets.randbelow(1_000_000)` 6-digit code, `timedelta` expiry, `secrets.compare_digest` verification. That one stores the code in the Flask session (fine for a login flow); e-signature needs a **DB-persisted** record instead, since it must survive as durable evidence.
- No driver login/portal exists (`Driver.password` is set but nothing ever authenticates against it). So the driver-facing signing page must be a **token-gated "magic link"**, not a login-based one — same anonymous-but-CSRF-protected pattern already used in `blueprints/public/routes.py::register`.
- PDF stamping reuses the existing ReportLab/pypdf stack in `services/contracts.py` (`register_unicode_font`, `safe_pdf_text`, `safe_rtl_pdf_text`, and the overlay/merge technique already used by `_apply_driver_contract_letterhead`).
- File storage reuses `services/file_storage.py::save_to_shared_storage` (same helper every other document uses) and the `_document_filename` naming convention already established for contracts/promissory notes.
- Rate limiting reuses `extensions.limiter`, same as `auth/routes.py`.
- IP capture: this codebase has no proxy-aware IP helper anywhere — it uses `request.remote_addr` directly everywhere (`auth/routes.py`, `app.py`). Follow that same convention; don't add proxy/X-Forwarded-For handling that doesn't otherwise exist.

## Implementation

### 1. Data model — new `driver_document_signatures` table

Add `DriverDocumentSignature` to `models.py` (after `SharedGeneratedDriverContract`):
- Anchors: `shared_contract_id` (FK, required), `driver_document_id` (FK, nullable secondary anchor), `driver_id` (FK), `document_kind` (string, copied at creation time).
- Token: `token_hash` (unique, sha256 of the raw token — never store the raw token itself, same philosophy as password hashing), `token_expires_at`, `token_used_at`.
- Lifecycle: `status` (`sent` → `otp_requested` → `otp_verified` → `completed`; terminal failures: `expired`, `cancelled`, `failed`).
- OTP: `recipient_mobile` (snapshotted at send time, not re-read live), `otp_hash` (sha256/HMAC, never plaintext), `otp_sent_at`, `otp_expires_at`, `otp_attempts` (lock out after e.g. 5 wrong tries), `otp_verified_at`.
- Audit: `requested_by` (FK to `User`), `requested_at`, `ip_address`, `user_agent` (captured at OTP-verify time, since that's the moment of signature).
- Tamper-evidence: `pre_sign_sha256` (hash of the unsigned PDF, computed once at send time), `post_sign_sha256` (hash of the final stamped PDF), `signed_pdf_path`, `signed_driver_document_id` (FK — the signed PDF becomes its own new append-only `DriverDocument` row, never overwriting the original, matching how every other document in this app is stored).

Why a separate table instead of just extending `SharedGeneratedDriverContract`: a document can be resent/retokenized multiple times (expired link, too many wrong OTPs), and token/OTP hashes + IP/UA + before/after hashes don't belong mixed into document metadata. `SharedGeneratedDriverContract`'s three existing columns stay as the cheap current-state summary (kept in sync so existing HR UI reads don't need to change shape), while the new table is the system of record for the signing lifecycle.

New migration `migrations/versions/20260718_driver_document_signature.py` (`down_revision = '20260717_contract_template_arabic_content'`), following the exact style of `20260715_driver_contract_system.py` (inspector-guarded, symmetric `downgrade()`). Also add a `document_kind` column to `shared_generated_driver_contracts` if not already effectively available, so signing code doesn't need to join to `dobs_contract_template` to know what kind of document it's signing.

### 2. Fix promissory note tracking (prerequisite)

In `services/contracts.py::generate_promissory_note`, after `_save_contract_document(...)`, also call `_store_generated_contract_record(driver, template, None, doc, uploaded_by_id)` — exactly like `generate_driver_contracts` already does. This gives every promissory note a `SharedGeneratedDriverContract` row, unifying both document kinds under one anchor the new signature table can point at.

Then update `_generated_promissory_link()` in `blueprints/hr/routes.py` to query `SharedGeneratedDriverContract` instead of raw `DriverDocument` — this is what lets promissory notes expose `signed_status`/`signed_at` the same way contracts will.

### 3. SMS service — `services/sms.py` (new)

Provider-agnostic interface so Twilio can be swapped later:
- `SmsProvider` base class with `.send(to_e164, body) -> message_id`.
- `TwilioSmsProvider` — wraps `twilio.rest.Client(...).messages.create(...)`.
- `DryRunSmsProvider` — logs to `current_app.logger` instead of sending, for testing without a real Twilio account.
- `get_sms_provider()` factory, keyed off a new `SMS_PROVIDER` config value (`"dryrun"` default, `"twilio"` in production) — same shape as how mail transport is already configured.
- `normalize_ksa_mobile(raw)` — `"05XXXXXXXX"` → `"+9665XXXXXXXX"`, `None` if it doesn't match.
- `send_otp_sms(...)`, `send_signing_link_sms(...)`.

New config in `config.py`, following the existing `_env_or_file` pattern used for `MAIL_*`: `SMS_PROVIDER`, `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_FROM_NUMBER`, `SIGNATURE_TOKEN_EXPIRY_HOURS` (default 72), `SIGNATURE_OTP_EXPIRY_MIN` (default 10), `SIGNATURE_OTP_MAX_ATTEMPTS` (default 5), `APP_PUBLIC_BASE_URL` (needed to build absolute `/sign/<token>` links for SMS). Add `twilio` to `requirements.txt`.

No background task runner exists in this codebase (confirmed) — SMS sends happen synchronously in the request, same as `flask_mail` does today. That's fine for this volume; not something to solve now.

### 4. Signing flow — new `blueprints/sign/` (login-less, token-gated)

New blueprint (`sign_bp`, url_prefix `/sign`), registered in `app.py` alongside the others. Routes:
- `GET /sign/<token>` — look up by `sha256(token)` (never by raw token), check expiry/used/status, render a minimal page with the unsigned PDF and an "send me a code" action. `@limiter.limit("20 per hour")`.
- `POST /sign/<token>/request-otp` — generate a 6-digit code (same generation pattern as `auth/routes.py::_issue_otp`), store only its hash, send via `services/sms.py`. Rate-limited both per-IP (`5 per hour`) and per-token (to stop OTP-bombing a driver's phone regardless of source IP).
- `POST /sign/<token>/verify` — compare via `secrets.compare_digest` on the hash, enforce `otp_attempts` lockout, and on success: mark verified, capture `request.remote_addr` + `request.headers.get("User-Agent")`, then synchronously stamp + hash + save the signed PDF (section 5) and mark `status="completed"`. Rate-limited `10 per minute` per IP + per-token.

New service `services/esignature.py` (thin routes, real logic here — matches the existing `hr_service.py`/`contracts.py` split):
- `create_signature_request(shared_contract, requested_by_id)` — generates token, computes `pre_sign_sha256` from the existing unsigned PDF bytes, sends the link SMS, returns the new `DriverDocumentSignature` row.
- `finalize_signature(record, ip, user_agent)` — stamps the signature block onto the PDF, computes `post_sign_sha256`, saves via `save_to_shared_storage`, creates the new signed `DriverDocument` row, and updates `SharedGeneratedDriverContract.signed_status/signed_at/signed_copy_path`.

Validate `driver.personal_mobile_number` (format `^05\d{8}$`) at the moment HR triggers "send for signature," not at driver-creation time — fail fast with a clear message if missing/invalid, rather than making the field newly required everywhere (would break drivers who only ever use the physical-signing path).

### 5. PDF signature stamping

New `stamp_signature_block(pdf_bytes, *, driver, signature)` in `services/contracts.py`, reusing the existing overlay/merge technique (`_apply_driver_contract_letterhead`'s pattern: ReportLab canvas → pypdf merge onto the last page). Shows: signer name + Iqama number, phone **last 4 digits only** (not the full number — avoid printing PII on a document that gets handled physically), timestamp of `otp_verified_at`, IP address, and the document's reference number. A verification QR code is a nice-to-have, not required for v1.

### 6. HR workflow integration

In `blueprints/hr/routes.py`:
- New route `POST /dashboard/hr/generated_contracts/<int:shared_contract_id>/send_for_signature` (same permission guard as `generate_contract_pack`), calling `services.esignature.create_signature_request`.
- `_generated_contract_links()` and the fixed `_generated_promissory_link()` (section 2) both expose `signed_status`/`signed_at` per document.
- `templates/dashboard_hr.html`: add a "Send for Digital Signature" button + status pill next to each item in the existing "Generated PDFs ready for print" list (`renderGeneratedContracts()`), sitting **alongside** the existing Step 2 physical-upload form — both paths stay live simultaneously.
- **Resolved:** a completed digital signature (`signed_status == "signed"`) satisfies `approve_driver`'s "signed copy required" gate on its own — HR shouldn't have to print+scan a document the driver already digitally signed. Concretely, in the `required_files` check (`approve_driver`, ~line 332-343): for each field (`company_contract_file`, `promissory_note_file`), skip the "an uploaded file is required" check if the corresponding `SharedGeneratedDriverContract.signed_status == "signed"` for that driver's document of that kind; otherwise require the upload exactly as today. This keeps the physical path fully mandatory-by-default (today's behavior, zero regression) and only relaxes it when the digital alternative has *actually* completed — never both required, never neither.

## Data protection (Saudi PDPL)

Saudi's Personal Data Protection Law (in force since Sept 2024, enforced by SDAIA) requires purpose limitation, data minimization, and freely-given informed consent for processing personal data — and treats national ID-type identifiers as needing extra care. This flow touches several categories: mobile number, IP address, device/user-agent string, Iqama number (already stored elsewhere in this app, not newly introduced), and the signing event itself.

- **Consent notice on `/sign/<token>`:** the page must state in plain Arabic/English what's being collected (mobile number for OTP delivery, IP/timestamp/device as part of the signature record) and that clicking "sign" constitutes agreement to be legally bound - not just a UX nicety, this is the "informed decision" PDPL consent actually depends on, and doubles as the strongest single piece of ETL Article 14 evidence ("sole control / intent to sign").
- **Data minimization already designed in:** the stamped PDF shows only the phone's last 4 digits, not the full number (section 5) - keep this.
- **Retention:** no specific KSA statutory retention period for e-signature/contract audit trails was found in research - use the company's existing document retention policy for these records (treat the same as any other HR/contract document, likely retained for the life of the driver relationship plus some years after, per standard employment-record practice), and get legal counsel to confirm a specific number for the audit-trail table specifically (it does not need to match the retention period of the PDF file itself - the two can differ). Don't build automatic deletion in v1; that's a policy decision to make deliberately, not a default to pick unilaterally.
- **Access control:** the new `driver_document_signatures` table contains IP addresses and phone numbers - restrict read access the same way other sensitive driver fields already are (SuperAdmin/HR only, via the existing `require_permission`/role pattern - no new access-control mechanism needed, just apply the existing one consistently).

## Suggested rollout phasing

1. **Build + dry-run.** Ship sections 1-6 with `SMS_PROVIDER=dryrun`. No real SMS sent yet; verify the full flow internally (see Verification below).
2. **Small pilot.** Switch one test/volunteer driver to `SMS_PROVIDER=twilio` (Twilio trial account, that number pre-verified in the Twilio console). Run several real signings end-to-end, including at least one deliberately-wrong-OTP and one expired-link case, to see real-world SMS delivery latency to a KSA number before trusting it broadly.
3. **Get the legal sign-off** (see Context: KSA counsel review of the "simple e-signature" tier for Company Contract + Promissory Note specifically) before this becomes the default path HR reaches for.
4. **General rollout,** physical upload remaining available the whole time as a fallback per the user's decision - never removed.

## Verification

1. Set `SMS_PROVIDER=dryrun` (default) and run `flask db upgrade` for the new migration.
2. End-to-end manual test: generate a contract pack for a test driver with a valid `05XXXXXXXX`-format `absher_number`, click "Send for Digital Signature," pull the token link and OTP straight out of the dry-run log, open `/sign/<token>` in an incognito window (proving no login is required), request + submit the OTP, and confirm: the `driver_document_signatures` row reaches `status="completed"`, a new signed `DriverDocument` appears, `SharedGeneratedDriverContract.signed_status/signed_at/signed_copy_path` are populated, and the stamped PDF shows the correct name/Iqama/last-4-digits/timestamp/IP.
3. Negative-path checks: expired token, reused token, wrong OTP past the attempt limit, missing/malformed mobile number (expect the fail-fast HR error), rate limits triggering correctly.
4. Add unit tests (pytest is already in `requirements.txt`) for `normalize_ksa_mobile`, token hash round-trip, OTP hash/compare, and hash correctness on known byte strings.
5. Once ready to test real delivery: switch to `SMS_PROVIDER=twilio` with a Twilio trial account (verify the tester's real KSA number in the Twilio console first — trial accounts only send to verified numbers) and repeat the manual end-to-end flow over real SMS.