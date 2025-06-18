// Smooth scroll untuk anchor link
document.addEventListener("DOMContentLoaded", function () {
  const links = document.querySelectorAll('a[href^="#"]');

  for (const link of links) {
    link.addEventListener("click", function (e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute("href"));
      if (target) {
        target.scrollIntoView({ behavior: "smooth" });
      }
    });
  }
});

// Notifikasi sederhana saat item ditambahkan ke keranjang
const addToCartButtons = document.querySelectorAll("form[action='/add_to_cart'] button");

addToCartButtons.forEach((button) => {
  button.addEventListener("click", function () {
    alert("Item berhasil ditambahkan ke keranjang!");
  });
});
