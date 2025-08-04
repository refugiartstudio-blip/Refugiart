// auth.js

async function loginUser(event) {
  event.preventDefault();

  const email = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value.trim();

  const response = await fetch("https://refugiart.onrender.com/login", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ email, password })
  });

  if (response.ok) {
    const data = await response.json();
    localStorage.setItem("token", data.token);  // ou outro campo retornado
    alert("Login bem-sucedido!");
    window.location.href = "perfil.html";
  } else {
    alert("Erro no login. Verifique suas credenciais.");
  }
}

function logoutUser() {
  localStorage.removeItem("token");
  window.location.href = "login.html";
}