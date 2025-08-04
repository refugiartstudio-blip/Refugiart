// recarga.js

function recarregar(valor) {
  const saldoEl = document.getElementById('saldo');
  let atual = parseFloat(saldoEl.textContent);
  saldoEl.textContent = (atual + valor).toFixed(2);
  document.getElementById('modal-recarga').classList.remove('active');
}