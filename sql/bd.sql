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

CREATE TABLE vendas (
	id_venda INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT NOT NULL,
    data_venda DATETIME NOT NULL,
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
)

CREATE TABLE itens_por_venda (
	id_item_venda INT AUTO_INCREMENT PRIMARY KEY,
    id_venda INT NOT NULL,
    id_produto INT NOT NULL,
    quantidade INT NOT NULL,
    FOREIGN KEY (id_venda) REFERENCES vendas(id_venda),
    FOREIGN KEY (id_produto) REFERENCES produto(id_produto)
)

-- Durante minha analise de projeto, notei a falta de necessidade de manter a hora no vendas (data_venda)
-- Entao decidi fazer umas mudanças no bd

ALTER TABLE vendas
MODIFY COLUMN data_venda DATE NOT NULL;