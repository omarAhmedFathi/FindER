-- Run this directly in the database or via Alembic to enforce DB-level separation
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE emergencies ENABLE ROW LEVEL SECURITY;

-- Responders can only see their own profile
CREATE POLICY user_isolation_policy ON users
    FOR ALL
    USING (id = current_setting('finder.current_user_id')::uuid);

-- Emergency Managers bypass RLS
CREATE POLICY admin_bypass_policy ON users
    FOR ALL
    USING (current_setting('finder.current_role') = 'EMERGENCY_MANAGER');
