// perfil.js

document.addEventListener("DOMContentLoaded", function () {
  const editBtn = document.getElementById("edit-bio");

  if (!editBtn) return;

  editBtn.addEventListener("click", function () {
    const bioContainer = document.getElementById("bio-container");
    const currentBio = document.getElementById("bio-text").textContent;

    bioContainer.innerHTML = `
      <input type="text" id="bio-input" value="${currentBio}" />
      <button id="save-bio">Salvar</button>
    `;

    document.getElementById("save-bio").addEventListener("click", async function () {
      const newBio = document.getElementById("bio-input").value;

      // Aqui você pode fazer um PUT na API para salvar a bio
      // await fetch("/api/update_bio", { method: "PUT", body: JSON.stringify({ bio: newBio }) })

      bioContainer.innerHTML = `
        <span id="bio-text">${newBio}</span>
        <button id="edit-bio">✏️</button>
      `;
    });
  });
});