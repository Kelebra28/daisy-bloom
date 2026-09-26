const productsData = {
  'serum': {
    title: 'Suero Facial de Hidratación Profunda',
    brand: 'SEYTÚ',
    price: '$450.00 MXN',
    reviews: '(124)',
    desc: 'Un suero ligero pero potente, enriquecido con ácido hialurónico y extractos botánicos. Ideal para brindar luminosidad y una hidratación duradera a tu rostro. Absorción rápida sin sensación grasosa.',
    image: '/assets/img/seytu-serum.jpg'
  },
  'foam': {
    title: 'Espuma Limpiadora Facial',
    brand: 'SEYTÚ',
    price: '$380.00 MXN',
    reviews: '(342)',
    desc: 'Limpiador facial en espuma con extractos de aloe vera y moringa. Remueve impurezas de forma suave y efectiva, dejando tu piel fresca, limpia y sin sensación de tirantez.',
    image: '/assets/img/seytu-foam.jpg'
  },
  'foundation': {
    title: 'Maquillaje Líquido UP+ FPS 15',
    brand: 'SEYTÚ',
    price: '$510.00 MXN',
    reviews: '(89)',
    desc: 'Base de maquillaje de cobertura construible con FPS 15. Enriquecida con colágeno hidrolizado y ácido hialurónico, proporcionando un acabado mate radiante, resistente al agua y al sudor.',
    image: '/assets/img/seytu-foundation.jpg'
  }
};

function openModal(productId) {
  const product = productsData[productId];
  if (!product) return;

  document.getElementById('modal-img').src = product.image;
  document.getElementById('modal-brand').textContent = product.brand;
  document.getElementById('modal-title').textContent = product.title;
  document.getElementById('modal-price').textContent = product.price;
  document.getElementById('modal-reviews').textContent = product.reviews;
  document.getElementById('modal-desc').textContent = product.desc;

  // Build whatsapp message
  const msg = encodeURIComponent(`Hola Daisy! Me interesa conocer más sobre el producto: ${product.title}`);
  document.getElementById('modal-whatsapp').href = `https://wa.me/5215555555555?text=${msg}`;

  document.getElementById('product-modal').classList.add('active');
  document.body.style.overflow = 'hidden'; // prevent scrolling
}

function closeModal() {
  document.getElementById('product-modal').classList.remove('active');
  document.body.style.overflow = '';
}

// Close modal when clicking outside
document.getElementById('product-modal').addEventListener('click', function(e) {
  if (e.target === this) {
    closeModal();
  }
});

// Escape key to close modal
document.addEventListener('keydown', function(e) {
  if (e.key === 'Escape') {
    closeModal();
  }
});
