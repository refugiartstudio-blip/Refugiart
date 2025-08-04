<?php
// Inicia a sessão
session_start();

// Destroi todas as variáveis de sessão
$_SESSION = array();

// Se existir um cookie de sessão, apaga ele também
if (ini_get("session.use_cookies")) {
    $params = session_get_cookie_params();
    setcookie(
        session_name(),
        '',
        time() - 42000,
        $params["path"],
        $params["domain"],
        $params["secure"],
        $params["httponly"]
    );
}

// Destroi a sessão completamente
session_destroy();

// Redireciona para a tela de cadastro
header("Location: cadastro.html");
exit;
?>