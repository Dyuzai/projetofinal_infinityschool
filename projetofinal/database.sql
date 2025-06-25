         -- Utilzei o Workbench pra codar.

CREATE DATABASE projeto_batman;
USE projeto_batman;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    role ENUM('clt', 'gerente', 'adm') NOT NULL
);

CREATE TABLE bat_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    quantity INT DEFAULT 0,
    description TEXT
);

INSERT INTO users (username, password, role) VALUES 
('batman', 'batman123', 'adm'),
('alfred', 'alf123', 'gerente'),
('coringa', 'cdobatman', 'clt');