--
-- PostgreSQL database dump
--

-- Dumped from database version 10.12 (Ubuntu 10.12-0ubuntu0.18.04.1)
-- Dumped by pg_dump version 10.12 (Ubuntu 10.12-0ubuntu0.18.04.1)

-- Started on 2020-07-01 18:30:12 EEST

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
-- TOC entry 2971 (class 0 OID 17075)
-- Dependencies: 198
-- Data for Name: Branches; Type: TABLE DATA; Schema: public; Owner: khairallah
--

COPY public."Branches" (id, name, is_active) FROM stdin;
1	North Branch	t
2	West Branch	t
3	HQ Branch	t
\.


--
-- TOC entry 2975 (class 0 OID 17099)
-- Dependencies: 202
-- Data for Name: FaultTypes; Type: TABLE DATA; Schema: public; Owner: khairallah
--

COPY public."FaultTypes" (id, fault_type, it_section, is_active) FROM stdin;
1	Printers Problem	3	t
2	PSD Archive System	1	t
3	IP Telephony	2	t
4	Internet Connection	2	t
\.


--
-- TOC entry 2977 (class 0 OID 17123)
-- Dependencies: 204
-- Data for Name: Faults; Type: TABLE DATA; Schema: public; Owner: khairallah
--

COPY public."Faults" (id, fault_type, fault_description, branch_id, status) FROM stdin;
1	1	Printer is not recognized	1	New
\.


--
-- TOC entry 2979 (class 0 OID 17145)
-- Dependencies: 206
-- Data for Name: FaultsAction; Type: TABLE DATA; Schema: public; Owner: khairallah
--

COPY public."FaultsAction" (id, fault_id, action_taken, action_by, action_time, current_status, new_status) FROM stdin;
\.


--
-- TOC entry 2973 (class 0 OID 17087)
-- Dependencies: 200
-- Data for Name: ITSections; Type: TABLE DATA; Schema: public; Owner: khairallah
--

COPY public."ITSections" (id, name, is_active) FROM stdin;
2	Telephony Section	t
3	PC Section	t
1	Archive System Section	t
4	Communication Section	t
\.




--
-- TOC entry 2993 (class 0 OID 0)
-- Dependencies: 197
-- Name: Branches_id_seq; Type: SEQUENCE SET; Schema: public; Owner: khairallah
--

SELECT pg_catalog.setval('public."Branches_id_seq"', 3, true);


--
-- TOC entry 2994 (class 0 OID 0)
-- Dependencies: 201
-- Name: FaultTypes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: khairallah
--

SELECT pg_catalog.setval('public."FaultTypes_id_seq"', 4, true);


--
-- TOC entry 2995 (class 0 OID 0)
-- Dependencies: 205
-- Name: FaultsAction_id_seq; Type: SEQUENCE SET; Schema: public; Owner: khairallah
--

SELECT pg_catalog.setval('public."FaultsAction_id_seq"', 1, false);


--
-- TOC entry 2996 (class 0 OID 0)
-- Dependencies: 203
-- Name: Faults_id_seq; Type: SEQUENCE SET; Schema: public; Owner: khairallah
--

SELECT pg_catalog.setval('public."Faults_id_seq"', 1, true);


--
-- TOC entry 2997 (class 0 OID 0)
-- Dependencies: 199
-- Name: ITSections_id_seq; Type: SEQUENCE SET; Schema: public; Owner: khairallah
--

SELECT pg_catalog.setval('public."ITSections_id_seq"', 4, true);


-- Completed on 2020-07-01 18:30:12 EEST

--
-- PostgreSQL database dump complete
--

