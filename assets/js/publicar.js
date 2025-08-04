// publicar.js

document.querySelector("form").addEventListener("submit", async function (e) {
  e.preventDefault();

  const formData = new FormData(this);

  const response = await fetch("https://refugiart.onrender.com/publicar", {
    method: "POST",
    body: formData
  });

  if (response.ok) {
    alert("Obra publicada com sucesso!");
    window.location.href = "perfil.html";
  } else {
    alert("Erro ao publicar a obra.");
  }
});