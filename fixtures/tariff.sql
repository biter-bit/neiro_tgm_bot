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
    chatgpt_daily_limit integer,
    gemini_daily_limit integer,
    kandinsky_daily_limit integer,
    sd_daily_limit integer,
    token_balance integer NOT NULL,
    days integer NOT NULL,
    price integer NOT NULL,
    price_usd double precision NOT NULL,
    price_ton double precision NOT NULL,
    price_stars integer NOT NULL,
    is_active boolean NOT NULL,
    is_trial boolean NOT NULL,
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

COPY public.tariff (id, name, code, description, chatgpt_daily_limit, gemini_daily_limit, kandinsky_daily_limit, sd_daily_limit, token_balance, days, price, price_usd, price_ton, price_stars, is_active, is_trial, created_at, updated_at) FROM stdin;
1	Free	FREE	Бесплатный тариф	0	40	10	10	0	0	0	0	0	0	f	f	2024-09-01 18:13:40.328912	2024-09-01 18:13:40.328912
6	1₽ / 500 токенов / На 24 часа	TRIAL_500	Пробный тариф 500	-1	0	0	0	0	1	1	0	0	1	f	t	2024-09-01 18:13:40.337639	2024-09-01 18:13:40.337639
7	1₽ / 1500 токенов / На 24 часа	TRIAL_1500	Пробный тариф 1500	-1	0	0	0	0	1	1	0	0	1	f	t	2024-09-01 18:13:40.339171	2024-09-01 18:13:40.339171
8	1₽ / 3000 токенов / На 24 часа	TRIAL_3000	Пробный тариф 3000	-1	0	0	0	0	1	1	0	0	1	f	t	2024-09-01 18:13:40.340452	2024-09-01 18:13:40.340452
9	1₽ / 6000 токенов / На 24 часа	TRIAL_6000	Пробный тариф 6000	-1	0	0	0	0	1	1	0	0	1	f	t	2024-09-01 18:13:40.342096	2024-09-01 18:13:40.342096
10	300 токенов	TOKEN_300	Дополнительные 300 токенов	0	0	0	0	300	0	200	2.1	0.274869	200	t	f	2024-09-01 18:13:40.343544	2024-09-01 18:13:40.343544
14	API 1000	API_1000	Пополнение баланса API на 1000р.	0	0	0	0	0	0	1000	0	0	556	f	f	2024-09-01 18:13:40.344794	2024-09-01 18:13:40.344794
15	API 5000	API_5000	Пополнение баланса API на 5000р.	0	0	0	0	0	0	5000	0	0	2778	f	f	2024-09-01 18:13:40.345958	2024-09-01 18:13:40.345958
16	API 10000	API_10000	Пополнение баланса API на 10000р.	0	0	0	0	0	0	10000	0	0	5556	f	f	2024-09-01 18:13:40.347391	2024-09-01 18:13:40.347391
17	API 25000	API_25000	Пополнение баланса API на 25000р.	0	0	0	0	0	0	25000	0	0	13889	f	f	2024-09-01 18:13:40.349038	2024-09-01 18:13:40.349038
18	API 50000	API_50000	Пополнение баланса API на 50000р.	0	0	0	0	0	0	50000	0	0	27778	f	f	2024-09-01 18:13:40.350644	2024-09-01 18:13:40.350644
19	🔥 Пробный тариф за 100₽ / 50 токенов / 3 дня	TRIAL_50	Пробный тариф 500	-1	-1	-1	-1	50	3	100	0	0	56	f	t	2024-09-01 18:13:40.351832	2024-09-01 18:13:40.351832
11	450 токенов	TOKEN_450	Дополнительные 450 токенов	0	0	0	0	450	0	300	3.2	0.418848	330	t	f	2024-09-01 18:13:40.355725	2024-09-01 18:13:40.355725
12	3000 токенов	TOKEN_3000	Дополнительные 3000 токенов	0	0	0	0	3000	0	2000	21.3	2.79	2300	t	f	2024-09-01 18:13:40.357054	2024-09-01 18:13:40.357054
13	9000 токенов	TOKEN_9000	Дополнительные 9000 токенов	0	0	0	0	9000	0	6000	63.8	8.35	6300	t	f	2024-09-01 18:13:40.358106	2024-09-01 18:13:40.358106
3	💎 1500 токенов	MAIN_1500	Стандартный тариф	-1	-1	-1	-1	1500	30	990	10.5	1.37	1100	t	f	2024-09-01 18:13:40.359322	2024-09-01 18:13:40.359322
2	💎 500 токенов	MAIN_500	Пробный тариф на месяц	-1	-1	-1	-1	500	30	490	5.2	0.680628	660	t	f	2024-09-01 18:13:40.360953	2024-09-01 18:13:40.360953
4	💎 3000 токенов	MAIN_3000	Премиум тариф	-1	0	0	0	3000	30	1800	19.1	2.5	2000	t	f	2024-09-01 18:13:40.362544	2024-09-01 18:13:40.362544
5	💎 6000 токенов	MAIN_6000	Бизнес тариф	-1	-1	-1	-1	6000	30	3200	34.1	4.46	3500	t	f	2024-09-01 18:13:40.36397	2024-09-01 18:13:40.36397
\.


--
-- Name: tariff_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tariff_id_seq', 1, false);


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

