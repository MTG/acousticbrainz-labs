\set ON_ERROR_STOP 1

-- Create the user and the database. Must run as user postgres.

CREATE DATABASE abdata WITH OWNER = acousticbrainz TEMPLATE template0 ENCODING = 'UNICODE';
