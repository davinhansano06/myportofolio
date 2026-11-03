let experienceAutoSlideTimer = null;

function initializeExperienceCarousel() {
    const carousel = document.querySelector(".experience-carousel");

    if (!carousel) {
        return;
    }

    const track = carousel.querySelector(".experience-track");
    const cards = carousel.querySelectorAll(".experience-card");
    const previousButton = carousel.querySelector(".carousel-prev");
    const nextButton = carousel.querySelector(".carousel-next");
    const dotsContainer = carousel.parentElement.querySelector(".carousel-dots");

    if (
        !track ||
        cards.length === 0 ||
        !previousButton ||
        !nextButton ||
        !dotsContainer
    ) {
        return;
    }

    let currentIndex = 0;
    const AUTO_SLIDE_INTERVAL = 2600;

    function getVisibleCards() {
        if (window.innerWidth <= 768) {
            return 1;
        }

        return 2;
    }

    function getMaxIndex() {
        return Math.max(
            0,
            cards.length - getVisibleCards()
        );
    }

    function updateCarousel() {
        if (!cards[0]) {
            return;
        }

        const cardWidth = cards[0].getBoundingClientRect().width;

        const gap = parseFloat(
            window.getComputedStyle(track).gap
        ) || 0;

        const offset = currentIndex * (cardWidth + gap);

        track.style.transform = `translateX(-${offset}px)`;

        updateDots();
    }

    function createDots() {
        dotsContainer.innerHTML = "";

        const maxIndex = getMaxIndex();

        for (let i = 0; i <= maxIndex; i++) {
            const dot = document.createElement("button");

            dot.type = "button";
            dot.classList.add("carousel-dot");

            dot.setAttribute(
                "aria-label",
                `Go to experience ${i + 1}`
            );

            dot.addEventListener("click", function () {
                currentIndex = i;
                updateCarousel();
                restartAutoSlide();
            });

            dotsContainer.appendChild(dot);
        }

        updateDots();
    }

    function updateDots() {
        const dots = dotsContainer.querySelectorAll(".carousel-dot");

        dots.forEach(function (dot, index) {
            dot.classList.toggle(
                "active",
                index === currentIndex
            );
        });
    }

    function stepNext() {
        const maxIndex = getMaxIndex();
        if (maxIndex <= 0) {
            return;
        }
        if (currentIndex < maxIndex) {
            currentIndex++;
        } else {
            currentIndex = 0;
        }
        updateCarousel();
    }

    function startAutoSlide() {
        stopAutoSlide();
        experienceAutoSlideTimer = setInterval(function () {
            const popup = document.getElementById("experience-detail-popup");
            if (popup && popup.classList.contains("active")) {
                return;
            }
            stepNext();
        }, AUTO_SLIDE_INTERVAL);
    }

    function stopAutoSlide() {
        if (experienceAutoSlideTimer) {
            clearInterval(experienceAutoSlideTimer);
            experienceAutoSlideTimer = null;
        }
    }

    function restartAutoSlide() {
        startAutoSlide();
    }

    previousButton.onclick = function () {
        if (currentIndex > 0) {
            currentIndex--;
        } else {
            currentIndex = getMaxIndex();
        }
        updateCarousel();
        restartAutoSlide();
    };

    nextButton.onclick = function () {
        stepNext();
        restartAutoSlide();
    };

    if (!carousel.dataset.autoSlideBound) {
        carousel.dataset.autoSlideBound = "true";

        carousel.addEventListener("mouseenter", function () {
            stopAutoSlide();
        });

        carousel.addEventListener("mouseleave", function () {
            startAutoSlide();
        });

        window.addEventListener("resize", function () {
            currentIndex = Math.min(
                currentIndex,
                getMaxIndex()
            );

            createDots();
            updateCarousel();
        });
    }

    createDots();
    updateCarousel();
    startAutoSlide();
}

function initializeHomeExperienceCarousel() {
    initializeExperienceCarousel();
}
