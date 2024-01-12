--
-- PostgreSQL database dump
--

-- Dumped from database version 13.13 (Debian 13.13-1.pgdg120+1)
-- Dumped by pg_dump version 13.13 (Debian 13.13-1.pgdg120+1)

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
-- Name: tag_category_enum; Type: TYPE; Schema: public; Owner: username
--

CREATE TYPE public.tag_category_enum AS ENUM (
    'Durée de préparation',
    'Type de cuisine',
    'Régime alimentaire',
    'Saison'
);


ALTER TYPE public.tag_category_enum OWNER TO username;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: foods; Type: TABLE; Schema: public; Owner: username
--

CREATE TABLE public.foods (
    food_id integer NOT NULL,
    user_id integer,
    name character varying(255) NOT NULL,
    brand character varying(255),
    calories numeric,
    fats numeric,
    saturated_fats numeric,
    carbohydrates numeric,
    sugars numeric,
    fibers numeric,
    proteins numeric,
    sodium numeric,
    unit_id integer NOT NULL
);


ALTER TABLE public.foods OWNER TO username;

--
-- Name: foods_food_id_seq; Type: SEQUENCE; Schema: public; Owner: username
--

CREATE SEQUENCE public.foods_food_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.foods_food_id_seq OWNER TO username;

--
-- Name: foods_food_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: username
--

ALTER SEQUENCE public.foods_food_id_seq OWNED BY public.foods.food_id;


--
-- Name: portions; Type: TABLE; Schema: public; Owner: username
--

CREATE TABLE public.portions (
    portion_id integer NOT NULL,
    food_id integer NOT NULL,
    name character varying(255),
    size numeric NOT NULL
);


ALTER TABLE public.portions OWNER TO username;

--
-- Name: portions_portion_id_seq; Type: SEQUENCE; Schema: public; Owner: username
--

CREATE SEQUENCE public.portions_portion_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.portions_portion_id_seq OWNER TO username;

--
-- Name: portions_portion_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: username
--

ALTER SEQUENCE public.portions_portion_id_seq OWNED BY public.portions.portion_id;


--
-- Name: recipe_foods; Type: TABLE; Schema: public; Owner: username
--

CREATE TABLE public.recipe_foods (
    recipe_id integer NOT NULL,
    food_id integer NOT NULL,
    quantity numeric,
    portion_id integer
);


ALTER TABLE public.recipe_foods OWNER TO username;

--
-- Name: recipe_tags; Type: TABLE; Schema: public; Owner: username
--

CREATE TABLE public.recipe_tags (
    recipe_id integer NOT NULL,
    tag_id integer NOT NULL
);


ALTER TABLE public.recipe_tags OWNER TO username;

--
-- Name: recipes; Type: TABLE; Schema: public; Owner: username
--

CREATE TABLE public.recipes (
    recipe_id integer NOT NULL,
    user_id integer,
    title character varying(255) NOT NULL,
    description text,
    total_time integer,
    prep_time integer,
    difficulty character varying(50),
    ustensils character varying(255)[],
    image_url text
);


ALTER TABLE public.recipes OWNER TO username;

--
-- Name: recipes_recipe_id_seq; Type: SEQUENCE; Schema: public; Owner: username
--

CREATE SEQUENCE public.recipes_recipe_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.recipes_recipe_id_seq OWNER TO username;

--
-- Name: recipes_recipe_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: username
--

ALTER SEQUENCE public.recipes_recipe_id_seq OWNED BY public.recipes.recipe_id;


--
-- Name: refresh_tokens; Type: TABLE; Schema: public; Owner: username
--

CREATE TABLE public.refresh_tokens (
    id integer NOT NULL,
    jti character varying(255) NOT NULL,
    user_id integer NOT NULL,
    revoked boolean DEFAULT false,
    expires_at timestamp without time zone NOT NULL
);


ALTER TABLE public.refresh_tokens OWNER TO username;

--
-- Name: refresh_tokens_id_seq; Type: SEQUENCE; Schema: public; Owner: username
--

CREATE SEQUENCE public.refresh_tokens_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.refresh_tokens_id_seq OWNER TO username;

--
-- Name: refresh_tokens_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: username
--

ALTER SEQUENCE public.refresh_tokens_id_seq OWNED BY public.refresh_tokens.id;


--
-- Name: steps; Type: TABLE; Schema: public; Owner: username
--

CREATE TABLE public.steps (
    recipe_id integer NOT NULL,
    step_number integer NOT NULL,
    description text[],
    image_url text
);


ALTER TABLE public.steps OWNER TO username;

--
-- Name: tags; Type: TABLE; Schema: public; Owner: username
--

CREATE TABLE public.tags (
    tag_id integer NOT NULL,
    category public.tag_category_enum,
    name character varying(100) NOT NULL
);


ALTER TABLE public.tags OWNER TO username;

--
-- Name: tags_tag_id_seq; Type: SEQUENCE; Schema: public; Owner: username
--

CREATE SEQUENCE public.tags_tag_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tags_tag_id_seq OWNER TO username;

--
-- Name: tags_tag_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: username
--

ALTER SEQUENCE public.tags_tag_id_seq OWNED BY public.tags.tag_id;


--
-- Name: units; Type: TABLE; Schema: public; Owner: username
--

CREATE TABLE public.units (
    unit_id integer NOT NULL,
    name character varying(50) NOT NULL
);


ALTER TABLE public.units OWNER TO username;

--
-- Name: units_unit_id_seq; Type: SEQUENCE; Schema: public; Owner: username
--

CREATE SEQUENCE public.units_unit_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.units_unit_id_seq OWNER TO username;

--
-- Name: units_unit_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: username
--

ALTER SEQUENCE public.units_unit_id_seq OWNED BY public.units.unit_id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: username
--

CREATE TABLE public.users (
    user_id integer NOT NULL,
    username character varying(255) NOT NULL,
    email character varying(255) NOT NULL,
    hashed_password text NOT NULL,
    is_admin boolean
);


ALTER TABLE public.users OWNER TO username;

--
-- Name: users_user_id_seq; Type: SEQUENCE; Schema: public; Owner: username
--

CREATE SEQUENCE public.users_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_user_id_seq OWNER TO username;

--
-- Name: users_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: username
--

ALTER SEQUENCE public.users_user_id_seq OWNED BY public.users.user_id;


--
-- Name: foods food_id; Type: DEFAULT; Schema: public; Owner: username
--

ALTER TABLE ONLY public.foods ALTER COLUMN food_id SET DEFAULT nextval('public.foods_food_id_seq'::regclass);


--
-- Name: portions portion_id; Type: DEFAULT; Schema: public; Owner: username
--

ALTER TABLE ONLY public.portions ALTER COLUMN portion_id SET DEFAULT nextval('public.portions_portion_id_seq'::regclass);


--
-- Name: recipes recipe_id; Type: DEFAULT; Schema: public; Owner: username
--

ALTER TABLE ONLY public.recipes ALTER COLUMN recipe_id SET DEFAULT nextval('public.recipes_recipe_id_seq'::regclass);


--
-- Name: refresh_tokens id; Type: DEFAULT; Schema: public; Owner: username
--

ALTER TABLE ONLY public.refresh_tokens ALTER COLUMN id SET DEFAULT nextval('public.refresh_tokens_id_seq'::regclass);


--
-- Name: tags tag_id; Type: DEFAULT; Schema: public; Owner: username
--

ALTER TABLE ONLY public.tags ALTER COLUMN tag_id SET DEFAULT nextval('public.tags_tag_id_seq'::regclass);


--
-- Name: units unit_id; Type: DEFAULT; Schema: public; Owner: username
--

ALTER TABLE ONLY public.units ALTER COLUMN unit_id SET DEFAULT nextval('public.units_unit_id_seq'::regclass);


--
-- Name: users user_id; Type: DEFAULT; Schema: public; Owner: username
--

ALTER TABLE ONLY public.users ALTER COLUMN user_id SET DEFAULT nextval('public.users_user_id_seq'::regclass);


--
-- Data for Name: foods; Type: TABLE DATA; Schema: public; Owner: username
--

COPY public.foods (food_id, user_id, name, brand, calories, fats, saturated_fats, carbohydrates, sugars, fibers, proteins, sodium, unit_id) FROM stdin;
\.


--
-- Data for Name: portions; Type: TABLE DATA; Schema: public; Owner: username
--

COPY public.portions (portion_id, food_id, name, size) FROM stdin;
\.


--
-- Data for Name: recipe_foods; Type: TABLE DATA; Schema: public; Owner: username
--

COPY public.recipe_foods (recipe_id, food_id, quantity, portion_id) FROM stdin;
\.


--
-- Data for Name: recipe_tags; Type: TABLE DATA; Schema: public; Owner: username
--

COPY public.recipe_tags (recipe_id, tag_id) FROM stdin;
\.


--
-- Data for Name: recipes; Type: TABLE DATA; Schema: public; Owner: username
--

COPY public.recipes (recipe_id, user_id, title, description, total_time, prep_time, difficulty, ustensils, image_url) FROM stdin;
\.


--
-- Data for Name: refresh_tokens; Type: TABLE DATA; Schema: public; Owner: username
--

COPY public.refresh_tokens (id, jti, user_id, revoked, expires_at) FROM stdin;
\.


--
-- Data for Name: steps; Type: TABLE DATA; Schema: public; Owner: username
--

COPY public.steps (recipe_id, step_number, description, image_url) FROM stdin;
\.


--
-- Data for Name: tags; Type: TABLE DATA; Schema: public; Owner: username
--

COPY public.tags (tag_id, category, name) FROM stdin;
\.


--
-- Data for Name: units; Type: TABLE DATA; Schema: public; Owner: username
--

COPY public.units (unit_id, name) FROM stdin;
1	gramme
2	ml
3	cl
4	litre
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: username
--

COPY public.users (user_id, username, email, hashed_password, is_admin) FROM stdin;
1	Foor Bar	food@bar.com	hashed_password	t
\.


--
-- Name: foods_food_id_seq; Type: SEQUENCE SET; Schema: public; Owner: username
--

SELECT pg_catalog.setval('public.foods_food_id_seq', 1, false);


--
-- Name: portions_portion_id_seq; Type: SEQUENCE SET; Schema: public; Owner: username
--

SELECT pg_catalog.setval('public.portions_portion_id_seq', 1, false);


--
-- Name: recipes_recipe_id_seq; Type: SEQUENCE SET; Schema: public; Owner: username
--

SELECT pg_catalog.setval('public.recipes_recipe_id_seq', 1, false);


--
-- Name: refresh_tokens_id_seq; Type: SEQUENCE SET; Schema: public; Owner: username
--

SELECT pg_catalog.setval('public.refresh_tokens_id_seq', 1, false);


--
-- Name: tags_tag_id_seq; Type: SEQUENCE SET; Schema: public; Owner: username
--

SELECT pg_catalog.setval('public.tags_tag_id_seq', 1, false);


--
-- Name: units_unit_id_seq; Type: SEQUENCE SET; Schema: public; Owner: username
--

SELECT pg_catalog.setval('public.units_unit_id_seq', 1, false);


--
-- Name: users_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: username
--

SELECT pg_catalog.setval('public.users_user_id_seq', 1, false);


--
-- Name: foods foods_pkey; Type: CONSTRAINT; Schema: public; Owner: username
--

ALTER TABLE ONLY public.foods
    ADD CONSTRAINT foods_pkey PRIMARY KEY (food_id);


--
-- Name: portions portions_pkey; Type: CONSTRAINT; Schema: public; Owner: username
--

ALTER TABLE ONLY public.portions
    ADD CONSTRAINT portions_pkey PRIMARY KEY (portion_id);


--
-- Name: recipe_foods recipe_foods_pkey; Type: CONSTRAINT; Schema: public; Owner: username
--

ALTER TABLE ONLY public.recipe_foods
    ADD CONSTRAINT recipe_foods_pkey PRIMARY KEY (recipe_id, food_id);


--
-- Name: recipe_tags recipe_tags_pkey; Type: CONSTRAINT; Schema: public; Owner: username
--

ALTER TABLE ONLY public.recipe_tags
    ADD CONSTRAINT recipe_tags_pkey PRIMARY KEY (recipe_id, tag_id);


--
-- Name: recipes recipes_pkey; Type: CONSTRAINT; Schema: public; Owner: username
--

ALTER TABLE ONLY public.recipes
    ADD CONSTRAINT recipes_pkey PRIMARY KEY (recipe_id);


--
-- Name: refresh_tokens refresh_tokens_pkey; Type: CONSTRAINT; Schema: public; Owner: username
--

ALTER TABLE ONLY public.refresh_tokens
    ADD CONSTRAINT refresh_tokens_pkey PRIMARY KEY (id);


--
-- Name: steps steps_pkey; Type: CONSTRAINT; Schema: public; Owner: username
--

ALTER TABLE ONLY public.steps
    ADD CONSTRAINT steps_pkey PRIMARY KEY (recipe_id, step_number);


--
-- Name: tags tags_pkey; Type: CONSTRAINT; Schema: public; Owner: username
--

ALTER TABLE ONLY public.tags
    ADD CONSTRAINT tags_pkey PRIMARY KEY (tag_id);


--
-- Name: units units_pkey; Type: CONSTRAINT; Schema: public; Owner: username
--

ALTER TABLE ONLY public.units
    ADD CONSTRAINT units_pkey PRIMARY KEY (unit_id);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: username
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: username
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- Name: refresh_tokens fk_user; Type: FK CONSTRAINT; Schema: public; Owner: username
--

ALTER TABLE ONLY public.refresh_tokens
    ADD CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES public.users(user_id) ON DELETE CASCADE;


--
-- Name: foods foods_unit_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: username
--

ALTER TABLE ONLY public.foods
    ADD CONSTRAINT foods_unit_id_fkey FOREIGN KEY (unit_id) REFERENCES public.units(unit_id);


--
-- Name: foods foods_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: username
--

ALTER TABLE ONLY public.foods
    ADD CONSTRAINT foods_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id) ON DELETE SET NULL;


--
-- Name: portions portions_food_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: username
--

ALTER TABLE ONLY public.portions
    ADD CONSTRAINT portions_food_id_fkey FOREIGN KEY (food_id) REFERENCES public.foods(food_id);


--
-- Name: recipe_foods recipe_foods_food_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: username
--

ALTER TABLE ONLY public.recipe_foods
    ADD CONSTRAINT recipe_foods_food_id_fkey FOREIGN KEY (food_id) REFERENCES public.foods(food_id);


--
-- Name: recipe_foods recipe_foods_portion_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: username
--

ALTER TABLE ONLY public.recipe_foods
    ADD CONSTRAINT recipe_foods_portion_id_fkey FOREIGN KEY (portion_id) REFERENCES public.portions(portion_id);


--
-- Name: recipe_foods recipe_foods_recipe_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: username
--

ALTER TABLE ONLY public.recipe_foods
    ADD CONSTRAINT recipe_foods_recipe_id_fkey FOREIGN KEY (recipe_id) REFERENCES public.recipes(recipe_id);


--
-- Name: recipe_tags recipe_tags_recipe_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: username
--

ALTER TABLE ONLY public.recipe_tags
    ADD CONSTRAINT recipe_tags_recipe_id_fkey FOREIGN KEY (recipe_id) REFERENCES public.recipes(recipe_id);


--
-- Name: recipe_tags recipe_tags_tag_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: username
--

ALTER TABLE ONLY public.recipe_tags
    ADD CONSTRAINT recipe_tags_tag_id_fkey FOREIGN KEY (tag_id) REFERENCES public.tags(tag_id);


--
-- Name: recipes recipes_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: username
--

ALTER TABLE ONLY public.recipes
    ADD CONSTRAINT recipes_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- Name: steps steps_recipe_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: username
--

ALTER TABLE ONLY public.steps
    ADD CONSTRAINT steps_recipe_id_fkey FOREIGN KEY (recipe_id) REFERENCES public.recipes(recipe_id);


--
-- PostgreSQL database dump complete
--

