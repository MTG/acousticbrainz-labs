#!/bin/sh

# Create the database
psql -U postgres < create-db.sql

# Create the tables
psql -U acousticbrainz abdata < create-tables.sql
