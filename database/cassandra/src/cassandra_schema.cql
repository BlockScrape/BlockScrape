DROP KEYSPACE IF EXISTS blockscrape;

CREATE KEYSPACE blockscrape WITH replication = {
  'class': 'SimpleStrategy',
  'replication_factor': 3
};

USE blockscrape;

CREATE TABLE user_data (
  username text PRIMARY KEY,
  first_name text,
  last_name text,
  email text,
  passwd text,
  birthdate date
);

CREATE TABLE order_list (
  uuid uuid PRIMARY KEY,
  u_username uuid,
  name text,
  url text,
  start_timestamp int,
  repetitions int,
  intervall int
);

CREATE TABLE data (
  uuid uuid PRIMARY KEY,
  a_uuid uuid,
  u_username text,
  scraping_username text,
  data text
);