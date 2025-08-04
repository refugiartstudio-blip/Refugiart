<?php
// Configurações do banco de dados - ajuste conforme seu ambiente
$DB_HOST = "localhost";        // endereço do servidor MySQL
$DB_USER = "seu_usuario";      // usuário do banco
$DB_PASS = "sua_senha";        // senha do banco
$DB_NAME = "seu_banco_de_dados";  // nome do banco de dados

// Cria a conexão
$conn = new mysqli($DB_HOST, $DB_USER, $DB_PASS, $DB_NAME);

// Verifica a conexão
if ($conn->connect_error) {
    die("Falha na conexão com o banco de dados: " . $conn->connect_error);
}

// Define charset para evitar problemas de acentuação
$conn->set_charset("utf8mb4");