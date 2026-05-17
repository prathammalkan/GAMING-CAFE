document.addEventListener("DOMContentLoaded", () => {
    const cards = document.querySelectorAll(".game-card, .genre-card, .editorial-card");

    cards.forEach((card) => {
        card.addEventListener("mousemove", (event) => {
            const bounds = card.getBoundingClientRect();
            const rotateY = ((event.clientX - bounds.left) / bounds.width - 0.5) * 6;
            const rotateX = ((event.clientY - bounds.top) / bounds.height - 0.5) * -6;
            card.style.transform = `perspective(900px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-4px)`;
        });

        card.addEventListener("mouseleave", () => {
            card.style.transform = "";
        });
    });
});
