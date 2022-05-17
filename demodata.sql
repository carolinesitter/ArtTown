--
-- PostgreSQL database dump
--

-- Dumped from database version 14.2
-- Dumped by pg_dump version 14.2

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
-- Name: artist_collections; Type: TABLE; Schema: public; Owner: carolinesitter
--

CREATE TABLE public.artist_collections (
    artist_collection_id integer NOT NULL,
    user_id integer,
    gallery_title character varying NOT NULL,
    gallery_description character varying NOT NULL
);


ALTER TABLE public.artist_collections OWNER TO carolinesitter;

--
-- Name: artist_collections_artist_collection_id_seq; Type: SEQUENCE; Schema: public; Owner: carolinesitter
--

CREATE SEQUENCE public.artist_collections_artist_collection_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.artist_collections_artist_collection_id_seq OWNER TO carolinesitter;

--
-- Name: artist_collections_artist_collection_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: carolinesitter
--

ALTER SEQUENCE public.artist_collections_artist_collection_id_seq OWNED BY public.artist_collections.artist_collection_id;


--
-- Name: comment; Type: TABLE; Schema: public; Owner: carolinesitter
--

CREATE TABLE public.comment (
    comment_id integer NOT NULL,
    comment character varying(250) NOT NULL,
    image_id integer,
    user_id integer
);


ALTER TABLE public.comment OWNER TO carolinesitter;

--
-- Name: comment_comment_id_seq; Type: SEQUENCE; Schema: public; Owner: carolinesitter
--

CREATE SEQUENCE public.comment_comment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.comment_comment_id_seq OWNER TO carolinesitter;

--
-- Name: comment_comment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: carolinesitter
--

ALTER SEQUENCE public.comment_comment_id_seq OWNED BY public.comment.comment_id;


--
-- Name: images; Type: TABLE; Schema: public; Owner: carolinesitter
--

CREATE TABLE public.images (
    image_id integer NOT NULL,
    artist_collection_id integer,
    user_id integer,
    image_title character varying(50) NOT NULL,
    image_link character varying NOT NULL,
    date_uploaded timestamp without time zone NOT NULL
);


ALTER TABLE public.images OWNER TO carolinesitter;

--
-- Name: images_image_id_seq; Type: SEQUENCE; Schema: public; Owner: carolinesitter
--

CREATE SEQUENCE public.images_image_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.images_image_id_seq OWNER TO carolinesitter;

--
-- Name: images_image_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: carolinesitter
--

ALTER SEQUENCE public.images_image_id_seq OWNED BY public.images.image_id;


--
-- Name: likes; Type: TABLE; Schema: public; Owner: carolinesitter
--

CREATE TABLE public.likes (
    like_id integer NOT NULL,
    image_id integer,
    user_id integer
);


ALTER TABLE public.likes OWNER TO carolinesitter;

--
-- Name: likes_like_id_seq; Type: SEQUENCE; Schema: public; Owner: carolinesitter
--

CREATE SEQUENCE public.likes_like_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.likes_like_id_seq OWNER TO carolinesitter;

--
-- Name: likes_like_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: carolinesitter
--

ALTER SEQUENCE public.likes_like_id_seq OWNED BY public.likes.like_id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: carolinesitter
--

CREATE TABLE public.users (
    user_id integer NOT NULL,
    first_name character varying(50) NOT NULL,
    last_name character varying(50) NOT NULL,
    email character varying(50) NOT NULL,
    username character varying(50) NOT NULL,
    password character varying(50) NOT NULL,
    instagram character varying(50),
    twitter character varying(50),
    tiktok character varying(50),
    website character varying(50),
    zipcode integer NOT NULL
);


ALTER TABLE public.users OWNER TO carolinesitter;

--
-- Name: users_user_id_seq; Type: SEQUENCE; Schema: public; Owner: carolinesitter
--

CREATE SEQUENCE public.users_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_user_id_seq OWNER TO carolinesitter;

--
-- Name: users_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: carolinesitter
--

ALTER SEQUENCE public.users_user_id_seq OWNED BY public.users.user_id;


--
-- Name: artist_collections artist_collection_id; Type: DEFAULT; Schema: public; Owner: carolinesitter
--

ALTER TABLE ONLY public.artist_collections ALTER COLUMN artist_collection_id SET DEFAULT nextval('public.artist_collections_artist_collection_id_seq'::regclass);


--
-- Name: comment comment_id; Type: DEFAULT; Schema: public; Owner: carolinesitter
--

ALTER TABLE ONLY public.comment ALTER COLUMN comment_id SET DEFAULT nextval('public.comment_comment_id_seq'::regclass);


--
-- Name: images image_id; Type: DEFAULT; Schema: public; Owner: carolinesitter
--

ALTER TABLE ONLY public.images ALTER COLUMN image_id SET DEFAULT nextval('public.images_image_id_seq'::regclass);


--
-- Name: likes like_id; Type: DEFAULT; Schema: public; Owner: carolinesitter
--

ALTER TABLE ONLY public.likes ALTER COLUMN like_id SET DEFAULT nextval('public.likes_like_id_seq'::regclass);


--
-- Name: users user_id; Type: DEFAULT; Schema: public; Owner: carolinesitter
--

ALTER TABLE ONLY public.users ALTER COLUMN user_id SET DEFAULT nextval('public.users_user_id_seq'::regclass);


--
-- Data for Name: artist_collections; Type: TABLE DATA; Schema: public; Owner: carolinesitter
--

COPY public.artist_collections (artist_collection_id, user_id, gallery_title, gallery_description) FROM stdin;
1	1	Turtle Frenzy	Utilized oil pastels to capture adorable essence of turtle-kind.
5	2	A Unique Perspective	Playing with dimension in order to influence the line of vision.
47	3	Into the Green	Explored the mystical and dreamlike atmosphere of the forest through digital art.
48	3	Forest Creatures	Developed skills with character art and design.
50	4	Into the Unknown 	A study in color, texture, and squid.
51	4	Ocean's Paint	Worked with thicker brush strokes to create texture on the canvas
\.


--
-- Data for Name: comment; Type: TABLE DATA; Schema: public; Owner: carolinesitter
--

COPY public.comment (comment_id, comment, image_id, user_id) FROM stdin;
3	I love the gradient work with the colors in the background. 	1	2
7	Wow! Your use of perspective is mind blowing! 	5	1
11	This is wonderful!	5	3
17	Love the blue hues!	1	3
20	Wow! I love the contrast between the roughness of the marble sculpture and the soft leaves within nature.	9	3
4	It's cool to see you trying out a new technique!	\N	2
6	Very relaxing. 	\N	2
5	Great work! Interesting composition!	\N	2
19	This is amazing! I love your use of color!	\N	3
21	This is so beautiful. Keep up the good work.	9	1
22	This is incredible! I love your use of detail.	18	1
23	Wow! I am blown away by your digital artistry.	19	1
24	This reminds me of The Hobbit!	20	1
25	This is awesome! Keep up the good work.	18	2
26	This is amazing! I love your style.	19	2
27	Your creativity is amazing!	20	2
70	I love how balanced this is.	5	4
71	I love how peaceful this is!	1	4
72	Nice! I love your work. 	9	4
73	Wow. This looks and feels like 	18	4
74	Wow. This looks and feels like I'm in a dream. Wonderful use of detail.	18	4
75	Absolutely incredible!	19	4
76	So creative! I also love your use of texture and color.	20	4
78	This is so creative! 	35	2
79	Wow. I love the contrast in color here.	36	2
80	This is awesome!	33	1
81	This piece feels ethereal. I love how soft and coordinated your color scheme is!	35	1
82	I absolutely love how you utilized color theory in this piece!	36	1
83	Great work. I absolutely love how you combined multiple mediums in order to play with the texture of the piece as a whole.	33	3
84	This is incredible! It's cool to watch you incorporate more colors into your work.	36	3
77	Woah! This is so creative I love your use of ink technique along with the watercolor in the background.	33	2
\.


--
-- Data for Name: images; Type: TABLE DATA; Schema: public; Owner: carolinesitter
--

COPY public.images (image_id, artist_collection_id, user_id, image_title, image_link, date_uploaded) FROM stdin;
5	5	2	Two Worlds	https://res.cloudinary.com/dgvuwdtnb/image/upload/v1651879424/udxgkfi0tx5kblzzj63u.jpg	2022-05-06 18:23:44.557263
1	1	1	In the Blue	https://res.cloudinary.com/dgvuwdtnb/image/upload/v1651877825/aod5itropftiv0kqhobw.jpg	2022-05-06 17:57:04.801126
33	50	4	Existential Fears	https://res.cloudinary.com/dgvuwdtnb/image/upload/v1652737030/kmnb63llga7ku1kycihp.jpg	2022-05-16 16:37:09.382284
35	51	4	Sea Shadows	https://res.cloudinary.com/dgvuwdtnb/image/upload/v1652737537/smlogirsatrghpqujmn6.jpg	2022-05-16 16:45:37.238305
36	51	4	On the Reef	https://res.cloudinary.com/dgvuwdtnb/image/upload/v1652737602/vdzp5ogbnzglsnwfjg05.jpg	2022-05-16 16:46:41.679242
9	5	2	Comfort in Stone	https://res.cloudinary.com/dgvuwdtnb/image/upload/v1652320023/ofhje2unq5zvnftaqvxc.jpg	2022-05-11 20:47:03.154045
18	47	3	Wizard Bark	https://res.cloudinary.com/dgvuwdtnb/image/upload/v1652641500/nbdqw8cznfyi9fmziy5m.jpg	2022-05-15 14:05:00.343262
19	47	3	Tree Trunks and Spells	https://res.cloudinary.com/dgvuwdtnb/image/upload/v1652641573/knv0tqdndxk7mjehtoqq.jpg	2022-05-15 14:06:12.992433
20	48	3	Frog Hair	https://res.cloudinary.com/dgvuwdtnb/image/upload/v1652641725/ipufgffl7xskuppjiabk.jpg	2022-05-15 14:08:44.705728
\.


--
-- Data for Name: likes; Type: TABLE DATA; Schema: public; Owner: carolinesitter
--

COPY public.likes (like_id, image_id, user_id) FROM stdin;
7	5	1
8	1	1
9	1	1
14	1	2
15	5	2
17	5	3
27	1	3
28	5	3
30	9	3
31	9	3
32	9	3
33	19	3
34	19	3
35	19	3
36	18	3
38	20	3
39	20	3
2	\N	1
4	\N	2
16	\N	3
18	\N	3
25	\N	3
6	\N	2
10	\N	1
5	\N	2
26	\N	3
40	9	1
41	18	1
42	19	1
43	20	1
44	18	2
45	19	2
46	20	2
47	1	1
48	33	4
49	33	4
50	33	4
51	36	2
52	36	2
53	33	2
54	36	2
55	35	2
56	35	2
57	35	2
58	33	1
59	35	1
60	36	1
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: carolinesitter
--

COPY public.users (user_id, first_name, last_name, email, username, password, instagram, twitter, tiktok, website, zipcode) FROM stdin;
1	Vanessa	Lloyd	vanessalloyd@gmail.com	vlloyd13	password	@vanessa_lloyd	@vanessalloyd	@vlloyd	www.vanessalloyd.com	78701
2	John	Silverstone	silverstoneworks@gmail.com	silverstoneworks	password	@silverstoneart	@johnsilverstone	@silverstone	www.silverstoneworks.com	78733
3	Alice	Graham	alicegraham@gmail.com	alicedraws	password	@alicedraws	@alicegraham	@alice_draws	www.artbyalice.com	78701
4	Robert	Ford	robertford@gmail.com	robford	password	@robertford	@robert-ford	@art_by_ford	www.ArtbyFord.com	78721
\.


--
-- Name: artist_collections_artist_collection_id_seq; Type: SEQUENCE SET; Schema: public; Owner: carolinesitter
--

SELECT pg_catalog.setval('public.artist_collections_artist_collection_id_seq', 51, true);


--
-- Name: comment_comment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: carolinesitter
--

SELECT pg_catalog.setval('public.comment_comment_id_seq', 84, true);


--
-- Name: images_image_id_seq; Type: SEQUENCE SET; Schema: public; Owner: carolinesitter
--

SELECT pg_catalog.setval('public.images_image_id_seq', 37, true);


--
-- Name: likes_like_id_seq; Type: SEQUENCE SET; Schema: public; Owner: carolinesitter
--

SELECT pg_catalog.setval('public.likes_like_id_seq', 60, true);


--
-- Name: users_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: carolinesitter
--

SELECT pg_catalog.setval('public.users_user_id_seq', 4, true);


--
-- Name: artist_collections artist_collections_pkey; Type: CONSTRAINT; Schema: public; Owner: carolinesitter
--

ALTER TABLE ONLY public.artist_collections
    ADD CONSTRAINT artist_collections_pkey PRIMARY KEY (artist_collection_id);


--
-- Name: comment comment_pkey; Type: CONSTRAINT; Schema: public; Owner: carolinesitter
--

ALTER TABLE ONLY public.comment
    ADD CONSTRAINT comment_pkey PRIMARY KEY (comment_id);


--
-- Name: images images_pkey; Type: CONSTRAINT; Schema: public; Owner: carolinesitter
--

ALTER TABLE ONLY public.images
    ADD CONSTRAINT images_pkey PRIMARY KEY (image_id);


--
-- Name: likes likes_pkey; Type: CONSTRAINT; Schema: public; Owner: carolinesitter
--

ALTER TABLE ONLY public.likes
    ADD CONSTRAINT likes_pkey PRIMARY KEY (like_id);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: carolinesitter
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: carolinesitter
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: carolinesitter
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- Name: users users_website_key; Type: CONSTRAINT; Schema: public; Owner: carolinesitter
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_website_key UNIQUE (website);


--
-- Name: artist_collections artist_collections_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: carolinesitter
--

ALTER TABLE ONLY public.artist_collections
    ADD CONSTRAINT artist_collections_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- Name: comment comment_image_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: carolinesitter
--

ALTER TABLE ONLY public.comment
    ADD CONSTRAINT comment_image_id_fkey FOREIGN KEY (image_id) REFERENCES public.images(image_id);


--
-- Name: comment comment_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: carolinesitter
--

ALTER TABLE ONLY public.comment
    ADD CONSTRAINT comment_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- Name: images images_artist_collection_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: carolinesitter
--

ALTER TABLE ONLY public.images
    ADD CONSTRAINT images_artist_collection_id_fkey FOREIGN KEY (artist_collection_id) REFERENCES public.artist_collections(artist_collection_id);


--
-- Name: images images_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: carolinesitter
--

ALTER TABLE ONLY public.images
    ADD CONSTRAINT images_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- Name: likes likes_image_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: carolinesitter
--

ALTER TABLE ONLY public.likes
    ADD CONSTRAINT likes_image_id_fkey FOREIGN KEY (image_id) REFERENCES public.images(image_id);


--
-- Name: likes likes_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: carolinesitter
--

ALTER TABLE ONLY public.likes
    ADD CONSTRAINT likes_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- PostgreSQL database dump complete
--

