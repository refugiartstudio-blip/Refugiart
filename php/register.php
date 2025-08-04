<?php
// register.php

// Função para limpar dados de entrada (proteção básica)
function limparEntrada($data) {
    return htmlspecialchars(stripslashes(trim($data)));
}

if ($_SERVER["REQUEST_METHOD"] === "POST") {
    // Limpa e pega os dados
    $name = limparEntrada($_POST["name"] ?? "");
    $email = limparEntrada($_POST["email"] ?? "");
    $username = limparEntrada($_POST["username"] ?? "");
    $password = $_POST["password"] ?? "";
    $passwordConfirm = $_POST["passwordConfirm"] ?? "";

    // Validações básicas
    if (!$name || !$email || !$username || !$password || !$passwordConfirm) {
        die("Por favor, preencha todos os campos.");
    }

    if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
        die("E-mail inválido.");
    }

    if ($password !== $passwordConfirm) {
        die("As senhas não coincidem.");
    }

    // Hash da senha para segurança
    $senhaHash = password_hash($password, PASSWORD_DEFAULT);

    // Dados para salvar (nome, email, usuário, senha hash)
    $registro = [$name, $email, $username, $senhaHash];

    // Caminho para arquivo CSV (pode mudar para um banco de dados)
    $arquivoCSV = "usuarios.csv";

    // Abre arquivo para adicionar dados
    $fp = fopen($arquivoCSV, "a");

    if (!$fp) {
        die("Erro ao abrir arquivo para salvar os dados.");
    }

    // Salva o registro no arquivo CSV
    fputcsv($fp, $registro);

    fclose($fp);

    // Redireciona para a página de login após cadastro
    header("Location: login.html");
    exit;
} else {
    // Se não for POST, redireciona para cadastro
    header("Location: cadastro.html");
    exit;
}