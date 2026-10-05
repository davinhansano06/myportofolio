document.addEventListener("DOMContentLoaded", function () {
    document.body.classList.add("page-loaded");

    const elements = document.querySelectorAll(
        ".hero-kicker, .hero-identity h1, .hero-details, .hero-contact, .education-heading, .experience-heading, .experience-card, .item-pengalaman"
    );

    const observer = new IntersectionObserver(
        function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    entry.target.classList.add("scroll-visible");
                }
            });
        },
        {
            threshold: 2
        }
    );

    elements.forEach(function (element) {
        element.classList.add("scroll-reveal");
        observer.observe(element);
    });
});

// =================================
// NAME LETTER ANIMATION
// =================================

const nameTitle = document.querySelector(".hero-identity h1");

if (nameTitle) {
    const text = nameTitle.textContent.trim();

    nameTitle.innerHTML = "";

    text.split("").forEach(function (letter, index) {
        const span = document.createElement("span");

        span.textContent = letter === " " ? "\u00A0" : letter;

        span.classList.add("name-letter");

        span.style.animationDelay =
            `${index * 45}ms`;

        nameTitle.appendChild(span);
    });

    nameTitle.classList.add("name-animated");
}

    // =================================
    // SKILL CAROUSEL
    // =================================

    const skillCarousel = document.querySelector(".grid-skill");

    if (skillCarousel) {

        const skillCards =
            Array.from(
                skillCarousel.querySelectorAll(".cover-kartu")
            );

        let currentSkill = 0;
        let skillTimer = null;

        function updateSkillCarousel() {

            skillCards.forEach(function (card, index) {

                card.classList.toggle(
                    "skill-active",
                    index === currentSkill
                );

            });

        }

        function nextSkill() {

            currentSkill++;

            if (currentSkill >= skillCards.length) {
                currentSkill = 0;
            }

            updateSkillCarousel();
        }

        function startSkillCarousel() {

            if (skillTimer) {
                clearInterval(skillTimer);
            }

            skillTimer = setInterval(
                nextSkill,
                1800
            );
        }

        updateSkillCarousel();
        startSkillCarousel();


        // Pause ketika cursor berada di Skill
        skillCarousel.addEventListener(
            "mouseenter",
            function () {

                clearInterval(skillTimer);

            }
        );


        skillCarousel.addEventListener(
            "mouseleave",
            function () {

                startSkillCarousel();

            }
        );


        // =================================
        // SUBTLE 3D TILT
        // =================================

        skillCards.forEach(function (card) {

            card.addEventListener(
                "mousemove",
                function (event) {

                    const rect =
                        card.getBoundingClientRect();

                    const x =
                        event.clientX - rect.left;

                    const y =
                        event.clientY - rect.top;

                    const centerX =
                        rect.width / 2;

                    const centerY =
                        rect.height / 2;

                    const rotateY =
                        ((x - centerX) / centerX) * 5;

                    const rotateX =
                        ((centerY - y) / centerY) * 5;

                    card.querySelector(
                        ".skill-card"
                    ).style.transform = `
                        perspective(700px)
                        rotateX(${rotateX}deg)
                        rotateY(${rotateY}deg)
                        translateY(-8px)
                    `;

                }
            );


            card.addEventListener(
                "mouseleave",
                function () {

                    card.querySelector(
                        ".skill-card"
                    ).style.transform = "";

                }
            );

        });

    }