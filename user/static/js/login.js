document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("#login-form");
    const errors = document.getElementById("form-errors");

    const showMessage = (element, message) => {
        element.textContent = message;
        element.classList.remove("hidden");
    };

    form.addEventListener("submit", async (event) => {
        event.preventDefault();

        const formData = new FormData(form);
        const payload  = Object.fromEntries(formData.entries());

        try {
            const resposta = await fetch(form.dataset.apiUrl, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                    "X-CSRFToken": formData.get("csrfmiddlewaretoken"),
                },
                body: JSON.stringify(payload),
            });

            const data = await resposta.json();

            if (!resposta.ok) {
                showMessage(errors, Object.values(data).flat().join(" ") || "Não foi possível concluir o login.");
                return;
            }

            // https://dev.to/jumaschion/-cache-session-storage-local-storage-e-cookies-360p
            // sessionStorage.setItem("access", dados.access);
            // sessionStorage.setItem("refresh", dados.refresh);

            window.location.href = "/"

        } catch (erro) {
            console.error("Erro ao realizar login:", erro);
            showMessage(errors, "Não foi possível conectar ao serviço de login.");
        }
    });
});