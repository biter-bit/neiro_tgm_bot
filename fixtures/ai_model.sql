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
-- Name: ai_model; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ai_model (
    code character varying NOT NULL,
    name character varying,
    type character varying,
    is_active boolean,
    created_at timestamp without time zone DEFAULT timezone('utc'::text, now()) NOT NULL,
    updated_at timestamp without time zone DEFAULT timezone('utc'::text, now()) NOT NULL
);


ALTER TABLE public.ai_model OWNER TO postgres;

--
-- Data for Name: ai_model; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ai_model (code, name, type, is_active, created_at, updated_at) FROM stdin;
gpt-4o	GPT_4_O	text	t	2024-09-15 14:01:53.717622	2024-09-15 14:01:53.717622
gpt-4o-mini	GPT_4_O_MINI	text	t	2024-09-15 14:01:53.722313	2024-09-15 14:01:53.722313
mj	MIDJOURNEY	image	t	2024-09-15 14:01:53.724711	2024-09-15 14:01:53.724711
\.


--
-- Name: ai_model ai_model_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ai_model
    ADD CONSTRAINT ai_model_pkey PRIMARY KEY (code);


--
-- PostgreSQL database dump complete
--

