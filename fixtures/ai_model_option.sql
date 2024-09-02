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
-- Name: ai_model_option; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ai_model_option (
    id integer NOT NULL,
    ai_model_id character varying(50) NOT NULL,
    ai_option_id bigint NOT NULL
);


ALTER TABLE public.ai_model_option OWNER TO postgres;

--
-- Data for Name: ai_model_option; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ai_model_option (id, ai_model_id, ai_option_id) FROM stdin;
1	gpt-4o	1
2	pica	1
3	bard	6
4	bard	7
5	bard	8
6	bard	9
7	bard	41
8	bard	42
9	claude-3-haiku-20240307	41
10	claude-3-haiku-20240307	10
11	claude-3-haiku-20240307	11
12	claude-3-haiku-20240307	12
13	claude-3-haiku-20240307	13
14	claude-3-haiku-20240307	42
15	claude-3-opus-20240229	41
16	claude-3-opus-20240229	10
17	claude-3-opus-20240229	11
18	claude-3-opus-20240229	12
19	claude-3-opus-20240229	13
20	claude-3-opus-20240229	42
21	claude-3-sonnet-20240229	41
22	claude-3-sonnet-20240229	10
23	claude-3-sonnet-20240229	11
24	claude-3-sonnet-20240229	12
25	claude-3-sonnet-20240229	13
26	claude-3-sonnet-20240229	42
27	dall-e-2	25
28	dall-e-3	26
29	dall-e-3	27
30	gpt-3.5-turbo-1106	1
31	gpt-3.5-turbo-1106	2
32	gpt-3.5-turbo-1106	3
33	gpt-3.5-turbo-1106	4
34	gpt-3.5-turbo-1106	5
35	gpt-3.5-turbo-1106	41
36	gpt-3.5-turbo-1106	42
37	gpt-4	1
38	gpt-4	2
39	gpt-4	3
40	gpt-4	4
41	gpt-4	5
42	gpt-4	41
43	gpt-4	42
44	gpt-4-1106-preview	1
45	gpt-4-1106-preview	2
46	gpt-4-1106-preview	3
47	gpt-4-1106-preview	4
48	gpt-4-1106-preview	5
49	gpt-4-1106-preview	41
50	gpt-4-1106-preview	42
51	gpt-4-vision-preview	1
52	gpt-4-vision-preview	2
53	gpt-4-vision-preview	3
54	gpt-4-vision-preview	4
55	gpt-4-vision-preview	5
56	gpt-4-vision-preview	41
57	gpt-4-vision-preview	42
58	kandinsky	40
59	kandinsky	37
60	kandinsky	38
61	kandinsky	39
62	mj	43
63	mj	15
64	mj	16
65	mj	17
66	mj	18
67	mj	19
68	mj	20
69	mj	21
70	mj	22
71	mj	23
72	mj	24
73	sd	32
74	sd	33
75	sd	34
76	sd	35
77	sd	36
78	sd	28
79	sd	29
80	sd	30
81	sd	31
82	yandexgpt	41
83	yandexgpt	42
84	yandexgpt	14
85	yandexgpt-lite	41
86	yandexgpt-lite	42
87	yandexgpt-lite	14
\.


--
-- Name: ai_model_option ai_model_option_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ai_model_option
    ADD CONSTRAINT ai_model_option_pkey PRIMARY KEY (id, ai_model_id, ai_option_id);


--
-- Name: ai_model_option ai_model_option_ai_model_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ai_model_option
    ADD CONSTRAINT ai_model_option_ai_model_id_fkey FOREIGN KEY (ai_model_id) REFERENCES public.ai_model(code) ON DELETE CASCADE;


--
-- Name: ai_model_option ai_model_option_ai_option_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ai_model_option
    ADD CONSTRAINT ai_model_option_ai_option_id_fkey FOREIGN KEY (ai_option_id) REFERENCES public.ai_option(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

