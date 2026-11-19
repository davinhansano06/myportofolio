(function () {
    document.addEventListener("DOMContentLoaded", function () {
        document.body.classList.add("page-loaded");

        // =================================================
        // 1. EFEK TULISAN MUNCUL PERLAHAN SAAT DI-SCROLL
        // =================================================
        const revealElements = document.querySelectorAll(
            ".hero-kicker, .hero-identity h1, #contact h1, .hero-details, .hero-contact, .contact-lead, .wa-preview-card, .contact-form-panel, .education-heading, .experience-heading, .item-pengalaman"
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

    // =========================================================
    // 6. INTERACTIVE PRIVATE INBOX CONTACT FORM & OWNER INBOX
    //    (100% Phone Number Hidden from Public HTML/JS)
    // =========================================================
    function getCsrfToken() {
        const tokenInput = document.querySelector(
            "input[name='csrfmiddlewaretoken']"
        );
        if (tokenInput && tokenInput.value) {
            return tokenInput.value;
        }
        const match = document.cookie.match(/(?:^|;\s*)csrftoken=([^;]+)/);
        return match ? decodeURIComponent(match[1]) : "";
    }

    function escapeHtmlSafe(value) {
        return String(value ?? "")
            .replaceAll("&", "&amp;")
            .replaceAll("<", "&lt;")
            .replaceAll(">", "&gt;")
            .replaceAll('"', "&quot;")
            .replaceAll("'", "&#39;");
    }

    function buildReplyLink(contactRaw, senderName, topic) {
        const cleaned = (contactRaw || "").trim();
        if (cleaned.includes("@")) {
            const subject = encodeURIComponent(`Re: ${topic} - Davin Tristan Hansano`);
            const body = encodeURIComponent(
                `Halo ${senderName},\n\nTerima kasih telah menghubungi saya melalui website portofolio mengenai "${topic}". `
            );
            return {
                type: "email",
                label: "✉️ Balas via Email",
                url: `mailto:${cleaned}?subject=${subject}&body=${body}`
            };
        }

        let digits = cleaned.replace(/\D/g, "");
        if (digits.startsWith("0")) {
            digits = "62" + digits.slice(1);
        } else if (digits.startsWith("8")) {
            digits = "62" + digits;
        }

        if (digits.length >= 9) {
            const text = encodeURIComponent(
                `Halo ${senderName}! 👋 Perkenalkan saya Davin Tristan Hansano. Terima kasih sudah meninggalkan pesan di portofolio saya terkait *${topic}*.`
            );
            return {
                type: "whatsapp",
                label: "💬 Balas ke WhatsApp Pengunjung",
                url: `https://wa.me/${digits}?text=${text}`
            };
        }

        return null;
    }

    const ownerInboxSection = document.getElementById("owner-inbox-section");
    const ownerInboxList = document.getElementById("owner-inbox-list");
    const ownerInboxCount = document.getElementById("owner-inbox-count");

    async function loadOwnerInbox() {
        if (!ownerInboxSection || !ownerInboxList) {
            return;
        }

        try {
            const response = await fetch("/api/v1/messages/", {
                headers: { Accept: "application/json" }
            });

            if (!response.ok) {
                ownerInboxList.innerHTML =
                    '<p class="owner-inbox-empty">Tidak dapat memuat pesan inbox.</p>';
                return;
            }

            const messages = await response.json();
            const unreadCount = messages.filter(function (m) {
                return !m.is_read;
            }).length;

            if (ownerInboxCount) {
                ownerInboxCount.textContent = `${messages.length} Pesan (${unreadCount} Baru)`;
            }

            if (messages.length === 0) {
                ownerInboxList.innerHTML =
                    '<p class="owner-inbox-empty">Belum ada pesan masuk di inbox portofolio Anda.</p>';
                return;
            }

            ownerInboxList.innerHTML = "";

            messages.forEach(function (item) {
                const card = document.createElement("article");
                card.className = `owner-msg-card ${item.is_read ? "is-read" : "is-unread"}`;

                const replyInfo = buildReplyLink(
                    item.sender_contact,
                    item.sender_name,
                    item.topic
                );

                const orgLabel = item.sender_org
                    ? `<span class="owner-msg-org">&middot; ${escapeHtmlSafe(item.sender_org)}</span>`
                    : "";

                const replyButtonHtml = replyInfo
                    ? `<a href="${replyInfo.url}" target="_blank" rel="noopener noreferrer" class="button owner-reply-btn">${replyInfo.label}</a>`
                    : "";

                card.innerHTML = `
                    <div class="owner-msg-top">
                        <div class="owner-msg-sender">
                            <strong>${escapeHtmlSafe(item.sender_name)}</strong>
                            ${orgLabel}
                            <span class="owner-msg-topic">${escapeHtmlSafe(item.topic)}</span>
                        </div>
                        <span class="owner-msg-time">${escapeHtmlSafe(item.created_at_display)}</span>
                    </div>
                    <p class="owner-msg-contact">
                        Kontak Pengunjung: <strong>${escapeHtmlSafe(item.sender_contact)}</strong>
                    </p>
                    <p class="owner-msg-body">${escapeHtmlSafe(item.message)}</p>
                    <div class="owner-msg-actions">
                        ${replyButtonHtml}
                        <button type="button" class="button button-secondary owner-toggle-read-btn" data-id="${item.id}" data-read="${item.is_read}">
                            ${item.is_read ? "Tandai Belum Dibaca" : "✓ Tandai Dibaca"}
                        </button>
                        <button type="button" class="button button-danger owner-delete-msg-btn" data-id="${item.id}">
                            Hapus
                        </button>
                    </div>
                `;

                ownerInboxList.appendChild(card);
            });

            ownerInboxList
                .querySelectorAll(".owner-toggle-read-btn")
                .forEach(function (btn) {
                    btn.addEventListener("click", async function () {
                        const msgId = btn.dataset.id;
                        const currentlyRead = btn.dataset.read === "true";
                        await fetch(`/api/v1/messages/${msgId}/`, {
                            method: "PATCH",
                            headers: {
                                "Content-Type": "application/json",
                                "X-CSRFToken": getCsrfToken()
                            },
                            body: JSON.stringify({ is_read: !currentlyRead })
                        });
                        loadOwnerInbox();
                    });
                });

            ownerInboxList
                .querySelectorAll(".owner-delete-msg-btn")
                .forEach(function (btn) {
                    btn.addEventListener("click", async function () {
                        const msgId = btn.dataset.id;
                        await fetch(`/api/v1/messages/${msgId}/`, {
                            method: "DELETE",
                            headers: {
                                "X-CSRFToken": getCsrfToken()
                            }
                        });
                        loadOwnerInbox();
                    });
                });
        } catch (err) {
            console.error("Failed to load owner inbox:", err);
        }
    }

    const waForm = document.getElementById("whatsapp-contact-form");
    if (waForm && !waForm.dataset.waBound) {
        waForm.dataset.waBound = "true";

        const nameInput = document.getElementById("wa-sender-name");
        const contactInput = document.getElementById("wa-sender-contact");
        const orgInput = document.getElementById("wa-sender-org");
        const messageInput = document.getElementById("wa-message-input");
        const charCounter = document.getElementById("wa-char-counter");
        const livePreviewText = document.getElementById("wa-live-preview-text");
        const livePreviewBubble = document.getElementById("wa-live-preview-bubble");
        const previewStatus = document.getElementById("wa-preview-status");
        const topicChips = Array.from(document.querySelectorAll(".wa-chip"));
        const feedbackEl = document.getElementById("wa-form-feedback");
        const submitBtn = document.getElementById("wa-submit-btn");
        const submitBtnText = document.getElementById("wa-submit-btn-text");

        let selectedTopic = "Kolaborasi Proyek";
        let lastAutoTemplate = messageInput ? messageInput.value.trim() : "";

        function composePreviewMessage() {
            const senderName = nameInput ? nameInput.value.trim() : "";
            const senderContact = contactInput ? contactInput.value.trim() : "";
            const senderOrg = orgInput ? orgInput.value.trim() : "";
            const rawMessage = messageInput ? messageInput.value.trim() : "";

            let headerLine = "Halo Davin! 👋";
            if (senderName && senderOrg) {
                headerLine += `\nPerkenalkan saya ${senderName} (${senderOrg}).`;
            } else if (senderName) {
                headerLine += `\nPerkenalkan saya ${senderName}.`;
            }

            const contactLine = senderContact
                ? `\nKontak balasan: ${senderContact}`
                : "";
            const topicLine = selectedTopic ? `\nTopik: ${selectedTopic}` : "";
            const bodyLine = rawMessage ? `\n\n${rawMessage}` : "";

            return `${headerLine}${topicLine}${contactLine}${bodyLine}`;
        }

        function updateLivePreviewAndCounter() {
            if (messageInput && charCounter) {
                const len = messageInput.value.length;
                charCounter.textContent = `${len} / 500`;
                charCounter.classList.toggle("wa-char-near-limit", len >= 450);
            }

            if (livePreviewText) {
                livePreviewText.textContent = composePreviewMessage();
                if (livePreviewBubble) {
                    livePreviewBubble.classList.remove("wa-bubble-pulse");
                    void livePreviewBubble.offsetWidth;
                    livePreviewBubble.classList.add("wa-bubble-pulse");
                }
            }
        }

        topicChips.forEach(function (chip) {
            chip.addEventListener("click", function () {
                topicChips.forEach(function (c) {
                    c.classList.remove("active");
                });
                chip.classList.add("active");
                selectedTopic = chip.dataset.topic || "";

                const newTemplate = chip.dataset.template || "";
                if (
                    messageInput &&
                    newTemplate &&
                    (messageInput.value.trim() === "" ||
                        messageInput.value.trim() === lastAutoTemplate)
                ) {
                    messageInput.value = newTemplate;
                    lastAutoTemplate = newTemplate;
                }

                updateLivePreviewAndCounter();
            });
        });

        [nameInput, contactInput, orgInput, messageInput].forEach(function (inputEl) {
            if (inputEl) {
                inputEl.addEventListener("input", function () {
                    if (feedbackEl) {
                        feedbackEl.classList.add("hide");
                    }
                    if (previewStatus) {
                        previewStatus.textContent = "Live Preview ✓✓";
                    }
                    updateLivePreviewAndCounter();
                });
            }
        });

        waForm.addEventListener("submit", async function (event) {
            event.preventDefault();

            const senderName = nameInput ? nameInput.value.trim() : "";
            const senderContact = contactInput ? contactInput.value.trim() : "";
            const senderOrg = orgInput ? orgInput.value.trim() : "";
            const rawMessage = messageInput ? messageInput.value.trim() : "";

            if (!senderName) {
                if (feedbackEl) {
                    feedbackEl.textContent = "Mohon isi nama Anda terlebih dahulu.";
                    feedbackEl.className = "wa-form-feedback wa-feedback-error";
                }
                if (nameInput) nameInput.focus();
                return;
            }

            if (!senderContact) {
                if (feedbackEl) {
                    feedbackEl.textContent =
                        "Mohon cantumkan nomor WhatsApp atau Email Anda agar Davin dapat membalas pesan Anda.";
                    feedbackEl.className = "wa-form-feedback wa-feedback-error";
                }
                if (contactInput) contactInput.focus();
                return;
            }

            if (!rawMessage) {
                if (feedbackEl) {
                    feedbackEl.textContent = "Mohon tulis pesan Anda terlebih dahulu.";
                    feedbackEl.className = "wa-form-feedback wa-feedback-error";
                }
                if (messageInput) messageInput.focus();
                return;
            }

            if (submitBtn) submitBtn.disabled = true;
            if (submitBtnText) submitBtnText.textContent = "Mengirim Pesan...";

            try {
                const response = await fetch("/api/v1/messages/", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        Accept: "application/json",
                        "X-CSRFToken": getCsrfToken()
                    },
                    body: JSON.stringify({
                        sender_name: senderName,
                        sender_contact: senderContact,
                        sender_org: senderOrg,
                        topic: selectedTopic,
                        message: rawMessage
                    })
                });

                if (!response.ok) {
                    throw new Error("Gagal mengirim pesan.");
                }

                if (feedbackEl) {
                    feedbackEl.textContent =
                        "✓ Pesan berhasil terkirim ke inbox pribadi Davin! Davin akan segera menghubungi kontak Anda.";
                    feedbackEl.className = "wa-form-feedback wa-feedback-success";
                }

                if (previewStatus) {
                    previewStatus.textContent = "Terkirim ke Inbox Davin ✓✓";
                }

                if (nameInput) nameInput.value = "";
                if (contactInput) contactInput.value = "";
                if (orgInput) orgInput.value = "";

                if (typeof window.showToast === "function") {
                    window.showToast(
                        "Pesan Terkirim!",
                        "Pesan Anda telah disimpan secara aman di inbox Davin.",
                        "success"
                    );
                }

                loadOwnerInbox();
            } catch (err) {
                if (feedbackEl) {
                    feedbackEl.textContent =
                        "Terjadi kesalahan saat mengirim pesan. Silakan coba lagi.";
                    feedbackEl.className = "wa-form-feedback wa-feedback-error";
                }
            } finally {
                if (submitBtn) submitBtn.disabled = false;
                if (submitBtnText) submitBtnText.textContent = "Kirim ke Inbox Davin";
            }
        });

        updateLivePreviewAndCounter();
    }

    loadOwnerInbox();
})();
