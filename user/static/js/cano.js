const modal = document.querySelector("#modal-cano");
const btnAdicionar = document.querySelector("#btn-adicionar-cano");
const btnFechar = document.querySelector("#btn-fechar-modal");

btnAdicionar.addEventListener("click", () => {
    modal.showModal();
});

btnFechar.addEventListener("click", () => {
    modal.close();
});

const form = document.querySelector("#form-cano");

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    if (!form.reportValidity()) return;

    const formData = new FormData(form);
    const payload = Object.fromEntries(formData.entries());

    try {
        const response = await fetch(form.dataset.apiUrl, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "X-CSRFToken": formData.get("csrfmiddlewaretoken"),
            },
            body: JSON.stringify(payload),
        });

        const data = await response.json();

        if (!response.ok) {
            console.error("Erro ao cadastrar:", data);
            return;
        }

        console.log("Cano cadastrado:", data);

        form.reset();
        modal.close();

    } catch (error) {
        console.error("Erro na requisição:", error);
    }
});