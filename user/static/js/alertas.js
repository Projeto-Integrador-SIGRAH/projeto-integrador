
function formatarData(data) {
    return new Date(data).toLocaleDateString("pt-BR");
}

let alertas = [];
let alertaSelecionado = null;


async function listarAlertas() {
    const tabela = document.querySelector("#lista-alertas");

    try {
        const response = await fetch(tabela.dataset.apiUrl);

        if (!response.ok) {
            throw new Error("Erro ao buscar os alertas.");
        }

        alertas = await response.json();

        renderizarAlertas(alertas);

        console.log(alertas);

    } catch (error) {
        console.log(error);
    }
}

listarAlertas();


function renderizarAlertas(alertas) {
    const tabela = document.querySelector("#lista-alertas");

    tabela.innerHTML = "";

    alertas.forEach((alerta) => {
        const linha = document.createElement("tr");

        linha.classList.add(
            "border",
            "border-gray-200",
            "cursor-pointer"
        );

        linha.dataset.alertaId = alerta.id;

        const campos = [
            alerta.codigo,
            alerta.status,
            alerta.gravidade?.split("_")[1],
            alerta.tipo,
            alerta.reportado_em
                ? formatarData(alerta.reportado_em)
                : "-"
        ];

        campos.forEach((valor) => {
            const coluna = document.createElement("td");

            coluna.classList.add("px-3", "py-3", "text-sm");
            coluna.textContent = valor ?? "-";

            linha.appendChild(coluna);
        });

        tabela.appendChild(linha);
    });
}


const tabela = document.querySelector("#lista-alertas");
const containerTabela = document.querySelector("#container-tabela");
const painelDetalhe = document.querySelector("#painel-detalhe");

tabela.addEventListener("click", (event) => {
    const linha = event.target.closest("tr");

    if (!linha || !linha.dataset.alertaId) return;

    const linhaAnterior = tabela.querySelector(".linha-selecionada");

    if (linhaAnterior) {
        linhaAnterior.classList.remove(
            "bg-yellow-500",
            "linha-selecionada"
        );
    }

    linha.classList.add("bg-yellow-500", "linha-selecionada");

    const alertaId = linha.dataset.alertaId;

    alertaSelecionado = alertas.find(
        (alerta) => String(alerta.id) === alertaId
    );

    console.log("Alerta selecionado:", alertaSelecionado);

    painelDetalhe.querySelectorAll("[data-campo]").forEach((elemento) => {
        const campo = elemento.dataset.campo;
        let valor = alertaSelecionado[campo];

        if (campo === "reportado_em" && valor) {
            valor = new Date(valor).toLocaleString("pt-BR");
        }

        if (campo === "gravidade" && valor) {
            valor = valor.split("_")[1];
        }

        elemento.textContent = valor ?? "-";
    });

    const cardCodigo = painelDetalhe.querySelector("#card-codigo");
    const cardStatus = painelDetalhe.querySelector("#card-status-detalhe");

    if (cardCodigo) {
        cardCodigo.textContent = alertaSelecionado.codigo ?? "-";
    }

    if (cardStatus) {
        cardStatus.textContent = alertaSelecionado.status ?? "-";
    }


    containerTabela.classList.remove("w-full");
    containerTabela.classList.add("w-7/10");

    painelDetalhe.classList.remove("hidden");
    painelDetalhe.classList.add("flex");
});
