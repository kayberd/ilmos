CREATE OR REPLACE FUNCTION notify_updates() RETURNS TRIGGER AS $$
   BEGIN
      NOTIFY test, 'update';
      RETURN null;
   END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION notify_insertions() RETURNS TRIGGER AS $$
   BEGIN 
      NOTIFY test, 'insertion';
      RETURN null;
   END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION notify_deletions() RETURNS TRIGGER AS $$
   BEGIN
      NOTIFY test, 'deletion';
      RETURN null;
   END;
$$ LANGUAGE plpgsql;


DO $$
DECLARE
   t text;
BEGIN 
   FOR t in 
      SELECT table_name 
      FROM information_schema.tables
      WHERE table_name like 'library%'
   LOOP
      EXECUTE format('CREATE TRIGGER insertion_%I
                      AFTER INSERT ON %I
                      FOR EACH ROW EXECUTE PROCEDURE notify_insertions()', 
                      t, t);
   END LOOP;
END;
$$ LANGUAGE plpgsql;


DO $$
DECLARE
   t text;
BEGIN 
   FOR t in 
      SELECT table_name 
      FROM information_schema.tables
      WHERE table_name like 'library%'
   LOOP
      EXECUTE format('CREATE TRIGGER update_%I
                      AFTER UPDATE ON %I
                      FOR EACH ROW EXECUTE PROCEDURE notify_updates()', 
                      t, t);
   END LOOP;
END;
$$ LANGUAGE plpgsql;


DO $$
DECLARE
   t text;
BEGIN 
   FOR t in 
      SELECT table_name 
      FROM information_schema.tables
      WHERE table_name like 'library%'
   LOOP
      EXECUTE format('CREATE TRIGGER deletion_%I
                      AFTER DELETE ON %I
                      FOR EACH ROW EXECUTE PROCEDURE notify_deletions()', 
                      t, t);
   END LOOP;
END;
$$ LANGUAGE plpgsql;