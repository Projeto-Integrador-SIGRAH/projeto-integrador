const modalAlerta = document.querySelector("#modal-alerta");
const formAlerta = document.querySelector("#form-alerta");
const btnCloseAlerta = modalAlerta?.querySelector("#close-button-modal");
const btnAlertar = document.querySelector("#btnAlertar");

btnAlertar?.addEventListener("click", (event) => {
    event.preventDefault();


    if (!modalAlerta || !formAlerta) return;

    if (!window.canoSelecionado) {
        console.error("O cano selecionado não está disponível em window.");
        return;
    }

    formAlerta.reset();
    modalAlerta.showModal();

});

btnCloseAlerta?.addEventListener("click", (event) => {
    event.preventDefault();

    modalAlerta.close();

});

formAlerta?.addEventListener("submit", async (event) => {
    event.preventDefault();

    if (!formAlerta.reportValidity()) return;

    const formData = new FormData(formAlerta);

    const payload = Object.fromEntries(formData.entries());

    payload.codigo_id = window.canoSelecionado.id;

    try {
        const response = await fetch(formAlerta.action, {
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
            console.error("Erro ao criar alerta:", data);
            return;
        }

        modalAlerta.close();
        formAlerta.reset();
        await listarAlertas();

    } catch (error) {
        console.error("Erro na requisição:", error);
    }
});

function formatarData(data) {
    return new Date(data).toLocaleDateString("pt-BR");
}

let alertas = [];
let alertaSelecionado = null;


async function listarAlertas() {
    const tabelaAlertas = document.querySelector("#lista-alertas");

    if (!tabelaAlertas) return;

    try {
        const response = await fetch(tabelaAlertas.dataset.apiUrl);

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
    const tabelaAlertas = document.querySelector("#lista-alertas");

    tabelaAlertas.innerHTML = "";

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

        tabelaAlertas.appendChild(linha);
    });
}


const tabelaAlertas = document.querySelector("#lista-alertas");
const containerAlertas = document.querySelector("#container-tabela");
const painelAlertas = document.querySelector("#painel-detalhe");

tabelaAlertas?.addEventListener("click", (event) => {
    const linha = event.target.closest("tr");

    if (!linha || !linha.dataset.alertaId) return;

    const linhaAnterior = tabelaAlertas.querySelector(".linha-selecionada");

    if (linhaAnterior) {
        linhaAnterior.classList.remove(
            "bg-yellow-400",
            "linha-selecionada"
        );
    }

    linha.classList.add("bg-yellow-400", "linha-selecionada");

    const alertaId = linha.dataset.alertaId;

    alertaSelecionado = alertas.find(
        (alerta) => String(alerta.id) === alertaId
    );

    console.log("Alerta selecionado:", alertaSelecionado);

    painelAlertas.querySelectorAll("[data-campo]").forEach((elemento) => {
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

    const cardCodigo = painelAlertas.querySelector("#card-codigo");
    const cardStatus = painelAlertas.querySelector("#card-status-detalhe");

    if (cardCodigo) {
        cardCodigo.textContent = alertaSelecionado.codigo ?? "-";
    }

    if (cardStatus) {
        cardStatus.textContent = alertaSelecionado.status ?? "-";
    }


    containerAlertas.classList.remove("w-full");
    containerAlertas.classList.add("w-7/10");

    painelAlertas.classList.remove("hidden");
    painelAlertas.classList.add("flex");
});
