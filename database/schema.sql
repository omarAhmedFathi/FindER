-- FindER Core Schema

CREATE TYPE user_role AS ENUM ('EMERGENCY_MANAGER', 'FIRST_RESPONDER', 'FIELD_MEDIC', 'HOSPITAL_ADMIN', 'BYSTANDER');
CREATE TYPE emergency_status AS ENUM ('ACTIVE', 'ROUTED', 'RESOLVED', 'FALSE_ALARM');
CREATE TYPE resource_type AS ENUM ('AMBULANCE', 'FIRE_TRUCK', 'HELO', 'SUPPLY_DROP');

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    role user_role NOT NULL,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE hospitals (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    location_lat DECIMAL(10, 8) NOT NULL,
    location_lon DECIMAL(11, 8) NOT NULL,
    total_beds INT NOT NULL,
    available_beds INT NOT NULL,
    trauma_level INT NOT NULL,
    admin_id UUID REFERENCES users(id)
);

CREATE TABLE emergencies (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    reporter_id UUID REFERENCES users(id),
    status emergency_status DEFAULT 'ACTIVE',
    location_lat DECIMAL(10, 8) NOT NULL,
    location_lon DECIMAL(11, 8) NOT NULL,
    description TEXT,
    detected_via_nlp BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE resources (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    type resource_type NOT NULL,
    status VARCHAR(50) DEFAULT 'AVAILABLE',
    assigned_to UUID REFERENCES emergencies(id) NULL,
    location_lat DECIMAL(10, 8) NOT NULL,
    location_lon DECIMAL(11, 8) NOT NULL
);

-- Indexes for spatial and temporal queries
CREATE INDEX idx_emergencies_location ON emergencies (location_lat, location_lon);
CREATE INDEX idx_emergencies_status ON emergencies (status);
CREATE INDEX idx_hospitals_availability ON hospitals (available_beds);
