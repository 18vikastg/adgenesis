-- Migration: Initial Schema
-- Version: 001
-- Date: 2025-11-30
-- Description: Create initial database schema for ADGENESIS

-- This migration creates the foundational tables for the ADGENESIS platform

BEGIN;

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255),
    name VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Designs table
CREATE TABLE IF NOT EXISTS designs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    prompt TEXT NOT NULL,
    platform VARCHAR(50) NOT NULL,
    format VARCHAR(50) NOT NULL,
    canvas_data JSONB,
    preview_url VARCHAR(500),
    s3_key VARCHAR(500),
    is_compliant INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Guidelines table
CREATE TABLE IF NOT EXISTS guidelines (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    file_url VARCHAR(500),
    s3_key VARCHAR(500),
    extracted_data JSONB,
    colors JSONB,
    fonts JSONB,
    logo_urls JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Exports table
CREATE TABLE IF NOT EXISTS exports (
    id SERIAL PRIMARY KEY,
    design_id INTEGER REFERENCES designs(id) ON DELETE CASCADE,
    format VARCHAR(10) NOT NULL,
    file_url VARCHAR(500),
    s3_key VARCHAR(500),
    file_size INTEGER,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Compliance logs table
CREATE TABLE IF NOT EXISTS compliance_logs (
    id SERIAL PRIMARY KEY,
    design_id INTEGER REFERENCES designs(id) ON DELETE CASCADE,
    platform VARCHAR(50) NOT NULL,
    is_compliant INTEGER NOT NULL,
    issues JSONB,
    checked_at TIMESTAMP DEFAULT NOW()
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_users_user_id ON users(user_id);
CREATE INDEX IF NOT EXISTS idx_designs_user_id ON designs(user_id);
CREATE INDEX IF NOT EXISTS idx_designs_platform ON designs(platform);
CREATE INDEX IF NOT EXISTS idx_designs_created_at ON designs(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_guidelines_user_id ON guidelines(user_id);
CREATE INDEX IF NOT EXISTS idx_exports_design_id ON exports(design_id);
CREATE INDEX IF NOT EXISTS idx_compliance_logs_design_id ON compliance_logs(design_id);

-- Insert demo user
INSERT INTO users (user_id, email, name) 
VALUES ('demo-user-001', 'demo@adgenesis.ai', 'Demo User')
ON CONFLICT (user_id) DO NOTHING;

COMMIT;
