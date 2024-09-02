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
-- Name: ai_option; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ai_option (
    id integer NOT NULL,
    name character varying,
    description character varying,
    created_at timestamp without time zone DEFAULT timezone('utc'::text, now()) NOT NULL,
    updated_at timestamp without time zone DEFAULT timezone('utc'::text, now()) NOT NULL
);


ALTER TABLE public.ai_option OWNER TO postgres;

--
-- Name: ai_option_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.ai_option_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ai_option_id_seq OWNER TO postgres;

--
-- Name: ai_option_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ai_option_id_seq OWNED BY public.ai_option.id;


--
-- Name: ai_option id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ai_option ALTER COLUMN id SET DEFAULT nextval('public.ai_option_id_seq'::regclass);


--
-- Data for Name: ai_option; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ai_option (id, name, description, created_at, updated_at) FROM stdin;
1	frequency_penalty	Positive values penalize new tokens based on their existing frequency in the text so far, decreasing the model's likelihood to repeat the same line verbatim	2024-09-01 19:14:57.545131	2024-09-01 19:14:57.545131
2	presence_penalty	Positive values penalize new tokens based on whether they appear in the text so far, increasing the model's likelihood to talk about new topics.	2024-09-01 19:14:57.546853	2024-09-01 19:14:57.546853
3	stop	Up to 4 sequences where the API will stop generating further tokens.	2024-09-01 19:14:57.5484	2024-09-01 19:14:57.5484
4	temperature	What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic. Recommend altering this or top_p but not both.	2024-09-01 19:14:57.549717	2024-09-01 19:14:57.549717
5	top_p	An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered.	2024-09-01 19:14:57.551219	2024-09-01 19:14:57.551219
6	stopSequences	The set of character sequences (up to 5) that will stop output generation.	2024-09-01 19:14:57.552425	2024-09-01 19:14:57.552425
7	temperature	Controls the randomness of the output.	2024-09-01 19:14:57.554356	2024-09-01 19:14:57.554356
8	topP	The topP parameter changes how the model selects tokens for output. Tokens are selected from the most to least probable until the sum of their probabilities equals the topP value.	2024-09-01 19:14:57.555229	2024-09-01 19:14:57.555229
9	topK	The topK parameter changes how the model selects tokens for output.	2024-09-01 19:14:57.556261	2024-09-01 19:14:57.556261
10	stop_sequences	Custom text sequences that will cause the model to stop generating.	2024-09-01 19:14:57.557215	2024-09-01 19:14:57.557215
11	temperature	Amount of randomness injected into the response.	2024-09-01 19:14:57.55805	2024-09-01 19:14:57.55805
12	top_k	Only sample from the top K options for each subsequent token.	2024-09-01 19:14:57.558906	2024-09-01 19:14:57.558906
13	top_p	In nucleus sampling, we compute the cumulative distribution over all the options for each subsequent token in decreasing probability order and cut it off once it reaches a particular probability specified by top_p. You should either alter temperature or top_p, but not both.	2024-09-01 19:14:57.559923	2024-09-01 19:14:57.559923
14	temperature	Affects creativity and randomness of responses. Lower values produce more straightforward responses while higher values lead to increased creativity and randomness.	2024-09-01 19:14:57.561051	2024-09-01 19:14:57.561051
15	--ar	Aspect Ratio	2024-09-01 19:14:57.562129	2024-09-01 19:14:57.562129
16	--chaos	arameter influences how varied the initial image grids are. High --chaos values will produce more unusual and unexpected results and compositions. Lower --chaos values have more reliable, repeatable results.	2024-09-01 19:14:57.563292	2024-09-01 19:14:57.563292
17	--cref	You can use images as character references in your prompt to create images of the same character in different situations.	2024-09-01 19:14:57.564098	2024-09-01 19:14:57.564098
18	--no	The No parameter tells the Midjourney Bot what not to include in your image.	2024-09-01 19:14:57.564883	2024-09-01 19:14:57.564883
19	--seed	The Midjourney bot uses a seed number to create a field of visual noise, like television static, as a starting point to generate the initial image grids. Seed numbers are generated randomly for each image but can be specified with the --seed parameter. If you use the same seed number and prompt, you will get similar final images.	2024-09-01 19:14:57.565582	2024-09-01 19:14:57.565582
20	--stop	Use the --stop parameter to finish a Job partway through the process. Stopping a Job at an earlier percentage can create blurrier, less detailed results.	2024-09-01 19:14:57.569002	2024-09-01 19:14:57.569002
21	--sref	You can use images as style references in your prompt to influence the style or aesthetic of images you want Midjourney to make.	2024-09-01 19:14:57.570346	2024-09-01 19:14:57.570346
22	--stylize	The Midjourney Bot has been trained to produce images that favor artistic color, composition, and forms. The --stylize parameter influences how strongly this training is applied. Low stylization values produce images that closely match the prompt but are less artistic. High stylization values create images that are very artistic but less connected to the prompt.	2024-09-01 19:14:57.571306	2024-09-01 19:14:57.571306
23	--tile	The --tile parameter generates images that can be used as repeating tiles to create seamless patterns for fabrics, wallpapers and textures.	2024-09-01 19:14:57.572683	2024-09-01 19:14:57.572683
24	--weird	Explore unconventional aesthetics with the experimental --weird or --w parameter. This parameter introduces quirky and offbeat qualities to your generated images, resulting in unique and unexpected outcomes.	2024-09-01 19:14:57.573711	2024-09-01 19:14:57.573711
25	size	The size of the generated images	2024-09-01 19:14:57.574989	2024-09-01 19:14:57.574989
26	size	The size of the generated images	2024-09-01 19:14:57.576357	2024-09-01 19:14:57.576357
27	quality	The quality of the image that will be generated. hd creates images with finer details and greater consistency across the image.	2024-09-01 19:14:57.577288	2024-09-01 19:14:57.577288
28	negative_prompt	Items you don't want in the image.	2024-09-01 19:14:57.578131	2024-09-01 19:14:57.578131
29	height	Height of image	2024-09-01 19:14:57.578952	2024-09-01 19:14:57.578952
30	num_inference_steps	Number of denoising steps. Available values: 21, 31, 41, 51.	2024-09-01 19:14:57.57973	2024-09-01 19:14:57.57973
31	enhance_prompt	Enhance prompts for better results	2024-09-01 19:14:57.580586	2024-09-01 19:14:57.580586
32	seed	Seed is used to reproduce results, same seed will give you same image in return again. Pass null for a random number.	2024-09-01 19:14:57.581389	2024-09-01 19:14:57.581389
33	guidance_scale	Scale for classifier-free guidance	2024-09-01 19:14:57.582158	2024-09-01 19:14:57.582158
34	multi_lingual	Allow multi lingual prompt to generate images. Use "no" for the default English.	2024-09-01 19:14:57.582954	2024-09-01 19:14:57.582954
35	panorama	Set this parameter to "yes" to generate a panorama image.	2024-09-01 19:14:57.583976	2024-09-01 19:14:57.583976
36	upscale	Set this parameter to "yes" if you want to upscale the given image resolution two times (2x). If the requested resolution is 512 x 512 px, the generated image will be 1024 x 1024 px.	2024-09-01 19:14:57.585189	2024-09-01 19:14:57.585189
37	width	Ширина изоображения	2024-09-01 19:14:57.586403	2024-09-01 19:14:57.586403
38	height	Высота изоображения	2024-09-01 19:14:57.587414	2024-09-01 19:14:57.587414
39	style	Стиль изоображения	2024-09-01 19:14:57.588382	2024-09-01 19:14:57.588382
40	negativePromptUnclip	Какие цвета и приёмы модель не должна использовать при генерации изображения.	2024-09-01 19:14:57.589332	2024-09-01 19:14:57.589332
41	dialog_mode	В режиме диалога нейросеть будет учитывать предыдущие сообщения	2024-09-01 19:14:57.590324	2024-09-01 19:14:57.590324
42	role	От лица кого нейросеть будет генерировать тексты	2024-09-01 19:14:57.591329	2024-09-01 19:14:57.591329
43	style	Стиль, в котором будет генерироваться изображение	2024-09-01 19:14:57.592201	2024-09-01 19:14:57.592201
\.


--
-- Name: ai_option_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ai_option_id_seq', 1, false);


--
-- Name: ai_option ai_option_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ai_option
    ADD CONSTRAINT ai_option_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

