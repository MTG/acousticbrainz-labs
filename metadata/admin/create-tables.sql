BEGIN;

-- tables

CREATE TABLE lastfm (
    id SERIAL,
    mbid uuid NOT NULL,
    data json NOT NULL,
    added timestamp with time zone DEFAULT now(),
    indexed timestamp with time zone
);


CREATE TABLE tempo (
    id SERIAL,
    mbid uuid NOT NULL,
    data json NOT NULL,
    added timestamp with time zone DEFAULT now(),
    indexed timestamp with time zone
);

-- primary keys

ALTER TABLE lastfm ADD CONSTRAINT lastfm_pkey PRIMARY KEY (id);
ALTER TABLE tempo ADD CONSTRAINT tempo_pkey PRIMARY KEY (id);

-- indexes

CREATE INDEX added_ndx_lastfm ON lastfm USING btree (added);
CREATE INDEX added_ndx_tempo ON tempo USING btree (added);
CREATE INDEX indexed_ndx_lastfm ON lastfm USING btree (indexed);
CREATE INDEX indexed_ndx_tempo ON tempo USING btree (indexed);
CREATE INDEX mbid_ndx_lastfm ON lastfm USING btree (mbid);
CREATE INDEX mbid_ndx_tempo ON tempo USING btree (mbid);

COMMIT;
