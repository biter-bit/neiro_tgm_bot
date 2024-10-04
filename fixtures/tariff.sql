--
-- PostgreSQL database dump
--

-- Dumped from database version 14.13 (Ubuntu 14.13-0ubuntu0.22.04.1)
-- Dumped by pg_dump version 14.13 (Ubuntu 14.13-0ubuntu0.22.04.1)

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: tariff; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tariff (
    id integer NOT NULL,
    name character varying NOT NULL,
    code public.tariffcode NOT NULL,
    description character varying,
    chatgpt_4o_daily_limit integer,
    chatgpt_4o_mini_daily_limit integer,
    midjourney_6_0_daily_limit integer,
    midjourney_5_2_daily_limit integer,
    days integer,
    price_rub integer,
    price_stars integer,
    is_active boolean NOT NULL,
    created_at timestamp without time zone DEFAULT timezone('utc'::text, now()) NOT NULL,
    updated_at timestamp without time zone DEFAULT timezone('utc'::text, now()) NOT NULL
);


ALTER TABLE public.tariff OWNER TO postgres;

--
-- Name: tariff_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tariff_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tariff_id_seq OWNER TO postgres;

--
-- Name: tariff_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tariff_id_seq OWNED BY public.tariff.id;


--
-- Name: tariff id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tariff ALTER COLUMN id SET DEFAULT nextval('public.tariff_id_seq'::regclass);


--
-- Data for Name: tariff; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tariff (id, name, code, description, chatgpt_4o_daily_limit, chatgpt_4o_mini_daily_limit, midjourney_6_0_daily_limit, midjourney_5_2_daily_limit, days, price_rub, price_stars, is_active, created_at, updated_at) FROM stdin;
1	Free	FREE	Бесплатный тариф	0	-1	0	0	\N	\N	\N	t	2024-09-15 14:16:29.932943	2024-09-15 14:16:29.932943
2	Premium	PREMIUM	Премиум тариф	100	-1	20	45	30	489	190	t	2024-09-15 14:19:09.158407	2024-09-15 14:19:09.158407
\.


--
-- Name: tariff_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tariff_id_seq', 2, true);


--
-- Name: tariff tariff_code_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tariff
    ADD CONSTRAINT tariff_code_key UNIQUE (code);


--
-- Name: tariff tariff_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tariff
    ADD CONSTRAINT tariff_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

