-- This script was generated by a beta version of the ERD tool in pgAdmin 4.
-- Please log an issue at https://redmine.postgresql.org/projects/pgadmin4/issues/new if you find any bugs, including reproduction steps.
BEGIN;


CREATE TABLE IF NOT EXISTS public."raportRow"
(
    "ID_" serial NOT NULL,
    ssl boolean,
    "ID_server_app" integer,
    "ID_server_rdb" integer,
    data_start text,
    retention boolean,
    users_in_rdb integer,
    blind_rdb_host boolean,
    test_time integer,
    "FULL_TEST_ID" integer,
    "TEST_ID" integer,
    "ONE_APP_ID" integer,
    "PROPORTION" text,
    PRIMARY KEY ("ID_")
)
WITH (
    OIDS = FALSE
);

CREATE TABLE IF NOT EXISTS public."MV_APP"
(
    "ID_" serial NOT NULL,
    "CPU" text,
    "RAM" text,
    "SIZE" text,
    "IOPS" text,
    platform text,
    host text,
    PRIMARY KEY ("ID_")
)
WITH (
    OIDS = FALSE
);

CREATE TABLE IF NOT EXISTS public."MV_RDB"
(
    "ID_" serial NOT NULL,
    "CPU" text,
    "RAM" text,
    "SIZE" text,
    "IOPS" text,
    platform text,
    host text,
    PRIMARY KEY ("ID_")
)
WITH (
    OIDS = FALSE
);

CREATE TABLE IF NOT EXISTS public."FULLTESTS"
(
    "ID_" serial NOT NULL,
    name text,
    PRIMARY KEY ("ID_")
)
WITH (
    OIDS = FALSE
);

CREATE TABLE IF NOT EXISTS public."ID_TEST"
(
    "ID_" serial NOT NULL,
    name text,
    "ID_FULL_TEST" integer,
    PRIMARY KEY ("ID_")
)
WITH (
    OIDS = FALSE
);

CREATE TABLE IF NOT EXISTS public."MODE"
(
    "ID_" serial NOT NULL,
    name text,
    host text,
    port text,
    "ID_TEST" integer,
    PRIMARY KEY ("ID_")
)
WITH (
    OIDS = FALSE
);

ALTER TABLE IF EXISTS public."MODE"
    ADD FOREIGN KEY ("ID_TEST")
    REFERENCES public."ID_TEST" ("ID_")
    NOT VALID;


ALTER TABLE IF EXISTS public."raportRow"
    ADD FOREIGN KEY ("ID_server_app")
    REFERENCES public."MV_APP" ("ID_")
    NOT VALID;


ALTER TABLE IF EXISTS public."raportRow"
    ADD FOREIGN KEY ("FULL_TEST_ID")
    REFERENCES public."FULLTESTS" ("ID_")
    NOT VALID;


ALTER TABLE IF EXISTS public."raportRow"
    ADD FOREIGN KEY ("TEST_ID")
    REFERENCES public."ID_TEST" ("ID_")
    NOT VALID;


ALTER TABLE IF EXISTS public."raportRow"
    ADD FOREIGN KEY ("ONE_APP_ID")
    REFERENCES public."MODE" ("ID_")
    NOT VALID;


ALTER TABLE IF EXISTS public."raportRow"
    ADD FOREIGN KEY ("ID_server_rdb")
    REFERENCES public."MV_RDB" ("ID_")
    NOT VALID;

END;