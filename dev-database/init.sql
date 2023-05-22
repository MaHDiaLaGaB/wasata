CREATE USER wasata_user WITH PASSWORD 'wasata_password';

CREATE DATABASE users_db;
GRANT ALL PRIVILEGES ON DATABASE users_db TO wasata_user;

