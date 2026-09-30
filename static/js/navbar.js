document.addEventListener("DOMContentLoaded", function () {
    console.log("NAVBAR JS BERJALAN");

    const menuButton = document.getElementById("mobile-menu-button");
    const mainNav = document.getElementById("main-nav");

    console.log("BUTTON:", menuButton);
    console.log("NAV:", mainNav);

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