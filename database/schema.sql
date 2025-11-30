-- ADGENESIS Database Schema
-- PostgreSQL Schema for Supabase

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255),
    name VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create index on user_id for faster lookups
CREATE INDEX idx_users_user_id ON users(user_id);

-- Designs table
CREATE TABLE designs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    prompt TEXT NOT NULL,
    platform VARCHAR(50) NOT NULL CHECK (platform IN ('meta', 'google', 'linkedin')),
    format VARCHAR(50) NOT NULL CHECK (format IN ('square', 'landscape', 'portrait', 'story')),
    canvas_data JSONB,
    preview_url VARCHAR(500),
    s3_key VARCHAR(500),
    is_compliant INTEGER DEFAULT 0 CHECK (is_compliant IN (-1, 0, 1)),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Create indexes for designs
CREATE INDEX idx_designs_user_id ON designs(user_id);
CREATE INDEX idx_designs_platform ON designs(platform);
CREATE INDEX idx_designs_created_at ON designs(created_at DESC);

-- Guidelines table
CREATE TABLE guidelines (
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

-- Create indexes for guidelines
CREATE INDEX idx_guidelines_user_id ON guidelines(user_id);
CREATE INDEX idx_guidelines_created_at ON guidelines(created_at DESC);

-- Exports table
CREATE TABLE exports (
    id SERIAL PRIMARY KEY,
    design_id INTEGER REFERENCES designs(id) ON DELETE CASCADE,
    format VARCHAR(10) NOT NULL CHECK (format IN ('png', 'jpg', 'svg', 'pdf')),
    file_url VARCHAR(500),
    s3_key VARCHAR(500),
    file_size INTEGER,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create indexes for exports
CREATE INDEX idx_exports_design_id ON exports(design_id);
CREATE INDEX idx_exports_created_at ON exports(created_at DESC);

-- Compliance logs table
CREATE TABLE compliance_logs (
    id SERIAL PRIMARY KEY,
    design_id INTEGER REFERENCES designs(id) ON DELETE CASCADE,
    platform VARCHAR(50) NOT NULL CHECK (platform IN ('meta', 'google', 'linkedin')),
    is_compliant INTEGER NOT NULL CHECK (is_compliant IN (0, 1)),
    issues JSONB,
    checked_at TIMESTAMP DEFAULT NOW()
);

-- Create indexes for compliance_logs
CREATE INDEX idx_compliance_logs_design_id ON compliance_logs(design_id);
CREATE INDEX idx_compliance_logs_platform ON compliance_logs(platform);
CREATE INDEX idx_compliance_logs_checked_at ON compliance_logs(checked_at DESC);

-- Insert demo user for hackathon
INSERT INTO users (user_id, email, name) 
VALUES ('demo-user-001', 'demo@adgenesis.ai', 'Demo User')
ON CONFLICT (user_id) DO NOTHING;

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create trigger for designs updated_at
CREATE TRIGGER update_designs_updated_at
    BEFORE UPDATE ON designs
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Comments for documentation
COMMENT ON TABLE users IS 'User accounts (simplified for hackathon - no auth)';
COMMENT ON TABLE designs IS 'Generated ad designs with AI-created content';
COMMENT ON TABLE guidelines IS 'Uploaded brand guidelines with extracted data';
COMMENT ON TABLE exports IS 'Exported design files in various formats';
COMMENT ON TABLE compliance_logs IS 'Platform compliance check results';

COMMENT ON COLUMN designs.is_compliant IS '0: not checked, 1: compliant, -1: non-compliant';
COMMENT ON COLUMN designs.canvas_data IS 'Fabric.js canvas JSON data';
COMMENT ON COLUMN guidelines.extracted_data IS 'AI-extracted brand elements (colors, fonts, logos)';
COMMENT ON COLUMN compliance_logs.issues IS 'JSON array of compliance issues';
