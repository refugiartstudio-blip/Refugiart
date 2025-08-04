<?php
session_start();
include 'config.php'; // arquivo com conexão ao banco

// Verifica se o formulário foi enviado
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $username = trim($_POST['username'] ?? '');
    $password = $_POST['password'] ?? '';

    if (empty($username) || empty($password)) {
        $error = "Por favor, preencha usuário e senha.";
    } else {
        // Preparar consulta segura
        $stmt = $conn->prepare("SELECT id, username, password FROM users WHERE username = ?");
        $stmt->bind_param('s', $username);
        $stmt->execute();
        $result = $stmt->get_result();

        if ($result && $result->num_rows === 1) {
            $user = $result->fetch_assoc();
            // Verifica a senha com password_verify
            if (password_verify($password, $user['password'])) {
                // Login bem sucedido
                $_SESSION['user_id'] = $user['id'];
                $_SESSION['username'] = $user['username'];
                header('Location: index.html'); // redireciona para página principal
                exit;
            } else {
                $error = "Senha incorreta.";
            }
        } else {
            $error = "Usuário não encontrado.";
        }
        $stmt->close();
    }
}
?>

<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Login - Refugiart</title>
  <link rel="stylesheet" href="assets/css/cadastro.css" />
</head>
<body>
  <div class="container" style="max-width: 400px; margin: 40px auto; background: white; padding: 24px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
    <h1 style="text-align: center; background: linear-gradient(to right, #9333ea, #ec4899); -webkit-background-clip: text; color: transparent; font-weight: bold; margin-bottom: 24px;">Login</h1>

    <?php if (!empty($error)) : ?>
      <div style="color: red; margin-bottom: 16px; text-align: center;"><?= htmlspecialchars($error) ?></div>
    <?php endif; ?>

    <form action="login.php" method="POST">
      <label for="username">Nome de usuário</label>
      <input type="text" id="username" name="username" placeholder="Seu usuário" required />

      <label for="password">Senha</label>
      <input type="password" id="password" name="password" placeholder="Sua senha" required />

      <button type="submit">Entrar</button>
    </form>

    <p style="text-align: center; margin-top: 18px;">
      Não tem conta? <a href="cadastro.html" style="color: #9333ea; font-weight: bold;">Cadastre-se aqui</a>
    </p>
  </div>
</body>
</html>