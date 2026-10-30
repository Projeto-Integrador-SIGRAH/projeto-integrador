document.addEventListener("DOMContentLoaded", () => {
    const indicador = document.getElementById("indicador");
    const admin = document.getElementById("admin");
    const cidadao = document.getElementById("cidadao");
    const form = document.getElementById("registration-form");

    const animateNavigation = (link, transform) => {
        if (!link || !indicador) return;

        link.addEventListener("click", (event) => {
            event.preventDefault();
            indicador.style.transform = transform;
            window.setTimeout(() => {
                window.location.href = link.href;
            }, 300);
        });
    };

    animateNavigation(admin, "translateX(100%)");
    animateNavigation(cidadao, "translateX(-100%)");

    if (!form) return;

    const errors = document.getElementById("form-errors");
    const success = document.getElementById("form-success");
    const submitButton = form.querySelector('button[type="submit"]');

    const showMessage = (element, message) => {
        element.textContent = message;
        element.classList.remove("hidden");
    };

    form.addEventListener("submit", async (event) => {
        event.preventDefault();
        errors.classList.add("hidden");
        success.classList.add("hidden");

        if (!form.reportValidity()) return;

        const payload = Object.fromEntries(new FormData(form).entries());
        submitButton.disabled = true;
        submitButton.classList.add("cursor-not-allowed", "opacity-70");

        try {
            const response = await fetch(form.dataset.apiUrl, {
                method: "POST",
                headers: { "Content-Type": "application/json", Accept: "application/json" },
                body: JSON.stringify(payload),
            });
            const data = await response.json();

            if (!response.ok) {
                const message = Object.values(data).flat().join(" ")
                    || "Não foi possível concluir o cadastro.";
                showMessage(errors, message);
                return;
            }

            // form.reset();
            showMessage(success, data.detail);
            window.setTimeout(() => {
                window.location.href = form.dataset.loginUrl;
            }, 700);
        } catch (error) {
            showMessage(errors, "Não foi possível conectar ao serviço de cadastro.");
        } finally {
            submitButton.disabled = false;
            submitButton.classList.remove("cursor-not-allowed", "opacity-70");
        }
    });
});
