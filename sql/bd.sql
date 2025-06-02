CREATE database solus;
USE solus

CREATE TABLE clientes (
    id_cliente INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(50) NOT NULL,
    sobrenome VARCHAR(50),
    cpf CHAR(11) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL
)

CREATE TABLE produto (
	id_produto INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR (50) NOT NULL,
    categoria VARCHAR (50) NOT NULL,
    preco DECIMAL (10,2) NOT NULL
)