(function () {
    document.addEventListener("DOMContentLoaded", function () {
        document.body.classList.add("page-loaded");

        // =================================================
        // 1. EFEK TULISAN MUNCUL PERLAHAN SAAT DI-SCROLL
        // =================================================
        const revealElements = document.querySelectorAll(
            ".hero-kicker, .hero-identity h1, .hero-details, .hero-contact, .education-heading, .experience-heading, .item-pengalaman"
        );

        const sectionHeadings = document.querySelectorAll(
            ".education-title, .experience-heading h1, #skill h1"
        );

        const revealObserver = new IntersectionObserver(
            function (entries) {
                entries.forEach(function (entry) {
                    if (entry.isIntersecting) {
                        if (
                            entry.target.classList.contains(
                                "section-heading-reveal"
                            )
                        ) {
                            entry.target.classList.add("show");
                        } else {
                            entry.target.classList.add("scroll-visible");
                            entry.target.classList.add("show");
                        }
                    } else {
                        // Reset saat keluar layar agar saat di-scroll kembali efek munculnya tetap hidup
                        if (
                            entry.target.classList.contains(
                                "section-heading-reveal"
                            )
                        ) {
                            entry.target.classList.remove("show");
                        } else {
                            entry.target.classList.remove("scroll-visible");
                        }
                    }
                });
            },
            {
                threshold: 0.12
            }
        );

        sectionHeadings.forEach(function (heading) {
            heading.classList.add("section-heading-reveal");
            revealObserver.observe(heading);
        });

        revealElements.forEach(function (element) {
            element.classList.add("scroll-reveal");
            revealObserver.observe(element);
        });

        // =================================================
        // 2. EFEK HALAMAN / SECTION SEBELUMNYA LAMA-LAMA
        //    MENGHILANG SAAT DI-SCROLL KE BAWAH
        // =================================================
        const sections = Array.from(document.querySelectorAll("main > section"));

        function updateSectionScrollFade() {
            const viewportHeight = window.innerHeight;

            sections.forEach(function (section) {
                const rect = section.getBoundingClientRect();

                // Jika section sedang ditinggalkan ke atas (scroll ke bawah melewati section ini)
                if (rect.top < 0 && rect.bottom > 0) {
                    // Hitung rasio seberapa banyak bagian bawah section yang masih tersisa di layar
                    const visibleRatio = rect.bottom / (viewportHeight * 0.75);
                    if (visibleRatio < 1) {
                        const clampedOpacity = Math.max(
                            0.05,
                            Math.min(1, Math.pow(visibleRatio, 1.35))
                        );
                        const blurPx = ((1 - clampedOpacity) * 5).toFixed(2);
                        section.style.opacity = clampedOpacity.toFixed(3);
                        section.style.filter = `blur(${blurPx}px)`;
                        return;
                    }
                }

                // Jika section baru mau masuk dari bawah layar
                if (rect.top > viewportHeight * 0.65 && rect.top < viewportHeight) {
                    const enterRatio =
                        (viewportHeight - rect.top) / (viewportHeight * 0.35);
                    const clampedOpacity = Math.max(
                        0.15,
                        Math.min(1, enterRatio)
                    );
                    section.style.opacity = clampedOpacity.toFixed(3);
                    section.style.filter = "blur(0px)";
                    return;
                }

                section.style.opacity = "1";
                section.style.filter = "blur(0px)";
            });
        }

        window.addEventListener("scroll", updateSectionScrollFade, {
            passive: true
        });
        window.addEventListener("resize", updateSectionScrollFade);
        updateSectionScrollFade();
    });

    // =================================================
    // 3. ANIMASI HURUF NAMA PADA PROFILE
    // =================================================
    const nameTitle = document.querySelector(".hero-identity h1");

    if (nameTitle && !nameTitle.classList.contains("name-animated")) {
        const text = nameTitle.textContent.trim();

        nameTitle.innerHTML = "";

        text.split("").forEach(function (letter, index) {
            const span = document.createElement("span");

            span.textContent = letter === " " ? "\u00A0" : letter;

            span.classList.add("name-letter");

            span.style.animationDelay = `${index * 45}ms`;

            nameTitle.appendChild(span);
        });

        nameTitle.classList.add("name-animated");
    }

    // =========================================================
    // 4. SKILL HANGING LANYARD (NATURAL & SUBTLE ELASTIC MOTION)
    // =========================================================
    const skillSection = document.getElementById("skill");
    const skillGrid = document.querySelector(".grid-skill");

    if (skillSection && skillGrid && !skillGrid.dataset.hangerBound) {
        skillGrid.dataset.hangerBound = "true";

        const hangingCards = Array.from(
            skillGrid.querySelectorAll(".cover-kartu")
        );

        const baseStringHeight = 56;

        const cardStates = hangingCards.map(function (card, index) {
            const restAngle = parseFloat(card.dataset.restAngle || "0");
            const stringEl = card.querySelector(".hanger-string");
            const clipEl = card.querySelector(".hanger-clip");
            const cardBoxEl = card.querySelector(".skill-card");

            if (stringEl) {
                stringEl.style.height = `${baseStringHeight}px`;
                stringEl.style.transformOrigin = "50% 0%";
            }

            return {
                el: card,
                stringEl: stringEl,
                clipEl: clipEl,
                cardBoxEl: cardBoxEl,
                offsetY: 0,
                velY: 0,
                stiffnessY: 0.11 + index * 0.015,
                dampingY: 0.76,
                weightFactor: index === 1 ? 1.15 : index === 0 ? 0.95 : 1.05,
                restAngle: restAngle,
                angleZ: restAngle,
                velZ: 0,
                stiffnessZ: 0.09,
                dampingZ: 0.80
            };
        });

        let lastScrollY = window.scrollY;
        let isAnimating = false;

        function startAnimationLoop() {
            if (!isAnimating) {
                isAnimating = true;
                requestAnimationFrame(animateSkillHangers);
            }
        }

        window.addEventListener(
            "scroll",
            function () {
                const currentScrollY = window.scrollY;
                const deltaY = currentScrollY - lastScrollY;
                lastScrollY = currentScrollY;

                const rect = skillSection.getBoundingClientRect();
                if (rect.bottom < -100 || rect.top > window.innerHeight + 100) {
                    return;
                }

                const clampedDelta = Math.max(-28, Math.min(28, deltaY));

                cardStates.forEach(function (state, index) {
                    state.velY += clampedDelta * 0.14 * state.weightFactor;

                    const swingDir = index % 2 === 0 ? 1 : -1;
                    state.velZ += clampedDelta * 0.018 * swingDir;
                });

                startAnimationLoop();
            },
            { passive: true }
        );

        cardStates.forEach(function (state) {
            state.el.addEventListener("mouseenter", function () {
                state.velY += 3.2;
                startAnimationLoop();
            });
        });

        function animateSkillHangers() {
            let stillMoving = false;

            cardStates.forEach(function (state) {
                const forceY = (0 - state.offsetY) * state.stiffnessY;
                state.velY = (state.velY + forceY) * state.dampingY;
                state.offsetY += state.velY;

                state.offsetY = Math.max(-8, Math.min(18, state.offsetY));

                const forceZ = (state.restAngle - state.angleZ) * state.stiffnessZ;
                state.velZ = (state.velZ + forceZ) * state.dampingZ;
                state.angleZ += state.velZ;

                const maxAngleOffset = 3.5;
                state.angleZ = Math.max(
                    state.restAngle - maxAngleOffset,
                    Math.min(state.restAngle + maxAngleOffset, state.angleZ)
                );

                if (
                    Math.abs(state.velY) > 0.02 ||
                    Math.abs(state.offsetY) > 0.05 ||
                    Math.abs(state.velZ) > 0.01 ||
                    Math.abs(state.angleZ - state.restAngle) > 0.02
                ) {
                    stillMoving = true;
                } else {
                    state.offsetY = 0;
                    state.velY = 0;
                    state.angleZ = state.restAngle;
                    state.velZ = 0;
                }

                const stringScale = Math.max(
                    0.75,
                    (baseStringHeight + state.offsetY) / baseStringHeight
                );

                if (state.stringEl) {
                    state.stringEl.style.transform = `scaleY(${stringScale.toFixed(3)})`;
                }

                if (state.clipEl) {
                    state.clipEl.style.transform = `translate3d(0, ${state.offsetY.toFixed(2)}px, 0)`;
                }

                if (state.cardBoxEl) {
                    state.cardBoxEl.style.transform = `translate3d(0, ${state.offsetY.toFixed(2)}px, 0)`;
                }

                state.el.style.transform = `rotateZ(${state.angleZ.toFixed(2)}deg)`;
            });

            if (stillMoving) {
                requestAnimationFrame(animateSkillHangers);
            } else {
                isAnimating = false;
            }
        }

        startAnimationLoop();
    }

    // =================================================
    // 5. EXPERIENCE POP-UP MODAL (CLICK TO OPEN DETAIL)
    // =================================================
    window.initExperienceInteractiveCards = function () {
        const cards = Array.from(
            document.querySelectorAll(".experience-card")
        );
        const popupOverlay = document.getElementById("experience-detail-popup");
        const closePopupBtn = document.getElementById("close-experience-popup");

        if (cards.length === 0) {
            return;
        }

        cards.forEach(function (card) {
            card.addEventListener("click", function (event) {
                if (
                    event.target.closest("a, button, form, input") ||
                    !popupOverlay
                ) {
                    return;
                }

                const title =
                    card.dataset.title ||
                    card.querySelector("h2")?.textContent ||
                    "";
                const institution =
                    card.dataset.institution ||
                    card.querySelector(".experience-institution")?.textContent ||
                    "";
                const period =
                    card.dataset.period ||
                    card.querySelector(".experience-period")?.textContent ||
                    "";
                const description =
                    card.dataset.description ||
                    card.querySelector(".experience-description")?.textContent ||
                    "";
                const image =
                    card.dataset.image ||
                    card.querySelector(".experience-image")?.getAttribute("src") ||
                    "";

                document.getElementById("popup-experience-title").textContent = title;
                document.getElementById("popup-experience-institution").textContent = institution;
                document.getElementById("popup-experience-period").textContent = period ? `📅 ${period}` : "";
                document.getElementById("popup-experience-description").textContent = description;

                const imgEl = document.getElementById("popup-experience-image");
                if (imgEl && image) {
                    imgEl.src = image;
                    imgEl.alt = title;
                    imgEl.style.display = "block";
                } else if (imgEl) {
                    imgEl.style.display = "none";
                }

                popupOverlay.classList.add("active");
                popupOverlay.setAttribute("aria-hidden", "false");
            });
        });

        if (popupOverlay && !popupOverlay.dataset.bound) {
            popupOverlay.dataset.bound = "true";

            if (closePopupBtn) {
                closePopupBtn.addEventListener("click", function () {
                    popupOverlay.classList.remove("active");
                    popupOverlay.setAttribute("aria-hidden", "true");
                });
            }

            popupOverlay.addEventListener("click", function (event) {
                if (event.target === popupOverlay) {
                    popupOverlay.classList.remove("active");
                    popupOverlay.setAttribute("aria-hidden", "true");
                }
            });

            document.addEventListener("keydown", function (event) {
                if (
                    event.key === "Escape" &&
                    popupOverlay.classList.contains("active")
                ) {
                    popupOverlay.classList.remove("active");
                    popupOverlay.setAttribute("aria-hidden", "true");
                }
            });
        }
    };
})();
