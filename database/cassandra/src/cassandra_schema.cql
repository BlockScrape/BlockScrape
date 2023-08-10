
CREATE KEYSPACE IF NOT EXISTS blockscrape WITH replication = {
  'class': 'SimpleStrategy',
  'replication_factor': 3
};

USE blockscrape;

CREATE TABLE IF NOT EXISTS user_data (
  username text PRIMARY KEY,
  first_name text,
  last_name text,
  email text,
  passwd text,
  birthdate date
);

CREATE TABLE IF NOT EXISTS order_list (
  uuid uuid PRIMARY KEY,
  creator_username text,
  name text,
  scraping_url text,
  request_method text,
  request_header text,
  request_body text,
  start_timestamp int,
  next_scrape int,
  last_updated int,
  repetitions int,
  intervall int,
  finished boolean
);
