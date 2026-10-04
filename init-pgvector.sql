-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Create items table
CREATE TABLE IF NOT EXISTS items (
    id BIGSERIAL PRIMARY KEY,
    source VARCHAR(50) NOT NULL,
    url VARCHAR(2048) NOT NULL UNIQUE,
    title TEXT NOT NULL,
    published_at TIMESTAMP WITH TIME ZONE,
    category VARCHAR(50),
    summary TEXT,
    raw_content TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create embeddings table
CREATE TABLE IF NOT EXISTS embeddings (
    id BIGSERIAL PRIMARY KEY,
    item_id BIGINT NOT NULL UNIQUE REFERENCES items(id) ON DELETE CASCADE,
    embedding vector(1536),
    embedding_model VARCHAR(100) DEFAULT 'text-embedding-3-small',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create source tracking table
CREATE TABLE IF NOT EXISTS source_tracking (
    id BIGSERIAL PRIMARY KEY,
    source VARCHAR(50) NOT NULL UNIQUE,
    last_fetched_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_items_source ON items(source);
CREATE INDEX IF NOT EXISTS idx_items_category ON items(category);
CREATE INDEX IF NOT EXISTS idx_items_published_at ON items(published_at DESC);
CREATE INDEX IF NOT EXISTS idx_items_created_at ON items(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_embeddings_item_id ON embeddings(item_id);

-- Create vector index for semantic search (IVFFLAT for reasonable balance)
CREATE INDEX IF NOT EXISTS idx_embeddings_vector ON embeddings USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);
