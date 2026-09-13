document.addEventListener("DOMContentLoaded", function () {
    const menuButton = document.getElementById("mobile-menu-button");
    const mainNav = document.getElementById("main-nav");

    if (menuButton && mainNav) {
        menuButton.addEventListener("click", function () {
            mainNav.classList.toggle("active");
        });

        const navLinks = mainNav.querySelectorAll("a");

        navLinks.forEach(function (link) {
            link.addEventListener("click", function () {
                mainNav.classList.remove("active");
            });
        });
    }
});