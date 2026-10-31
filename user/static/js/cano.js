const modal = document.querySelector("#modal-cano");
const botoesAbrirModal = document.querySelectorAll(".btn-abrir-modal")
const botoesFecharModal = document.querySelectorAll(".btn-fechar-modal");

botoesAbrirModal.forEach((botao) => {
    botao.addEventListener("click", () => {
        const modalID = botao.dataset.modal
        const modal = document.getElementById(modalID)

        modal.showModal();
    });
})


botoesFecharModal.forEach((botao) => {
    botao.addEventListener("click", () => {
        const modalID = botao.dataset.modal
        const modal = document.getElementById(modalID)

        modal.close();
    });
})

const form = document.querySelector("#form-cano");

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    if (!form.reportValidity()) return;

    const formData = new FormData(form);
    const payload = Object.fromEntries(formData.entries());

    try {
        const response = await fetch(form.dataset.apiUrl, {
            method: form.dataset.method,
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