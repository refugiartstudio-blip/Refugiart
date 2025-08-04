// cadastro.js

document.querySelector("form").addEventListener("submit", async function (e) {
  e.preventDefault();

  const nome = document.getElementById("name").value.trim();
  const email = document.getElementById("email").value.trim();
  const username = document.getElementById("username").value.trim();
  const password = document.getElementById("password").value;
  const passwordConfirm = document.getElementById("passwordConfirm").value;

  if (password !== passwordConfirm) {
    return alert("As senhas não coincidem!");
  }

  const response = await fetch("https://refugiart.onrender.com/register", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ nome, email, username, senha: password })
  });

  if (response.ok) {
    alert("Cadastro realizado com sucesso!");
    window.location.href = "login.html";
  } else {
    alert("Erro no cadastro. Verifique os dados.");
  }
});