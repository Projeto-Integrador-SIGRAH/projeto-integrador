const modal = document.querySelector("#modal-cano");
const btnEditarCano = document.querySelector("#btn-editar-cano")
const modelForm = document.querySelector("#form-cano")
const buttonCloseModal = document.querySelector("#close-button-modal")
const modalTitle = document.querySelector("#titulo-modal")
const submitButton = document.querySelector("#submit-button")

btnEditarCano?.addEventListener("click", () => {
    modalTitle.textContent = "Editar Cano"
    submitButton.textContent = "Salvar"
    modelForm.reset();
    preencherFormulario(canoSelecionado, modelForm);
    modelForm.action += canoSelecionado.id + "/"
    modelForm.dataset.method = "PATCH"
    modal.showModal();
});

buttonCloseModal?.addEventListener("click", () => {
    modal.close();
});

submitButton?.addEventListener("click", async (event) => {
    event.preventDefault();

    if (!modelForm.reportValidity()) return;

    const formData = new FormData(modelForm);

    const payload = Object.fromEntries(formData.entries());

    try {
        const response = await fetch(modelForm.action, {
            method: modelForm.dataset.method,
            headers: {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "X-CSRFToken": formData.get("csrfmiddlewaretoken"),
            },
            body: JSON.stringify(payload),
        });

        const data = await response.json();

        if (!response.ok) {
            console.error("Erro ao editar:", data);
            return;
        }

        modal.close();

        await listarCanos();

    } catch (error) {
        console.error("Erro na requisição:", error);
    }

});

function preencherFormulario(dados, formulario) {
    Object.entries(dados).forEach(([campo, valor]) => {
        const elemento = formulario.elements.namedItem(campo);

        if (elemento) {
            elemento.value = valor ?? "";
        }
    });
}

function formatarData(data) {
    return new Date(data).toLocaleDateString("pt-BR");
}

let canos = []
let canoSelecionado = null

async function listarCanos() {
    const tabela = document.querySelector("#lista-canos")

    try {
        const filtros = arguments[0] || new URLSearchParams();
        const url = new URL(tabela.dataset.apiUrl, window.location.origin);
        url.search = filtros.toString();
        const response = await fetch(url);

        if (!response.ok){
            throw new Error("Erro ao buscar os canos.")
        }

        canos = await response.json()

        renderizarCanos(canos)

        console.log(canos)
    } catch(error){
        console.log(error);
    }
}

listarCanos()
    .then(() => {
        preencherOpcoesFiltro();
    });

function preencherOpcoesFiltro() {
    const selectCodigo = document.querySelector("#filtro-codigo");
    const selectMaterial = document.querySelector("#filtro-material");
    const selectDiametro = document.querySelector("#filtro-diametro");

    if (!selectCodigo || !selectMaterial || !selectDiametro) return;

    preencherOpcoes(selectCodigo, canos.map((cano) => cano.codigo));
    preencherOpcoes(selectMaterial, canos.map((cano) => cano.material));
    preencherOpcoes(selectDiametro, canos.map((cano) => cano.diametro));
}

function preencherOpcoes(select, valores) {
    const valoresUnicos = [...new Set(valores.filter(Boolean))]
        .sort((a, b) => String(a).localeCompare(String(b), "pt-BR", { numeric: true }));

    valoresUnicos.forEach((valor) => {
        select.add(new Option(valor, valor));
    });
}

const formularioFiltros = document.querySelector("#filtros-canos");

formularioFiltros?.addEventListener("submit", (event) => {
    event.preventDefault();
    const filtros = new URLSearchParams(new FormData(formularioFiltros));
    listarCanos(filtros).catch((error) => console.error(error));
});

formularioFiltros?.addEventListener("reset", () => {
    window.requestAnimationFrame(() => {
        listarCanos().catch((error) => console.error(error));
    });
});

function renderizarCanos(canos){
    const tabela = document.querySelector("#lista-canos")

    tabela.innerHTML = ""

    canos.forEach((cano) => {
        const linha = document.createElement("tr")

        linha.classList.add("border", "border-gray-200", "cursor-pointer")

        linha.dataset.canoId = cano.id

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

        tabela.appendChild(linha)
    })
}

const tabela = document.querySelector("#lista-canos");
const containerTabela = document.querySelector("#container-tabela");
const painelDetalhe = document.querySelector("#painel-detalhe");

tabela.addEventListener("click", (event) => {

    const linha = event.target.closest("tr");

    if (!linha) return;

    const linhaAnterior = tabela.querySelector(".linha-selecionada");

    if (linhaAnterior) {
        linhaAnterior.classList.remove("bg-sky-500", "linha-selecionada");
    }

    linha.classList.add("bg-sky-500", "linha-selecionada");

    const canoId = linha.dataset.canoId;

    canoSelecionado = canos.find(
        (cano) => String(cano.id) === canoId
    );

    console.log("Cano selecionado:", canoSelecionado);

    painelDetalhe.querySelectorAll("[data-campo]").forEach((elemento) => {
        const campo = elemento.dataset.campo;
        let valor = canoSelecionado[campo];

        if (["data_instalacao", "criado_em", "atualizado_em"].includes(campo) && valor) {
            valor = formatarData(valor);
        }

        elemento.textContent = valor ?? "-";
    });

    containerTabela.classList.remove("w-full");
    containerTabela.classList.add("w-7/10");

    painelDetalhe.classList.remove("hidden");
    painelDetalhe.classList.add("flex");
});


