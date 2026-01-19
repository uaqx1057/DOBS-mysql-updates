--
-- PostgreSQL database dump
--

-- Dumped from database version 16.10 (Ubuntu 16.10-0ubuntu0.24.04.1)
-- Dumped by pg_dump version 16.10 (Ubuntu 16.10-0ubuntu0.24.04.1)

-- Started on 2025-10-19 12:26:23 +03

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 6 (class 2615 OID 2200)
-- Name: public; Type: SCHEMA; Schema: -; Owner: dobsykjq_admin
--

-- *not* creating schema, since initdb creates it


ALTER SCHEMA public OWNER TO dobsykjq_admin;

--
-- TOC entry 2 (class 3079 OID 16463)
-- Name: pgcrypto; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS pgcrypto WITH SCHEMA public;


--
-- TOC entry 3490 (class 0 OID 0)
-- Dependencies: 2
-- Name: EXTENSION pgcrypto; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION pgcrypto IS 'cryptographic functions';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 216 (class 1259 OID 16390)
-- Name: driver; Type: TABLE; Schema: public; Owner: dobsykjq_admin
--

CREATE TABLE public.driver (
    id integer NOT NULL,
    full_name character varying(100),
    iqama_number character varying(20),
    iqama_expiry_date date,
    saudi_driving_license boolean,
    nationality character varying(100),
    mobile_number character varying(15),
    previous_sponsor_number character varying(50),
    iqama_card_upload character varying(200),
    platform character varying(100),
    city character varying(100),
    car_details character varying(200),
    assignment_date date,
    onboarding_stage character varying(50) DEFAULT 'Ops Manager'::character varying,
    qiwa_contract_created boolean DEFAULT false,
    company_contract_created boolean DEFAULT false,
    qiwa_transfer_approved boolean DEFAULT false,
    sponsorship_transfer_done boolean DEFAULT false,
    qiwa_contract_status character varying(20) DEFAULT 'Pending'::character varying,
    sponsorship_transfer_status character varying(20) DEFAULT 'Pending'::character varying,
    ops_manager_approved_at timestamp without time zone,
    hr_approved_at timestamp without time zone,
    ops_supervisor_approved_at timestamp without time zone,
    fleet_manager_approved_at timestamp without time zone,
    finance_approved_at timestamp without time zone,
    ops_manager_approved boolean DEFAULT false,
    hr_approved_by integer,
    platform_id character varying(50),
    mobile_issued boolean DEFAULT false,
    tamm_authorized boolean DEFAULT false,
    transfer_fee_paid boolean DEFAULT false,
    transfer_fee_amount double precision,
    transfer_fee_paid_at timestamp without time zone,
    transfer_fee_receipt character varying(200),
    issued_mobile_number character varying(20),
    issued_device_id character varying(100),
    tamm_authorization_ss character varying(200),
    sponsorship_transfer_proof character varying(200)
);


ALTER TABLE public.driver OWNER TO dobsykjq_admin;

--
-- TOC entry 217 (class 1259 OID 16406)
-- Name: driver_id_seq; Type: SEQUENCE; Schema: public; Owner: dobsykjq_admin
--

CREATE SEQUENCE public.driver_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.driver_id_seq OWNER TO dobsykjq_admin;

--
-- TOC entry 3491 (class 0 OID 0)
-- Dependencies: 217
-- Name: driver_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dobsykjq_admin
--

ALTER SEQUENCE public.driver_id_seq OWNED BY public.driver.id;


--
-- TOC entry 218 (class 1259 OID 16407)
-- Name: driver_platform; Type: TABLE; Schema: public; Owner: dobsykjq_admin
--

CREATE TABLE public.driver_platform (
    id integer NOT NULL,
    driver_id integer NOT NULL,
    platform_name character varying(100) NOT NULL,
    platform_user_id character varying(100) NOT NULL,
    assigned_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.driver_platform OWNER TO dobsykjq_admin;

--
-- TOC entry 219 (class 1259 OID 16411)
-- Name: driver_platform_id_seq; Type: SEQUENCE; Schema: public; Owner: dobsykjq_admin
--

CREATE SEQUENCE public.driver_platform_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.driver_platform_id_seq OWNER TO dobsykjq_admin;

--
-- TOC entry 3492 (class 0 OID 0)
-- Dependencies: 219
-- Name: driver_platform_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dobsykjq_admin
--

ALTER SEQUENCE public.driver_platform_id_seq OWNED BY public.driver_platform.id;


--
-- TOC entry 220 (class 1259 OID 16412)
-- Name: offboarding; Type: TABLE; Schema: public; Owner: dobsykjq_admin
--

CREATE TABLE public.offboarding (
    id integer NOT NULL,
    driver_id integer NOT NULL,
    requested_by_id integer NOT NULL,
    requested_at timestamp without time zone,
    status character varying(30),
    ops_supervisor_cleared boolean,
    ops_supervisor_cleared_at timestamp without time zone,
    ops_supervisor_note text,
    fleet_cleared boolean,
    fleet_cleared_at timestamp without time zone,
    fleet_damage_report text,
    fleet_damage_cost double precision,
    finance_cleared boolean,
    finance_cleared_at timestamp without time zone,
    finance_invoice_file character varying(200),
    finance_adjustments double precision,
    finance_note text,
    hr_cleared boolean,
    hr_cleared_at timestamp without time zone,
    hr_note text,
    tamm_revoked boolean,
    tamm_revoked_at timestamp without time zone,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    company_contract_cancelled boolean DEFAULT false,
    qiwa_contract_cancelled boolean DEFAULT false,
    salary_paid boolean DEFAULT false
);


ALTER TABLE public.offboarding OWNER TO dobsykjq_admin;

--
-- TOC entry 221 (class 1259 OID 16420)
-- Name: offboarding_id_seq; Type: SEQUENCE; Schema: public; Owner: dobsykjq_admin
--

CREATE SEQUENCE public.offboarding_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.offboarding_id_seq OWNER TO dobsykjq_admin;

--
-- TOC entry 3493 (class 0 OID 0)
-- Dependencies: 221
-- Name: offboarding_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dobsykjq_admin
--

ALTER SEQUENCE public.offboarding_id_seq OWNED BY public.offboarding.id;


--
-- TOC entry 222 (class 1259 OID 16421)
-- Name: user; Type: TABLE; Schema: public; Owner: dobsykjq_admin
--

CREATE TABLE public."user" (
    id integer NOT NULL,
    username character varying(50) NOT NULL,
    password text NOT NULL,
    role character varying(50) NOT NULL,
    name character varying(100),
    designation character varying(100),
    branch_city character varying(100),
    email character varying(150)
);


ALTER TABLE public."user" OWNER TO dobsykjq_admin;

--
-- TOC entry 223 (class 1259 OID 16426)
-- Name: user_id_seq; Type: SEQUENCE; Schema: public; Owner: dobsykjq_admin
--

CREATE SEQUENCE public.user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.user_id_seq OWNER TO dobsykjq_admin;

--
-- TOC entry 3494 (class 0 OID 0)
-- Dependencies: 223
-- Name: user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dobsykjq_admin
--

ALTER SEQUENCE public.user_id_seq OWNED BY public."user".id;


--
-- TOC entry 3299 (class 2604 OID 16427)
-- Name: driver id; Type: DEFAULT; Schema: public; Owner: dobsykjq_admin
--

ALTER TABLE ONLY public.driver ALTER COLUMN id SET DEFAULT nextval('public.driver_id_seq'::regclass);


--
-- TOC entry 3311 (class 2604 OID 16428)
-- Name: driver_platform id; Type: DEFAULT; Schema: public; Owner: dobsykjq_admin
--

ALTER TABLE ONLY public.driver_platform ALTER COLUMN id SET DEFAULT nextval('public.driver_platform_id_seq'::regclass);


--
-- TOC entry 3313 (class 2604 OID 16429)
-- Name: offboarding id; Type: DEFAULT; Schema: public; Owner: dobsykjq_admin
--

ALTER TABLE ONLY public.offboarding ALTER COLUMN id SET DEFAULT nextval('public.offboarding_id_seq'::regclass);


--
-- TOC entry 3317 (class 2604 OID 16430)
-- Name: user id; Type: DEFAULT; Schema: public; Owner: dobsykjq_admin
--

ALTER TABLE ONLY public."user" ALTER COLUMN id SET DEFAULT nextval('public.user_id_seq'::regclass);


--
-- TOC entry 3477 (class 0 OID 16390)
-- Dependencies: 216
-- Data for Name: driver; Type: TABLE DATA; Schema: public; Owner: dobsykjq_admin
--

COPY public.driver (id, full_name, iqama_number, iqama_expiry_date, saudi_driving_license, nationality, mobile_number, previous_sponsor_number, iqama_card_upload, platform, city, car_details, assignment_date, onboarding_stage, qiwa_contract_created, company_contract_created, qiwa_transfer_approved, sponsorship_transfer_done, qiwa_contract_status, sponsorship_transfer_status, ops_manager_approved_at, hr_approved_at, ops_supervisor_approved_at, fleet_manager_approved_at, finance_approved_at, ops_manager_approved, hr_approved_by, platform_id, mobile_issued, tamm_authorized, transfer_fee_paid, transfer_fee_amount, transfer_fee_paid_at, transfer_fee_receipt, issued_mobile_number, issued_device_id, tamm_authorization_ss, sponsorship_transfer_proof) FROM stdin;
5	ayaz khan	1245789638	2025-10-07	t	pakistani	0565465460	1	ayaz_khan_1245789638.jpeg	Jahez	Dammam	zxc 125 - adwdwsd	2025-10-05	Completed	t	t	f	f	Approved	Completed	2025-10-05 12:09:46.524305	2025-10-05 12:10:10.010151	2025-10-05 12:10:47.801914	2025-10-05 12:12:00.463915	2025-10-05 12:12:41.211514	t	\N	1478	t	t	t	4000	2025-10-05 12:12:41.211506	ayaz_khan_1245789638_transfer_payment_proof.jpeg	0569696989	nokia	ayaz_khan_1245789638_zxc_125_TAMM_Authorisation.png	ayaz_khan_1245789638_transfer_proof.png
2	Usama Akhtar	1234567899	2026-02-24	t	Pakistani	0568465058	0	usama_akhtar_1234567899.jpeg	HungerStation	Khobar	adc 458 - swift blue	2025-10-02	Completed	t	t	f	f	Approved	Completed	2025-10-02 12:25:10.767802	2025-10-02 12:26:08.755607	2025-10-02 12:26:38.960381	2025-10-02 12:27:33.233976	2025-10-02 12:28:14.91034	t	\N	4567	t	t	t	2000	2025-10-02 12:28:14.910332	Usama_Akhtar_1234567899_transfer_payment_proof.jpeg	0500000000	Iphone 17	Usama_Akhtar_1234567899_adc_458_TAMM_Authorisation.png	Usama_Akhtar_1234567899_transfer_proof.png
7	moannad	2583697841	2026-01-14	t	pakistani	0565432171	1	moannad_2583697841.jpeg	\N	Dammam	ags 4588 - white corola	2025-10-15	Completed	t	t	f	f	Approved	Completed	2025-10-14 12:43:41.406261	2025-10-15 08:58:41.602257	2025-10-15 09:10:09.280291	2025-10-15 09:22:11.461424	2025-10-15 09:36:31.403879	t	\N	\N	t	t	t	2000	2025-10-15 09:36:31.40387	moannad_2583697841_transfer_payment_proof.jpeg	\N	\N	moannad_2583697841_ags_4588_TAMM_Authorisation.png	moannad_2583697841_transfer_proof.png
6	ali ali	789654123	2025-10-28	t	pakistani	0565465460	1	ali_ali_789654123.jpeg	Unknown	Dammam	hgxdubka - adwdwsd	2025-10-06	Completed	t	t	f	f	Approved	Completed	2025-10-05 12:47:09.85941	2025-10-06 12:57:26.578826	2025-10-06 13:01:17.962878	2025-10-06 13:30:12.625921	2025-10-07 08:32:13.729953	t	\N	\N	f	t	t	2000	2025-10-07 08:32:13.729943	ali_ali_789654123_transfer_payment_proof.jpeg	\N	\N	ali_ali_789654123_hgxdubka_TAMM_Authorisation.png	ali_ali_789654123_transfer_proof.png
3	meesam ali	1447788552	2026-02-18	t	Pakistani	0568465058	0	meesam_ali_1447788552.png	HungerStation	Khobar	hgxd ubka - adwd wsd	2025-10-04	Completed	t	t	f	f	Approved	Completed	2025-10-04 09:45:20.004144	2025-10-04 09:45:34.161271	2025-10-04 09:46:19.028062	2025-10-04 09:46:50.438401	2025-10-04 09:48:11.882348	t	\N	77895	t	t	t	2000	2025-10-04 09:48:11.882334	meesam_ali_1447788552_transfer_payment_proof.png	0545454544	nikia	meesam_ali_1447788552_hgxd_ubka_TAMM_Authorisation.png	meesam_ali_1447788552_transfer_proof.png
4	abuzar	7896541236	2026-02-20	t	sudan	058529637	0	abuzar_7896541236.jpeg	ToYou	Dammam	hg xdubka - ad wdwsd	2025-10-05	Completed	t	t	f	f	Approved	Completed	2025-10-05 11:50:47.551892	2025-10-05 11:52:16.548935	2025-10-05 11:57:44.629205	2025-10-05 11:58:28.904249	2025-10-05 11:59:09.445367	t	\N	123	t	t	t	2000	2025-10-05 11:59:09.445356	abuzar_7896541236_transfer_payment_proof.jpeg	0545454545	nokia	abuzar_7896541236_hg_xdubka_TAMM_Authorisation.png	abuzar_7896541236_transfer_proof.png
8	usama aamir qureshi	8528528527	2026-02-12	t	pakistani	0568466048	1	usama_aamir_qureshi_8528528527.jpeg	\N	Dammam	\N	\N	HR	f	f	f	f	Pending	Pending	2025-10-14 12:43:50.350761	\N	\N	\N	\N	t	\N	\N	f	f	f	\N	\N	\N	\N	\N	\N	\N
1	Usman Asif	2585305937	2025-12-10	t	Pakistani	0568465058	0	usman_asif_2585305937.jpeg	ToYou	Khobar	abc 123 - Elantra White	2025-09-30	Completed	t	t	f	f	Approved	Completed	2025-09-30 09:45:34.911956	2025-09-30 09:48:36.860774	2025-09-30 10:10:00.253743	2025-09-30 10:38:51.067753	2025-09-30 11:22:41.035067	t	\N	112258	t	t	t	2000	2025-09-30 11:22:41.035057	Usman_Asif_2585305937_transfer_payment_proof.jpeg	0500000000	Samsung S23 ultra	Usman_Asif_2585305937_abc_123_TAMM_Authorisation.png	Usman_Asif_2585305937_transfer_proof.png
10	murtadha	1254789632	2026-01-15	t	uganda	0568465058	0	murtadha_1254789632.jpeg	\N	Dammam	hgx   du bka - a dwd wsd	2025-10-14	Completed	t	t	f	f	Approved	Completed	2025-10-14 12:18:39.406559	2025-10-14 12:19:19.559697	2025-10-14 13:52:11.647647	2025-10-14 14:22:44.800838	2025-10-14 14:25:33.981141	t	\N	\N	t	t	t	2000	2025-10-14 14:25:33.981132	murtadha_1254789632_transfer_payment_proof.jpeg	0500000000	dwadwda	murtadha_1254789632_hgx_du_bka_TAMM_Authorisation.png	murtadha_1254789632_transfer_proof.png
9	alpha beta	5528528527	2026-02-12	t	pakistani	056565656	1	alpha_beta_5528528527.jpeg	\N	Dammam	\N	\N	HR	f	f	f	f	Pending	Pending	2025-10-15 08:49:07.582041	\N	\N	\N	\N	t	\N	\N	f	f	f	\N	\N	\N	\N	\N	\N	\N
\.


--
-- TOC entry 3479 (class 0 OID 16407)
-- Dependencies: 218
-- Data for Name: driver_platform; Type: TABLE DATA; Schema: public; Owner: dobsykjq_admin
--

COPY public.driver_platform (id, driver_id, platform_name, platform_user_id, assigned_at) FROM stdin;
1	5	Jahez	1478	2025-10-06 12:04:02.297883
2	2	HungerStation	4567	2025-10-06 12:04:02.297883
3	3	HungerStation	77895	2025-10-06 12:04:02.297883
4	4	ToYou	123	2025-10-06 12:04:02.297883
5	1	ToYou	112258	2025-10-06 12:04:02.297883
6	6	Keeta	1212457	2025-10-06 13:01:17.967287
7	6	Jahez	11225	2025-10-06 13:01:17.967291
8	10	جاهز	1212445	2025-10-14 13:52:11.6539
9	7	هنجر ستيشن	dadw	2025-10-15 09:10:09.285136
\.


--
-- TOC entry 3481 (class 0 OID 16412)
-- Dependencies: 220
-- Data for Name: offboarding; Type: TABLE DATA; Schema: public; Owner: dobsykjq_admin
--

COPY public.offboarding (id, driver_id, requested_by_id, requested_at, status, ops_supervisor_cleared, ops_supervisor_cleared_at, ops_supervisor_note, fleet_cleared, fleet_cleared_at, fleet_damage_report, fleet_damage_cost, finance_cleared, finance_cleared_at, finance_invoice_file, finance_adjustments, finance_note, hr_cleared, hr_cleared_at, hr_note, tamm_revoked, tamm_revoked_at, created_at, updated_at, company_contract_cancelled, qiwa_contract_cancelled, salary_paid) FROM stdin;
2	2	12	2025-10-02 12:29:08.983329	Completed	t	2025-10-02 12:29:46.521206	done	t	2025-10-02 14:03:14.891975	major accident 	5000	t	2025-10-02 13:55:50.592108	offboarding_Usama_Akhtar_1234567899_invoice.jpeg	500	5500-5000	t	2025-10-02 14:02:47.910054	\N	t	2025-10-02 14:03:14.891984	2025-10-02 12:29:08.984686	2025-10-02 14:03:14.892627	t	t	t
4	4	12	2025-10-05 12:00:37.981466	Completed	t	2025-10-05 12:01:40.492174		t	2025-10-05 12:06:10.944931	bumpers	2000	t	2025-10-05 12:03:31.900007	\N	1000	2000 damages	t	2025-10-05 12:05:24.527254	\N	t	2025-10-05 12:06:10.944942	2025-10-05 12:00:37.982992	2025-10-05 12:06:10.945672	t	t	t
5	6	12	2025-10-07 12:15:58.588741	Completed	t	2025-10-07 13:45:24.414054	all clear\n	t	2025-10-07 14:31:55.768473	none	0	t	2025-10-07 14:25:48.306574	\N	1500	net sallery	t	2025-10-07 14:31:23.453777	\N	t	2025-10-07 14:31:55.768484	2025-10-07 12:15:58.591543	2025-10-07 14:31:55.769439	t	t	t
1	1	12	2025-09-30 11:25:30.751933	Completed	t	2025-09-30 11:32:34.516434		t	2025-10-02 08:44:01.53001	front bumper	200	t	2025-09-30 13:25:48.491418	offboarding_Usman_Asif_2585305937_invoice.png	1500	none	t	2025-10-01 14:33:33.053599	\N	t	2025-10-02 08:44:01.53002	2025-09-30 11:25:30.754056	2025-10-02 08:44:01.532513	t	t	t
6	5	12	2025-10-14 12:54:20.434744	Completed	t	2025-10-14 13:52:25.783193		t	2025-10-14 14:55:41.8813	0	-0.01	t	2025-10-14 14:25:52.037863	\N	3000	None	t	2025-10-14 14:54:13.904846	\N	t	2025-10-14 14:55:41.881317	2025-10-14 12:54:20.437116	2025-10-14 14:55:41.882278	t	t	t
3	3	12	2025-10-04 09:49:14.021411	Completed	t	2025-10-06 13:10:24.162929		t	2025-10-14 14:55:48.557489		0	t	2025-10-07 14:30:36.179077	\N	2000	net sallery	t	2025-10-14 14:54:34.112604	\N	t	2025-10-14 14:55:48.557497	2025-10-04 09:49:14.024117	2025-10-14 14:55:48.557838	t	t	t
7	10	12	2025-10-15 08:49:19.62618	Completed	t	2025-10-15 08:56:04.72759		t	2025-10-15 12:10:19.588258	none	0	t	2025-10-15 09:36:07.802772	\N	5000	None	t	2025-10-15 12:01:17.032539	\N	t	2025-10-15 12:10:19.588268	2025-10-15 08:49:19.62899	2025-10-15 12:10:19.588992	t	t	t
\.


--
-- TOC entry 3483 (class 0 OID 16421)
-- Dependencies: 222
-- Data for Name: user; Type: TABLE DATA; Schema: public; Owner: dobsykjq_admin
--

COPY public."user" (id, username, password, role, name, designation, branch_city, email) FROM stdin;
10	kashif	$2a$06$eSxuy4p.DMRE.guvhOpCT.8Xi2UyQIYAedU0dwKSpwIY2ag/dfM6W	FleetManager	kashif	fleat manager	Dammam	kashif@gmail.com
11	asif	$2a$06$wOVks9c9j2ODfsk6UleTieBys9t9VACxT.nLaJbkf34PIQq4ECSB2	FinanceManager	asif	asif	Dammam	asif@gmail.com
7	usama	pbkdf2:sha256:260000$GG9mqCnKBNmlhGkQ$1693ae1fcdef1daac935cb0a60026a7deb8b5ebed4039c5725355543bdb5131f	HR	usama	IT manager	Dammam	usama@gmail.com
12	usman	pbkdf2:sha256:260000$yS3J1fi2gsssSZYA$15c16cc5d066c421e13cb1d8f930e8ee20651e7acd220876e28e93e0366dbae2	OpsManager	usman	dev	Dammam	usman@gmail.com
9	ahmed	pbkdf2:sha256:260000$QqGuFEEmEminBavH$c259730afd154fe1632f75238dffe09fca24ebce5b1da9b17a77c1ed08c3cf27	OpsSupervisor	ahmed	dummy	Dammam	ahmed@gmail.com
1	superadmin	pbkdf2:sha256:260000$yYKP6YbqwW5xduZo$32780dacf73b1330c5cbd335240e7b8ab6324e9e452c73e24eab3db6f0a10cba	SuperAdmin	\N	\N	\N	dobsykjq_admin@example.com
\.


--
-- TOC entry 3495 (class 0 OID 0)
-- Dependencies: 217
-- Name: driver_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dobsykjq_admin
--

SELECT pg_catalog.setval('public.driver_id_seq', 10, true);


--
-- TOC entry 3496 (class 0 OID 0)
-- Dependencies: 219
-- Name: driver_platform_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dobsykjq_admin
--

SELECT pg_catalog.setval('public.driver_platform_id_seq', 9, true);


--
-- TOC entry 3497 (class 0 OID 0)
-- Dependencies: 221
-- Name: offboarding_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dobsykjq_admin
--

SELECT pg_catalog.setval('public.offboarding_id_seq', 7, true);


--
-- TOC entry 3498 (class 0 OID 0)
-- Dependencies: 223
-- Name: user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dobsykjq_admin
--

SELECT pg_catalog.setval('public.user_id_seq', 14, true);


--
-- TOC entry 3319 (class 2606 OID 16432)
-- Name: driver driver_iqama_number_key; Type: CONSTRAINT; Schema: public; Owner: dobsykjq_admin
--

ALTER TABLE ONLY public.driver
    ADD CONSTRAINT driver_iqama_number_key UNIQUE (iqama_number);


--
-- TOC entry 3321 (class 2606 OID 16434)
-- Name: driver driver_pkey; Type: CONSTRAINT; Schema: public; Owner: dobsykjq_admin
--

ALTER TABLE ONLY public.driver
    ADD CONSTRAINT driver_pkey PRIMARY KEY (id);


--
-- TOC entry 3323 (class 2606 OID 16436)
-- Name: driver_platform driver_platform_pkey; Type: CONSTRAINT; Schema: public; Owner: dobsykjq_admin
--

ALTER TABLE ONLY public.driver_platform
    ADD CONSTRAINT driver_platform_pkey PRIMARY KEY (id);


--
-- TOC entry 3325 (class 2606 OID 16438)
-- Name: offboarding offboarding_pkey; Type: CONSTRAINT; Schema: public; Owner: dobsykjq_admin
--

ALTER TABLE ONLY public.offboarding
    ADD CONSTRAINT offboarding_pkey PRIMARY KEY (id);


--
-- TOC entry 3327 (class 2606 OID 16440)
-- Name: user user_pkey; Type: CONSTRAINT; Schema: public; Owner: dobsykjq_admin
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);


--
-- TOC entry 3329 (class 2606 OID 16442)
-- Name: user user_username_key; Type: CONSTRAINT; Schema: public; Owner: dobsykjq_admin
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_username_key UNIQUE (username);


--
-- TOC entry 3330 (class 2606 OID 16443)
-- Name: driver driver_hr_approved_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dobsykjq_admin
--

ALTER TABLE ONLY public.driver
    ADD CONSTRAINT driver_hr_approved_by_fkey FOREIGN KEY (hr_approved_by) REFERENCES public."user"(id);


--
-- TOC entry 3331 (class 2606 OID 16448)
-- Name: driver_platform driver_platform_driver_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dobsykjq_admin
--

ALTER TABLE ONLY public.driver_platform
    ADD CONSTRAINT driver_platform_driver_id_fkey FOREIGN KEY (driver_id) REFERENCES public.driver(id) ON DELETE CASCADE;


--
-- TOC entry 3332 (class 2606 OID 16453)
-- Name: offboarding offboarding_driver_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dobsykjq_admin
--

ALTER TABLE ONLY public.offboarding
    ADD CONSTRAINT offboarding_driver_id_fkey FOREIGN KEY (driver_id) REFERENCES public.driver(id);


--
-- TOC entry 3333 (class 2606 OID 16458)
-- Name: offboarding offboarding_requested_by_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dobsykjq_admin
--

ALTER TABLE ONLY public.offboarding
    ADD CONSTRAINT offboarding_requested_by_id_fkey FOREIGN KEY (requested_by_id) REFERENCES public."user"(id);


-- Completed on 2025-10-19 12:26:23 +03

--
-- PostgreSQL database dump complete
--


