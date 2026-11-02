// Abertura e fechamento dos modais
const modal = document.querySelector("#modal-cano");
const btnEditarCano = document.querySelector("#btn-editar-cano")
// const btnFecharModal = document.querySelectorAll("#btn-fechar-modal");

btnEditarCano?.addEventListener("click", () => {
    const modalID = botao.dataset.modal
    const modal = document.getElementById(modalID)

    modal.showModal();
});


// btnFecharModal.addEventListener("click", () => {
//     const modalID = botao.dataset.modal
//     const modal = document.getElementById(modalID)

//     modal.close();
// });

function formatarData(data) {
    return new Date(data).toLocaleDateString("pt-BR");
}

let canos = []
let canoSelecionado = null

async function listarCanos() {
    const tabela = document.querySelector("#lista-canos")

    try {
        const response = await fetch(tabela.dataset.apiUrl);

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

// Detalhe do cano
const tabela = document.querySelector("#lista-canos");
const containerTabela = document.querySelector("#container-tabela");
const painelDetalhe = document.querySelector("#painel-detalhe");

tabela.addEventListener("click", (event) => {

    const linha = event.target.closest("tr");

    if (!linha) return;

    // Destacar linha selecionada
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


