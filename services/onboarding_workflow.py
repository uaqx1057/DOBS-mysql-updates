"""Data-driven onboarding stage sequencing.

Replaces hardcoded per-driver-type if/else with rows in
`dobs_onboarding_stage_template` (see models.py) so a new driver type or a
changed sequence is an admin-dashboard edit, not a code deploy.

Phase 0: shadow mode only. `shadow_check()` is called right after the
existing hardcoded stage-transition code runs, to log any place the
config-driven engine would have produced a different result - nothing here
changes actual behavior yet. Phase 2 wires `advance()` into the real
transition call sites and removes the shadow_check() calls.
"""
from flask import current_app

from models import OnboardingStageTemplate


def _stage_rows_for(driver_type_id):
    return (
        OnboardingStageTemplate.query
        .filter_by(driver_type_id=driver_type_id)
        .order_by(OnboardingStageTemplate.sequence_order)
        .all()
    )


def _condition_skips(driver, row) -> bool:
    """A row is skipped when driver's `skip_condition_field` attribute
    equals `skip_condition_value` (case-insensitive, bools compared as
    "true"/"false")."""
    if not row.skip_condition_field or row.skip_condition_value is None:
        return False
    actual = getattr(driver, row.skip_condition_field, None)
    actual_str = str(bool(actual)).lower() if isinstance(actual, bool) else str(actual).lower()
    return actual_str == str(row.skip_condition_value).lower()


def next_stage(driver, current_stage: str = None):
    """Return the next non-skipped configured stage after `current_stage`
    (defaults to driver.onboarding_stage) for the driver's type.

    Returns None if there's no configured sequence for this driver's type,
    `current_stage` isn't in that sequence, or it's already the last stage.
    """
    current_stage = driver.onboarding_stage if current_stage is None else current_stage
    rows = _stage_rows_for(driver.driver_type_id)
    if not rows:
        return None

    stage_names = [row.stage_name for row in rows]
    try:
        idx = stage_names.index(current_stage)
    except ValueError:
        return None

    for row in rows[idx + 1:]:
        if _condition_skips(driver, row):
            continue
        return row.stage_name

    return None


def advance(driver, from_stage: str):
    """Authoritative stage advance. Not yet called from any route in Phase 0
    - Phase 2 swaps each hardcoded `driver.onboarding_stage = "X"` call site
    over to this function."""
    target = next_stage(driver, current_stage=from_stage)
    if target:
        driver.onboarding_stage = target
    return target


def shadow_check(driver, from_stage: str, actual_next_stage: str, context: str = ""):
    """Log-only comparison between what the legacy hardcoded code just did
    (`actual_next_stage`) and what the config-driven engine would produce
    for the same transition. Never raises, never changes driver state."""
    try:
        computed = next_stage(driver, current_stage=from_stage)
        if computed is None:
            current_app.logger.info(
                "onboarding_workflow shadow: no stage template configured for driver_type_id=%s "
                "(driver=%s, from=%s, context=%s)",
                driver.driver_type_id, driver.id, from_stage, context,
            )
        elif computed != actual_next_stage:
            current_app.logger.warning(
                "onboarding_workflow shadow MISMATCH: driver=%s type=%s from=%s legacy_next=%s "
                "config_next=%s (context=%s)",
                driver.id, driver.driver_type_id, from_stage, actual_next_stage, computed, context,
            )
    except Exception:
        current_app.logger.exception("onboarding_workflow shadow_check failed")
