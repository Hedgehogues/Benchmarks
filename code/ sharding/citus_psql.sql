-- Ensure that Citus is installed
CREATE EXTENSION IF NOT EXISTS citus;

-- Create a table for storing news articles
CREATE TABLE news (
    id SERIAL PRIMARY KEY,  -- Unique identifier for each article
    category_id INT,        -- Category ID for categorizing articles
    title TEXT,             -- Title of the article
    content TEXT            -- Content of the article
);

-- Distribute the table across shards based on the category_id
SELECT create_distributed_table('news', 'category_id');

-- Insert data into the distributed table
INSERT INTO news (category_id, title, content) VALUES (1, 'Title 1', 'Content 1');
INSERT INTO news (category_id, title, content) VALUES (2, 'Title 2', 'Content 2');
INSERT INTO news (category_id, title, content) VALUES (3, 'Title 3', 'Content 3');
