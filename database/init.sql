-- Create Enum Types
CREATE TYPE user_role AS ENUM ('EMERGENCY_MANAGER', 'FIRST_RESPONDER', 'FIELD_MEDIC', 'HOSPITAL_ADMIN', 'BYSTANDER');
CREATE TYPE emergency_status AS ENUM ('ACTIVE', 'ROUTED', 'RESOLVED', 'FALSE_ALARM');
CREATE TYPE resource_type AS ENUM ('AMBULANCE', 'FIRE_TRUCK', 'HELO', 'SUPPLY_DROP');

-- Audit Trigger Function
CREATE OR REPLACE FUNCTION trigger_set_timestamp()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = CURRENT_TIMESTAMP;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Tables
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    role user_role NOT NULL,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TRIGGER set_timestamp_users BEFORE UPDATE ON users FOR EACH ROW EXECUTE PROCEDURE trigger_set_timestamp();

CREATE TABLE IF NOT EXISTS hospitals (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    location_lat DECIMAL(10, 8) NOT NULL,
    location_lon DECIMAL(11, 8) NOT NULL,
    total_beds INT NOT NULL,
    available_beds INT NOT NULL CHECK (available_beds >= 0 AND available_beds <= total_beds),
    trauma_level INT NOT NULL CHECK (trauma_level BETWEEN 1 AND 5),
    admin_id UUID REFERENCES users(id) ON DELETE SET NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TRIGGER set_timestamp_hospitals BEFORE UPDATE ON hospitals FOR EACH ROW EXECUTE PROCEDURE trigger_set_timestamp();

CREATE TABLE IF NOT EXISTS emergencies (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    reporter_id UUID REFERENCES users(id) ON DELETE SET NULL,
    status emergency_status DEFAULT 'ACTIVE',
    location_lat DECIMAL(10, 8) NOT NULL,
    location_lon DECIMAL(11, 8) NOT NULL,
    description TEXT,
    detected_via_nlp BOOLEAN DEFAULT false,
    severity INT DEFAULT 3 CHECK (severity BETWEEN 1 AND 5),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TRIGGER set_timestamp_emergencies BEFORE UPDATE ON emergencies FOR EACH ROW EXECUTE PROCEDURE trigger_set_timestamp();

CREATE TABLE IF NOT EXISTS resources (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    type resource_type NOT NULL,
    status VARCHAR(50) DEFAULT 'AVAILABLE',
    assigned_to UUID REFERENCES emergencies(id) ON DELETE SET NULL,
    location_lat DECIMAL(10, 8) NOT NULL,
    location_lon DECIMAL(11, 8) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TRIGGER set_timestamp_resources BEFORE UPDATE ON resources FOR EACH ROW EXECUTE PROCEDURE trigger_set_timestamp();

-- Create Performance Indexes
CREATE INDEX IF NOT EXISTS idx_emergencies_location ON emergencies (location_lat, location_lon);
CREATE INDEX IF NOT EXISTS idx_emergencies_status_severity ON emergencies (status, severity);
CREATE INDEX IF NOT EXISTS idx_hospitals_availability ON hospitals (available_beds);
CREATE INDEX IF NOT EXISTS idx_users_email ON users (email);
