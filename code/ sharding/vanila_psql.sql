-- Enable the necessary extensions
CREATE EXTENSION IF NOT EXISTS postgres_fdw;

-- Create servers for each shard
CREATE SERVER shard1 FOREIGN DATA WRAPPER postgres_fdw OPTIONS (host 'shard1_host', dbname 'your_db', port '5432');
CREATE SERVER shard2 FOREIGN DATA WRAPPER postgres_fdw OPTIONS (host 'shard2_host', dbname 'your_db', port '5432');
CREATE SERVER shard3 FOREIGN DATA WRAPPER postgres_fdw OPTIONS (host 'shard3_host', dbname 'your_db', port '5432');

-- Create user mappings for each shard
CREATE USER MAPPING FOR postgres SERVER shard1 OPTIONS (user 'your_user', password 'your_password');
CREATE USER MAPPING FOR postgres SERVER shard2 OPTIONS (user 'your_user', password 'your_password');
CREATE USER MAPPING FOR postgres SERVER shard3 OPTIONS (user 'your_user', password 'your_password');

-- Create foreign tables on each shard
CREATE FOREIGN TABLE news_shard1 (
    id SERIAL PRIMARY KEY,
    category_id INT,
    title TEXT,
    content TEXT
) SERVER shard1 OPTIONS (table_name 'news');

CREATE FOREIGN TABLE news_shard2 (
    id SERIAL PRIMARY KEY,
    category_id INT,
    title TEXT,
    content TEXT
) SERVER shard2 OPTIONS (table_name 'news');

CREATE FOREIGN TABLE news_shard3 (
    id SERIAL PRIMARY KEY,
    category_id INT,
    title TEXT,
    content TEXT
) SERVER shard3 OPTIONS (table_name 'news');

-- Create a main table using a VIEW to combine data from all shards
CREATE VIEW news AS
SELECT * FROM news_shard1
UNION ALL
SELECT * FROM news_shard2
UNION ALL
SELECT * FROM news_shard3;

-- Insert data into the news view (data will be distributed across shards)
INSERT INTO news (category_id, title, content) VALUES (1, 'Title 1', 'Content 1');
INSERT INTO news (category_id, title, content) VALUES (2, 'Title 2', 'Content 2');
INSERT INTO news (category_id, title, content) VALUES (3, 'Title 3', 'Content 3');
