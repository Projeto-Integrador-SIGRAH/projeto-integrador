async function listarAlertas() {
    const tabelaCorpo = document.querySelector("#lista-alertas");
    if (!tabelaCorpo) return;

    try {
        const response = await fetch(tabelaCorpo.dataset.apiUrl);

        if (!response.ok) {
            throw new Error("Erro ao buscar os alertas.");
        }

        const alertas = await response.json();
        renderizarAlertas(alertas);
    } catch (error) {
        console.error(error);
    }
}

listarAlertas();

function renderizarAlertas(alertas) {
    const tabelaCorpo = document.querySelector("#lista-alertas");
    tabelaCorpo.innerHTML = "";

    if (alertas.length === 0) {
        const linhaVazia = document.createElement("tr");
        linhaVazia.innerHTML = `<td class="px-3 py-3 text-sm text-gray-500 text-center" colspan="4">Nenhum alerta enviado cadastrado para os seus canos.</td>`;
        tabelaCorpo.appendChild(linhaVazia);
        return;
    }

    alertas.forEach((alerta) => {
        const linha = document.createElement("tr");
        linha.classList.add("border", "border-gray-200", "cursor-pointer", "hover:bg-gray-50", "transition");

        linha.addEventListener("click", () => exibirDetalhesAlerta(alerta));

        const campos = [
            alerta.id,
            alerta.status,
            alerta.tipo || "-",
            alerta.reportado_em ? new Date(alerta.reportado_em).toLocaleDateString("pt-BR") : "-"
        ];

        campos.forEach((valor) => {
            const coluna = document.createElement("td");
            coluna.classList.add("px-3", "py-3", "text-sm");
            coluna.textContent = valor ?? "-";
            linha.appendChild(coluna);
        });

        tabelaCorpo.appendChild(linha);
    });
}

function exibirDetalhesAlerta(alerta) {
    const cardId = document.querySelector("#card-id");
    const cardStatus = document.querySelector("#card-status");
    const cardCodigo = document.querySelector("#card-codigo");
    const cardLocalizacao = document.querySelector("#card-localizacao");
    const cardData = document.querySelector("#card-data");
    const cardGravidade = document.querySelector("#card-gravidade");
    const cardCoordenadas = document.querySelector("#card-coordenadas");
    const cardResponsavel = document.querySelector("#card-responsavel");

    const dataFormatada = alerta.reportado_em
    ? new Date(alerta.reportado_em).toLocaleString("pt-BR")
    : "-";

    if (cardId) cardId.textContent = `A-${alerta.id}`;
    if (cardStatus) cardStatus.textContent = alerta.status ?? "-";
    if (cardCodigo) cardCodigo.textContent = alerta.codigo ?? "-";
    if (cardLocalizacao) cardLocalizacao.textContent = alerta.localizacao ?? "-";
    if (cardData) cardData.textContent = dataFormatada;
    if (cardGravidade) {
    cardGravidade.textContent = alerta.gravidade?.split("_")[1] ?? "-";}
    if (cardCoordenadas) cardCoordenadas.textContent = alerta.coordenadas ?? "-";
    if (cardResponsavel) cardResponsavel.textContent = alerta.responsavel;
}
