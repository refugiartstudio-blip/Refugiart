document.addEventListener("DOMContentLoaded", () => {
  // Animação inicial de fade-in no corpo da página
  fadeInBody();

  // Navegação suave para âncoras
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener("click", function (e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute("href"));
      if (target) {
        target.scrollIntoView({ behavior: "smooth" });
      }
    });
  });

  // Controle de modal (se existir no HTML)
  const modal = document.getElementById("modal");
  const openModal = document.getElementById("openModal");
  const closeModal = document.getElementById("closeModal");

  if (modal && openModal && closeModal) {
    openModal.addEventListener("click", () => modal.classList.remove("hidden"));
    closeModal.addEventListener("click", () => modal.classList.add("hidden"));
  }

  // Exemplo de toast ao carregar
  showToast("Site carregado com sucesso!", "success");
});

// ------------------------------
// Funções auxiliares
// ------------------------------

// Efeito de fade-in no <body>
function fadeInBody() {
  document.body.style.opacity = 0;
  document.body.style.transition = "opacity 1s";
  setTimeout(() => {
    document.body.style.opacity = 1;
  }, 100);
}

// Exibição de mensagens toast
function showToast(message, type = "info") {
  const toast = document.getElementById("toast");
  if (!toast) return;

  toast.innerText = message;
  toast.className = `toast toast-${type}`;
  toast.style.opacity = 1;

  setTimeout(() => {
    toast.style.opacity = 0;
  }, 3000);
}
