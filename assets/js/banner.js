// banner.js

const mensagens = [
  '🎨 Apoie artistas locais! <strong>Refugiart Bazar</strong>',
  '🖌️ Patrocine um artista hoje!',
  '🌍 Junte-se à rede cultural da Transamazônica!',
  '💡 Descubra talentos regionais agora mesmo!'
];

let index = 0;
const bannerText = document.getElementById("banner-text");

setInterval(() => {
  index = (index + 1) % mensagens.length;
  bannerText.style.opacity = 0;

  setTimeout(() => {
    bannerText.innerHTML = mensagens[index];
    bannerText.style.opacity = 1;
  }, 500);
}, 3000);