document.addEventListener("DOMContentLoaded", function () {

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

    // lanjutkan kode JS kamu yang sekarang...


    let currentIndex = 0;


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

        const cardWidth = cards[0].getBoundingClientRect().width;

        const gap = parseFloat(
            window.getComputedStyle(track).gap
        ) || 0;

        const offset = currentIndex * (cardWidth + gap);

        track.style.transform =
            `translateX(-${offset}px)`;

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

            });

            dotsContainer.appendChild(dot);
        }

        updateDots();
    }


    function updateDots() {

        const dots =
            document.querySelectorAll(".carousel-dot");

        dots.forEach(function (dot, index) {

            dot.classList.toggle(
                "active",
                index === currentIndex
            );

        });
    }


    previousButton.addEventListener(
        "click",
        function () {

            if (currentIndex > 0) {

                currentIndex--;

                updateCarousel();

            }

        }
    );


    nextButton.addEventListener(
        "click",
        function () {

            if (currentIndex < getMaxIndex()) {

                currentIndex++;

                updateCarousel();

            }

        }
    );


    window.addEventListener(
        "resize",
        function () {

            currentIndex = Math.min(
                currentIndex,
                getMaxIndex()
            );

            createDots();
            updateCarousel();

        }
    );


    createDots();
    updateCarousel();

});