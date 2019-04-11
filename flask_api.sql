--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.14
-- Dumped by pg_dump version 9.5.14

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO admin;

--
-- Name: authors; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.authors (
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    id integer NOT NULL,
    name character varying(256) NOT NULL
);


ALTER TABLE public.authors OWNER TO admin;

--
-- Name: authors_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.authors_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.authors_id_seq OWNER TO admin;

--
-- Name: authors_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.authors_id_seq OWNED BY public.authors.id;


--
-- Name: books; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.books (
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    id integer NOT NULL,
    author_id integer,
    publisher_id integer,
    category_id integer,
    title character varying(256),
    price integer
);


ALTER TABLE public.books OWNER TO admin;

--
-- Name: books_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.books_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.books_id_seq OWNER TO admin;

--
-- Name: books_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.books_id_seq OWNED BY public.books.id;


--
-- Name: categories; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.categories (
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    id integer NOT NULL,
    name character varying(256) NOT NULL
);


ALTER TABLE public.categories OWNER TO admin;

--
-- Name: categories_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.categories_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.categories_id_seq OWNER TO admin;

--
-- Name: categories_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.categories_id_seq OWNED BY public.categories.id;


--
-- Name: order_items; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.order_items (
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    id integer NOT NULL,
    order_id integer,
    quantity integer,
    total_price integer,
    book_id integer
);


ALTER TABLE public.order_items OWNER TO admin;

--
-- Name: order_items_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.order_items_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.order_items_id_seq OWNER TO admin;

--
-- Name: order_items_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.order_items_id_seq OWNED BY public.order_items.id;


--
-- Name: orders; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.orders (
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    id integer NOT NULL,
    user_id integer,
    total_price integer
);


ALTER TABLE public.orders OWNER TO admin;

--
-- Name: orders_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.orders_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.orders_id_seq OWNER TO admin;

--
-- Name: orders_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.orders_id_seq OWNED BY public.orders.id;


--
-- Name: publishers; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.publishers (
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    id integer NOT NULL,
    name character varying(256) NOT NULL
);


ALTER TABLE public.publishers OWNER TO admin;

--
-- Name: publishers_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.publishers_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.publishers_id_seq OWNER TO admin;

--
-- Name: publishers_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.publishers_id_seq OWNED BY public.publishers.id;


--
-- Name: reviews; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.reviews (
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    id integer NOT NULL,
    book_id integer,
    user_id integer,
    rate integer,
    title character varying(256),
    comment text
);


ALTER TABLE public.reviews OWNER TO admin;

--
-- Name: reviews_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.reviews_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.reviews_id_seq OWNER TO admin;

--
-- Name: reviews_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.reviews_id_seq OWNED BY public.reviews.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id integer NOT NULL,
    username text NOT NULL,
    password text NOT NULL,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.authors ALTER COLUMN id SET DEFAULT nextval('public.authors_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.books ALTER COLUMN id SET DEFAULT nextval('public.books_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.categories ALTER COLUMN id SET DEFAULT nextval('public.categories_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.order_items ALTER COLUMN id SET DEFAULT nextval('public.order_items_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.orders ALTER COLUMN id SET DEFAULT nextval('public.orders_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.publishers ALTER COLUMN id SET DEFAULT nextval('public.publishers_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.reviews ALTER COLUMN id SET DEFAULT nextval('public.reviews_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.alembic_version (version_num) FROM stdin;
a77d3b164aee
\.


--
-- Data for Name: authors; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.authors (created_at, updated_at, id, name) FROM stdin;
2019-04-09 08:15:05.288686	2019-04-09 08:15:05.288686	1	Rosie Nguyễn
2019-04-09 08:55:09.301446	2019-04-09 08:55:09.301446	2	Vãn Tình
2019-04-10 04:42:47.919694	2019-04-10 04:42:47.919694	3	Du Phong
2019-04-10 04:43:47.044583	2019-04-10 04:43:47.044583	4	Paulo Coelho
2019-04-10 04:44:40.843829	2019-04-10 04:44:40.843829	5	Hae Min
2019-04-10 04:46:10.287368	2019-04-10 04:46:10.287368	6	Marty Neumeier
2019-04-10 04:48:43.287818	2019-04-10 04:48:43.287818	7	TS. David J. Lieberman
2019-04-10 04:49:22.484324	2019-04-10 04:49:22.484324	8	Robin Sharma
2019-04-10 04:51:17.927687	2019-04-10 04:51:17.927687	9	Nguyễn Nhật Ánh
2019-04-10 04:52:02.498556	2019-04-10 04:52:02.498556	10	Sam McBratney
2019-04-10 04:53:40.383594	2019-04-10 04:53:40.383594	11	Baird T. Spalding
2019-04-10 04:56:14.629223	2019-04-10 04:56:14.629223	12	Nguyễn Văn Hiệp
\.


--
-- Name: authors_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.authors_id_seq', 12, true);


--
-- Data for Name: books; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.books (created_at, updated_at, id, author_id, publisher_id, category_id, title, price) FROM stdin;
2019-04-09 08:55:09.328583	2019-04-09 08:55:09.328583	3	2	2	1	Khí Chất Bao Nhiêu, Hạnh Phúc Bấy Nhiêu	77350
2019-04-09 08:48:45.698566	2019-04-09 09:24:33.166743	1	1	1	1	Tuổi Trẻ Đáng Giá Bao Nhiêu	49000
2019-04-10 04:42:47.948375	2019-04-10 04:42:47.948375	4	3	3	2	Thanh Xuân Không Hối Tiếc	52000
2019-04-10 04:43:47.075538	2019-04-10 04:43:47.075538	5	4	4	2	Nhà Giả Kim	47300
2019-04-10 04:44:40.852038	2019-04-10 04:44:40.852038	6	5	4	2	Bước Chậm Lại Giữa Thế Gian Vội Vã (Tái Bản)	59500
2019-04-10 04:46:10.316765	2019-04-10 04:46:10.316765	7	6	2	3	Khoảng Cách	69300
2019-04-10 04:48:43.310436	2019-04-10 04:48:43.310436	8	7	5	4	Đọc Vị Bất Kỳ Ai (Tái Bản)	46920
2019-04-10 04:49:22.512808	2019-04-10 04:49:22.512808	9	8	6	3	Nhà Lãnh Đạo Không Chức Danh	44000
2019-04-10 04:51:17.966881	2019-04-10 04:51:17.966881	10	9	6	5	Có Hai Con Mèo Ngồi Bên Cửa Sổ	46750
2019-04-10 04:52:02.508012	2019-04-10 04:52:02.508012	11	10	1	5	Con Yêu Bố Chừng Nào	31500
2019-04-10 04:53:40.399336	2019-04-10 04:53:40.399336	12	11	7	6	Hành Trình Về Phương Đông (Tái Bản)	31500
2019-04-10 04:56:14.656519	2019-04-10 04:56:14.656519	13	12	8	7	"Hack" Não 1500 Từ Tiếng Anh	400000
2019-04-10 04:58:33.410081	2019-04-10 04:58:33.410081	14	9	6	2	Cô Gái Đến Từ Hôm Qua	52000
2019-04-10 04:59:21.428084	2019-04-10 04:59:21.428084	15	9	6	2	Tôi Thấy Hoa Vàng Trên Cỏ Xanh	79990
\.


--
-- Name: books_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.books_id_seq', 15, true);


--
-- Data for Name: categories; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.categories (created_at, updated_at, id, name) FROM stdin;
2019-04-09 08:26:54.64804	2019-04-09 08:26:54.64804	1	Sách kỹ năng sống
2019-04-10 04:42:47.942218	2019-04-10 04:42:47.942218	2	Sách văn học
2019-04-10 04:46:10.296676	2019-04-10 04:46:10.296676	3	Sách kinh tế
2019-04-10 04:48:43.303735	2019-04-10 04:48:43.303735	4	Sách kỹ năng làm việc
2019-04-10 04:51:17.9476	2019-04-10 04:51:17.9476	5	Sách thiếu nhi
2019-04-10 04:53:40.39481	2019-04-10 04:53:40.39481	6	Sách tôn giáo - tâm linh
2019-04-10 04:56:14.650531	2019-04-10 04:56:14.650531	7	Sách học ngoại ngữ
\.


--
-- Name: categories_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.categories_id_seq', 7, true);


--
-- Data for Name: order_items; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.order_items (created_at, updated_at, id, order_id, quantity, total_price, book_id) FROM stdin;
2019-04-10 08:23:11.197072	2019-04-10 08:23:11.197072	1	1	2	159980	15
2019-04-10 08:23:11.197072	2019-04-10 08:23:11.197072	2	1	1	59500	6
2019-04-10 09:02:19.81156	2019-04-10 09:02:19.81156	9	5	1	52000	4
2019-04-10 09:04:07.294853	2019-04-10 09:04:07.294853	10	6	1	47300	5
2019-04-10 09:04:07.294853	2019-04-10 09:04:07.294853	11	6	1	46920	8
\.


--
-- Name: order_items_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.order_items_id_seq', 11, true);


--
-- Data for Name: orders; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.orders (created_at, updated_at, id, user_id, total_price) FROM stdin;
2019-04-10 08:23:11.197072	2019-04-10 08:23:11.197072	1	1	219480
2019-04-10 09:02:19.81156	2019-04-10 09:02:19.81156	5	3	52000
2019-04-10 09:04:07.294853	2019-04-10 09:04:07.294853	6	2	94220
\.


--
-- Name: orders_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.orders_id_seq', 6, true);


--
-- Data for Name: publishers; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.publishers (created_at, updated_at, id, name) FROM stdin;
2019-04-09 08:25:43.976954	2019-04-09 08:25:43.976954	1	Nhà Xuất Bản Hội Nhà Văn
2019-04-09 08:55:09.321608	2019-04-09 08:55:09.321608	2	Nhà Xuất Bản Thế Giới
2019-04-10 04:42:47.934321	2019-04-10 04:42:47.934321	3	Nhà Xuất Bản Văn Hóa - Văn Nghệ
2019-04-10 04:43:47.071676	2019-04-10 04:43:47.071676	4	Nhà Xuất Bản Văn Học
2019-04-10 04:48:43.298438	2019-04-10 04:48:43.298438	5	Nhà Xuất Bản Lao Động
2019-04-10 04:49:22.509211	2019-04-10 04:49:22.509211	6	Nhà Xuất Bản Trẻ
2019-04-10 04:53:40.391667	2019-04-10 04:53:40.391667	7	Nhà Xuất Bản Hồng Đức
2019-04-10 04:56:14.645277	2019-04-10 04:56:14.645277	8	Nhà Xuất Bản Lao Động Xã Hội
\.


--
-- Name: publishers_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.publishers_id_seq', 8, true);


--
-- Data for Name: reviews; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.reviews (created_at, updated_at, id, book_id, user_id, rate, title, comment) FROM stdin;
2019-04-09 10:42:27.52469	2019-04-09 10:42:27.52469	1	1	1	5	Sách hay	Bìa cứng, chất lượng in tốt, nội dung sâu sắc
2019-04-10 06:30:27.121143	2019-04-10 06:30:27.121143	2	15	1	5	Good!	Sách mới 100%...rất đẹp. Tiki giao hàng rất nhanh....nói chung ok
2019-04-10 06:57:43.468089	2019-04-10 06:57:43.468089	3	15	3	5	Cuốn Sách Tuyệt Vời, Ấn Bản Mới Nóng Hổi	Bản in mới nhất của NXB Trẻ trong cuối năm 2018 và đầu 2019. Thay bìa mới nhất và bọc seal nguyên tem nxb xịn luôn. Các bạn nhanh tay số lượng cực kỳ có hạn nhé. ^^
2019-04-10 07:00:27.149207	2019-04-10 07:00:27.149207	4	3	4	3	Dịch Vụ Tiki Tạm Ổn - Sản Phẩm Tạm Ổn - Nội Dung Hay Khỏi Bàn	Thời gian giao hàng: Mình đặt mua lúc vừa hết Tết. Vì lí do này mà thời gian giao hàng của Tiki chậm mất 3-4 ngày so với ngày dự kiến dự kiến. Sản phẩm: Có vài vết bẩn (đen đen) ở cạnh góc sách. Mình nghĩ do vấn đề lưu trữ sản phẩm tại kho. Nội dung: Đọc sẽ bị ghiền đấy.
2019-04-10 07:01:13.18268	2019-04-10 07:01:13.18268	5	3	5	5	Cực Kì Hài Lòng	Sách đẹp và ý nghĩa lắm. Mua không tiếc tiền đâu mọi người
2019-04-10 07:02:29.431361	2019-04-10 07:02:29.431361	6	3	6	4	Hài Lòng	Sách hay, thực tế, tiki giao hàng rất nhanh,mình mua đợt chưa sinh nhật tiki nên giá mắc hơn một chút, mua nhiều thể loại 6 cuốn, tất cả đều mới không bị cũ hay rách, đóng gói cẩn thận
2019-04-11 03:28:29.824534	2019-04-11 03:28:29.824534	7	3	7	3	Tiki Cần Cẩn Thận Hơn	Nội dung sách hay . Ý nghĩa . Đã có đủ hai cuốn của Vãn Tình và nội dung k chê đc . Nhg mà ..... Góc sách bị cong . Bìa bên ngoài còn hơi bị bẩn nữa . Mong tiki lm việc cẩn thận hơn. mấy cuốn sách mk mua trong đơn hàng toàn bị cong góc sách vs hơi bẩn nữa . Nhìn rất xót
\.


--
-- Name: reviews_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.reviews_id_seq', 7, true);


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, username, password, created_at, updated_at) FROM stdin;
1	minhhuu	123456	\N	\N
2	vovanphong	123456	2019-04-10 06:14:14.517724	2019-04-10 06:14:14.517724
3	vynguyen	123456	2019-04-10 06:57:26.334901	2019-04-10 06:57:26.334901
4	phungtram	123456	2019-04-10 06:59:18.77592	2019-04-10 06:59:18.77592
5	lenhi	123456	2019-04-10 07:00:43.812389	2019-04-10 07:00:43.812389
6	nguyenledung	123456	2019-04-10 07:02:16.725868	2019-04-10 07:02:16.725868
7	phamthuhien	123456	2019-04-11 03:28:19.523767	2019-04-11 03:28:19.523767
\.


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 7, true);


--
-- Name: alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: authors_name_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.authors
    ADD CONSTRAINT authors_name_key UNIQUE (name);


--
-- Name: authors_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.authors
    ADD CONSTRAINT authors_pkey PRIMARY KEY (id);


--
-- Name: books_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.books
    ADD CONSTRAINT books_pkey PRIMARY KEY (id);


--
-- Name: categories_name_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.categories
    ADD CONSTRAINT categories_name_key UNIQUE (name);


--
-- Name: categories_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.categories
    ADD CONSTRAINT categories_pkey PRIMARY KEY (id);


--
-- Name: order_items_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.order_items
    ADD CONSTRAINT order_items_pkey PRIMARY KEY (id);


--
-- Name: orders_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_pkey PRIMARY KEY (id);


--
-- Name: publishers_name_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.publishers
    ADD CONSTRAINT publishers_name_key UNIQUE (name);


--
-- Name: publishers_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.publishers
    ADD CONSTRAINT publishers_pkey PRIMARY KEY (id);


--
-- Name: reviews_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.reviews
    ADD CONSTRAINT reviews_pkey PRIMARY KEY (id);


--
-- Name: users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- Name: books_author_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.books
    ADD CONSTRAINT books_author_id_fkey FOREIGN KEY (author_id) REFERENCES public.authors(id);


--
-- Name: books_category_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.books
    ADD CONSTRAINT books_category_id_fkey FOREIGN KEY (category_id) REFERENCES public.categories(id);


--
-- Name: books_publisher_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.books
    ADD CONSTRAINT books_publisher_id_fkey FOREIGN KEY (publisher_id) REFERENCES public.publishers(id);


--
-- Name: order_items_book_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.order_items
    ADD CONSTRAINT order_items_book_id_fkey FOREIGN KEY (book_id) REFERENCES public.books(id);


--
-- Name: order_items_order_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.order_items
    ADD CONSTRAINT order_items_order_id_fkey FOREIGN KEY (order_id) REFERENCES public.orders(id);


--
-- Name: orders_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: reviews_book_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.reviews
    ADD CONSTRAINT reviews_book_id_fkey FOREIGN KEY (book_id) REFERENCES public.books(id);


--
-- Name: reviews_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.reviews
    ADD CONSTRAINT reviews_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

