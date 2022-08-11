# After applying changes on models:
1. delete all the files under library/migrations EXCEPT __init__.py
2. 
	1. sudo su - postgres
	2. psql
	3. drop database main;
	4. create database main;
	5. drop user if exists ilmos;
	6. CREATE USER ilmos WITH PASSWORD 'ilmos3131';
	7. ALTER ROLE ilmos SET client_encoding TO 'utf8';
	8. ALTER ROLE ilmos SET default_transaction_isolation TO 'read committed';
	9. ALTER ROLE ilmos SET timezone TO 'UTC';
	10. GRANT ALL PRIVILEGES ON DATABASE main TO ilmos;
	11. \q
	12. exit
3. python manage.py makemigrations
4. python manage.py migrate
