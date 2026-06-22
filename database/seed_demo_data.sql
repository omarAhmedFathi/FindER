-- FindER Demo Seed Data
-- Run after schema.sql: psql finder_db < seed_demo_data.sql
-- All demo accounts use password: demo1234

-- ENUMS (skip if already exist)
DO $$ BEGIN
  CREATE TYPE user_role AS ENUM ('EMERGENCY_MANAGER','FIRST_RESPONDER','FIELD_MEDIC','HOSPITAL_ADMIN','BYSTANDER');
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
  CREATE TYPE emergency_status AS ENUM ('ACTIVE','ROUTED','RESOLVED','FALSE_ALARM');
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
  CREATE TYPE resource_type AS ENUM ('AMBULANCE','FIRE_TRUCK','HELO','SUPPLY_DROP');
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

-- USERS (password = demo1234, bcrypt hash)
INSERT INTO users (id, email, hashed_password, full_name, role, is_active) VALUES
  ('5d2acba9-015e-4a73-b53f-7febb4aff612', 'manager@finder.com',     '$2b$12$bTBkHAQ4jcLIMtK64koJTep60tWJEb7eKyh3dfebB67Kaj66.aAVi', 'Alex Manager',        'EMERGENCY_MANAGER', true),
  ('b6ad3093-f13c-4035-af07-bb4368a4862a', 'responder@finder.com',   '$2b$12$bTBkHAQ4jcLIMtK64koJTep60tWJEb7eKyh3dfebB67Kaj66.aAVi', 'Sam Responder',       'FIRST_RESPONDER',   true),
  ('cb850ea3-bbd5-4257-af69-0c290988128e', 'medic@finder.com',       '$2b$12$bTBkHAQ4jcLIMtK64koJTep60tWJEb7eKyh3dfebB67Kaj66.aAVi', 'Dr. Rivera',          'FIELD_MEDIC',       true),
  ('53bc9c7c-9f4b-4d93-b02c-d60e79ee32c8', 'admin@cityhospital.com', '$2b$12$bTBkHAQ4jcLIMtK64koJTep60tWJEb7eKyh3dfebB67Kaj66.aAVi', 'City Hospital Admin', 'HOSPITAL_ADMIN',    true),
  ('c329bd86-5f0b-4412-a974-5b0c33f0403f', 'user@finder.com',        '$2b$12$bTBkHAQ4jcLIMtK64koJTep60tWJEb7eKyh3dfebB67Kaj66.aAVi', 'Jane Civilian',       'BYSTANDER',         true)
ON CONFLICT (email) DO NOTHING;

-- HOSPITALS
INSERT INTO hospitals (name, location_lat, location_lon, total_beds, available_beds, trauma_level, admin_id) VALUES
  ('City General Hospital',     37.77490000, -122.41940000, 200, 45,  1, '5d2acba9-015e-4a73-b53f-7febb4aff612'),
  ('Bay Area Medical Center',   37.80440000, -122.27110000, 150, 22,  2, '5d2acba9-015e-4a73-b53f-7febb4aff612'),
  ('St. Mary Emergency Clinic', 37.75100000, -122.46610000,  80, 60,  3, '5d2acba9-015e-4a73-b53f-7febb4aff612'),
  ('Oakland Trauma Center',     37.80490000, -122.27120000, 300, 12,  1, '5d2acba9-015e-4a73-b53f-7febb4aff612'),
  ('Peninsula Community Hosp',  37.52430000, -122.03060000, 120, 88,  3, '5d2acba9-015e-4a73-b53f-7febb4aff612')
ON CONFLICT DO NOTHING;

-- RESOURCES
INSERT INTO resources (name, type, status, location_lat, location_lon) VALUES
  ('Ambulance Alpha-1', 'AMBULANCE',  'AVAILABLE', 37.77490000, -122.41940000),
  ('Ambulance Beta-2',  'AMBULANCE',  'AVAILABLE', 37.78000000, -122.41000000),
  ('Ambulance Gamma-3', 'AMBULANCE',  'AVAILABLE', 37.76500000, -122.43000000),
  ('Fire Engine 7',     'FIRE_TRUCK', 'AVAILABLE', 37.77000000, -122.43000000),
  ('Fire Engine 12',    'FIRE_TRUCK', 'AVAILABLE', 37.78500000, -122.40500000),
  ('MedHelo-1',         'HELO',       'AVAILABLE', 37.79000000, -122.40000000),
  ('Supply Drop A',     'SUPPLY_DROP','AVAILABLE', 37.76000000, -122.44000000);

-- EMERGENCIES
INSERT INTO emergencies (reporter_id, status, location_lat, location_lon, description, severity) VALUES
  ('5d2acba9-015e-4a73-b53f-7febb4aff612', 'ACTIVE',   37.77510000, -122.41800000, 'Multi-car collision on Highway 101 — 3 injured, 1 critical', 4),
  ('5d2acba9-015e-4a73-b53f-7febb4aff612', 'ACTIVE',   37.78200000, -122.40500000, 'Building fire on Market St — residents trapped on 3rd floor', 5),
  ('5d2acba9-015e-4a73-b53f-7febb4aff612', 'ROUTED',   37.76800000, -122.43200000, 'Elderly person collapsed, suspected cardiac event',            5),
  (NULL,                                   'ACTIVE',   37.76000000, -122.44000000, 'SOS Alert — anonymous report from Mission District',           5),
  ('5d2acba9-015e-4a73-b53f-7febb4aff612', 'RESOLVED', 37.79000000, -122.39500000, 'Gas leak reported — area evacuated and sealed',                3),
  ('5d2acba9-015e-4a73-b53f-7febb4aff612', 'ACTIVE',   37.77900000, -122.42300000, 'Person trapped in elevator at office building',               3);
