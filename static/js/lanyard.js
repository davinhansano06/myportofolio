document.addEventListener("DOMContentLoaded", function () {
    const photo = document.querySelector(".hero-photo");
    const avatar = document.querySelector(".hero-photo .avatar");

    if (!photo || !avatar) {
        return;
    }

    let targetX = 0;
    let targetY = 0;
    let targetRotation = 0;

    let currentX = 0;
    let currentY = 0;
    let currentRotation = 0;

    let time = 0;

    photo.addEventListener("mousemove", function (event) {
        const rect = photo.getBoundingClientRect();

        const mouseX = event.clientX - rect.left;
        const mouseY = event.clientY - rect.top;

        const centerX = rect.width / 2;
        const centerY = rect.height / 2;

        const offsetX = mouseX - centerX;
        const offsetY = mouseY - centerY;

        targetX = (offsetX / centerX) * 12;
        targetY = (offsetY / centerY) * 7;
        targetRotation = (offsetX / centerX) * 3;
    });

    photo.addEventListener("mouseleave", function () {
        targetX = 0;
        targetY = 0;
        targetRotation = 0;
    });

    function animate() {
        time += 0.015;

        // Gerakan floating yang sangat pelan
        const idleX = Math.sin(time) * 2;
        const idleY = Math.sin(time * 1.3) * 3;
        const idleRotation = Math.sin(time * 0.8) * 1;

        // Cursor follow
        currentX += (targetX - currentX) * 0.06;
        currentY += (targetY - currentY) * 0.06;
        currentRotation +=
            (targetRotation - currentRotation) * 0.06;

        avatar.style.transform = `
            translate(
                ${currentX + idleX}px,
                ${currentY + idleY}px
            )
            rotate(${currentRotation + idleRotation}deg)
        `;

        requestAnimationFrame(animate);
    }

    animate();

    // Fade ketika profile masuk / keluar viewport
    const fadeObserver = new IntersectionObserver(
        function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    photo.classList.add("profile-visible");
                } else {
                    photo.classList.remove("profile-visible");
                }
            });
        },
        {
            threshold: 0.5
        }
    );

    fadeObserver.observe(photo);

    // Profile parallax saat scroll
    function updateParallax() {
        const rect = photo.getBoundingClientRect();
        const windowHeight = window.innerHeight;

        const distanceFromCenter =
            rect.top + rect.height / 2 - windowHeight / 2;

        const parallaxY = distanceFromCenter * -0.06;

        photo.style.setProperty(
            "--parallax-y",
            `${parallaxY}px`
        );
    }

    window.addEventListener("scroll", updateParallax);
    updateParallax();
});