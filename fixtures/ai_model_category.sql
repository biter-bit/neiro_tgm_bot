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
-- Name: ai_model_category; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ai_model_category (
    id integer NOT NULL,
    name character varying,
    type character varying,
    description character varying,
    created_at timestamp without time zone DEFAULT timezone('utc'::text, now()) NOT NULL,
    updated_at timestamp without time zone DEFAULT timezone('utc'::text, now()) NOT NULL
);


ALTER TABLE public.ai_model_category OWNER TO postgres;

--
-- Name: ai_model_category_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.ai_model_category_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ai_model_category_id_seq OWNER TO postgres;

--
-- Name: ai_model_category_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ai_model_category_id_seq OWNED BY public.ai_model_category.id;


--
-- Name: ai_model_category id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ai_model_category ALTER COLUMN id SET DEFAULT nextval('public.ai_model_category_id_seq'::regclass);


--
-- Data for Name: ai_model_category; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ai_model_category (id, name, type, description, created_at, updated_at) FROM stdin;
1	ChatGPT	ChatGPT description	text	2024-09-01 19:10:12.312488	2024-09-01 19:10:12.312488
2	YandexGPT	YandexGPT description	text	2024-09-01 19:10:12.316888	2024-09-01 19:10:12.316888
3	Gemini Pro	Gemini Pro description	text	2024-09-01 19:10:12.317981	2024-09-01 19:10:12.317981
4	Claude	Claude description	text	2024-09-01 19:10:12.319207	2024-09-01 19:10:12.319207
5	Kandinsky	Kandinsky description	image	2024-09-01 19:10:12.320209	2024-09-01 19:10:12.320209
6	Midjourney	Midjourney description	image	2024-09-01 19:10:12.321723	2024-09-01 19:10:12.321723
7	DALL-E	DALL-E description	image	2024-09-01 19:10:12.323184	2024-09-01 19:10:12.323184
8	StableDiffusion	StableDiffusion description	image	2024-09-01 19:10:12.324246	2024-09-01 19:10:12.324246
9	Pika ART	Pica description	video	2024-09-01 19:10:12.32529	2024-09-01 19:10:12.32529
\.


--
-- Name: ai_model_category_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ai_model_category_id_seq', 1, false);


--
-- Name: ai_model_category ai_model_category_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ai_model_category
    ADD CONSTRAINT ai_model_category_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

