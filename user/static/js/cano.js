// Abertura e fechamento dos modais
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

//* listagem de canos3
const tabelaCanos = document.querySelector("#lista-canos");
const formularioFiltros = document.querySelector("#filtros-canos");

async function listarCanos(filtros = new URLSearchParams()) {
    const url = new URL(tabelaCanos.dataset.apiUrl, window.location.origin);
    url.search = filtros.toString();
    const response = await fetch(url);

    if (!response.ok){
        throw new Error("Erro ao buscar os canos.")
    }

    const canos = await response.json()
    renderizarCanos(canos)

    return canos;
}


function preencherOpcoes(select, valores) {
    const valoresUnicos = [...new Set(valores.filter(Boolean))]
        .sort((a, b) => String(a).localeCompare(String(b), "pt-BR", { numeric: true }));

    valoresUnicos.forEach((valor) => {
        select.add(new Option(valor, valor));
    });
}


listarCanos()
    .then((canos) => {
        preencherOpcoes(
            document.querySelector("#filtro-codigo"),
            canos.map((cano) => cano.codigo),
        );
        preencherOpcoes(
            document.querySelector("#filtro-material"),
            canos.map((cano) => cano.material),
        );
        preencherOpcoes(
            document.querySelector("#filtro-diametro"),
            canos.map((cano) => cano.diametro),
        );
    })
    .catch((error) => console.error(error));

formularioFiltros.addEventListener("submit", (event) => {
    event.preventDefault();
    const filtros = new URLSearchParams(new FormData(formularioFiltros));
    listarCanos(filtros).catch((error) => console.error(error));
});

formularioFiltros.addEventListener("reset", () => {
    window.requestAnimationFrame(() => {
        listarCanos().catch((error) => console.error(error));
    });
});


function renderizarCanos(canos){
    tabelaCanos.innerHTML = ""

    canos.forEach((cano) => {
        const linha = document.createElement("tr")

        linha.classList.add("border", "border-gray-200")

        const campos = [
            cano.codigo,
            cano.material,
            `${cano.diametro} mm`,
            cano.status,
            `${formatarData(cano.atualizado_em)}`,
        ]

        campos.forEach((valor) => {
            const coluna = document.createElement("td")

            coluna.classList.add("px-3", "py-3", "text-sm")
            coluna.textContent = valor ?? "-"

            linha.appendChild(coluna)
        })

        tabelaCanos.appendChild(linha)
    })
}

function formatarData(data) {
    return new Date(data).toLocaleString("pt-BR");
}

// Create & Update de canos 
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