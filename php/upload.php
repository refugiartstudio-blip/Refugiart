<?php
if (isset($_FILES['foto'])) {
  $pasta = "uploads/";
  $nome = basename($_FILES['foto']['name']);
  $caminho = $pasta . $nome;

  if (move_uploaded_file($_FILES['foto']['tmp_name'], $caminho)) {
    echo "Foto enviada com sucesso!";
    // Aqui você poderia salvar o caminho no banco de dados
  } else {
    echo "Erro ao enviar a foto.";
  }
}
?>