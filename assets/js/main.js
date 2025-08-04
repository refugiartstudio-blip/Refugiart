document.addEventListener("DOMContentLoaded", () => {
  fadeInBody();
  setupSmoothScroll();
  setupModal();
  setupCadastroForm();
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

// Navegação suave
function setupSmoothScroll() {
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener("click", function (e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute("href"));
      if (target) {
        target.scrollIntoView({ behavior: "smooth" });
      }
    });
  });
}

// Modal simples
function setupModal() {
  const modal = document.getElementById("modal");
  const openModal = document.getElementById("openModal");
  const closeModal = document.getElementById("closeModal");

  if (modal && openModal && closeModal) {
    openModal.addEventListener("click", () => modal.classList.remove("hidden"));
    closeModal.addEventListener("click", () => modal.classList.add("hidden"));
  }
}

// Toasts
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

// Cadastro via FastAPI
function setupCadastroForm() {
  const form = document.getElementById("formCadastro");
  if (!form) return;

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const nome = document.getElementById("nome").value.trim();
    const email = document.getElementById("email").value.trim();
    const senha = document.getElementById("senha").value;

    if (!nome || !email || !senha) {
      showToast("Preencha todos os campos!", "error");
      return;
    }

    try {
      const response = await fetch("https://refugiart.onrender.com/cadastro", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ nome, email, senha })
      });

      if (!response.ok) {
        const err = await response.json();
        showToast(err.detail || "Erro no cadastro", "error");
        return;
      }

      showToast("Cadastro realizado com sucesso!", "success");
      form.reset();
    } catch (err) {
      showToast("Erro de conexão com o servidor!", "error");
      console.error(err);
    }
  });
}