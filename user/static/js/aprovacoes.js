const tabelaAtivos = document.querySelector("#lista-admins-ativos");
const tabelaPendentes = document.querySelector("#lista-admins-pendentes");
const confirmActionModal = document.querySelector("#modal-confirm-action")
const confirmActionModalButton = document.querySelector("#modal-confirm-action-button")
const confirmActionModalTitle = document.querySelector("#modal-confirm-action-titulo")
const confirmActionModalMensagem = document.querySelector("#modal-confirm-action-mensagem")
let adminId;
let action;
let botao;

const apiUrl = tabelaAtivos.dataset.apiUrl;

const csrfToken = document.querySelector(
    "[name=csrfmiddlewaretoken]"
)?.value;


async function listarAdministradores() {
    try {
        const response = await fetch(apiUrl);

        if (!response.ok) {
            throw new Error("Erro ao buscar administradores.");
        }

        const data = await response.json();

        const administradores = data.results ?? data;

        const ativos = administradores.filter(
            (admin) => admin.is_active &&
                admin.is_approved &&
                !admin.is_rejected
        );

        const pendentes = administradores.filter(
            (admin) => !admin.is_approved &&
                !admin.is_rejected
        );

        renderizarAdministradoresAtivos(ativos);
        renderizarAdministradoresPendentes(pendentes);

    } catch (error) {
        console.error(error);
    }
}


function renderizarAdministradoresAtivos(administradores) {
    tabelaAtivos.innerHTML = "";

    if (administradores.length === 0) {
        tabelaAtivos.innerHTML = `<tr class="border-b border-gray-300 text-sm text-gray-600">
            <td class="px-3 py-3" colspan="4">
                <p class="text-center text-gray-500">Nenhum administrador ativo encontrado.</p>
            </td>
        </tr>`;
        return;
    }

    administradores.forEach((admin) => {
        const linha = document.createElement("tr");

        linha.classList.add(
            "border",
            "border-gray-200",
            "text-sm",
            "hover:bg-gray-50"
        );

        const campos = [
            admin.nome,
            admin.matricula,
            admin.email,
            "Ativo",
        ];

        campos.forEach((valor) => {
            const coluna = document.createElement("td");

            coluna.classList.add("px-3", "py-3");
            coluna.textContent = valor ?? "-";

            linha.appendChild(coluna);
        });

        tabelaAtivos.appendChild(linha);
    });
}


function renderizarAdministradoresPendentes(administradores) {
    tabelaPendentes.innerHTML = "";

    if (administradores.length === 0) {
        tabelaPendentes.innerHTML = `<tr class="border-b border-gray-300 text-sm text-gray-600">
            <td class="px-3 py-3" colspan="4">
                <p class="text-center text-gray-500">Nenhum administrador pendente encontrado.</p>
            </td>
        </tr>`;
        return;
    }

    administradores.forEach((admin) => {
        const linha = document.createElement("tr");

        linha.classList.add(
            "border",
            "border-gray-200",
            "text-sm",
            "hover:bg-gray-50"
        );

        linha.dataset.adminId = admin.id;

        const campos = [
            admin.nome,
            admin.matricula,
            admin.email,
        ];

        campos.forEach((valor) => {
            const coluna = document.createElement("td");

            coluna.classList.add("px-3", "py-3");
            coluna.textContent = valor ?? "-";

            linha.appendChild(coluna);
        });

        const colunaAcoes = document.createElement("td");

        colunaAcoes.classList.add("px-3", "py-3");

        const containerAcoes = document.createElement("div");

        containerAcoes.classList.add("flex", "flex-wrap", "gap-2");

        const botaoAprovar = document.createElement("button");

        botaoAprovar.type = "button";
        botaoAprovar.textContent = "Aprovar";

        botaoAprovar.dataset.action = "approve";

        botaoAprovar.classList.add(
            "cursor-pointer",
            "rounded-md",
            "border",
            "border-green-700",
            "px-3",
            "py-2",
            "text-green-700",
            "transition-colors",
            "hover:bg-green-700",
            "hover:text-white"
        );

        const botaoRejeitar = document.createElement("button");

        botaoRejeitar.type = "button";
        botaoRejeitar.textContent = "Rejeitar";

        botaoRejeitar.dataset.action = "reject";

        botaoRejeitar.classList.add(
            "cursor-pointer",
            "rounded-md",
            "border",
            "border-red-700",
            "px-3",
            "py-2",
            "text-red-700",
            "transition-colors",
            "hover:bg-red-700",
            "hover:text-white"
        );

        containerAcoes.append(botaoAprovar, botaoRejeitar);

        colunaAcoes.appendChild(containerAcoes);
        linha.appendChild(colunaAcoes);

        tabelaPendentes.appendChild(linha);
    });
}


tabelaPendentes.addEventListener("click", (event) => {
    botao = event.target.closest("button[data-action]");

    if (!botao) return;

    const linha = botao.closest("tr");

    adminId = linha.dataset.adminId;
    action = botao.dataset.action;
    let colors = confirmActionModal.querySelectorAll(".bg-sky-600, .bg-red-600")
    console.log(colors)

    if (action == "approve") {
        confirmActionModalTitle.textContent = "Aprovar Administrador"
        confirmActionModalMensagem.textContent = "Tem certeza que deseja Aprovar esse Administrador?"
        confirmActionModalButton.textContent = "Aprovar"
        colors.forEach((e) => {
            e.classList.remove("bg-red-600")
            e.classList.add("bg-sky-600")
        })
    } else {
        confirmActionModalTitle.textContent = "Rejeitar Administrador"
        confirmActionModalMensagem.textContent = "Tem certeza que deseja Rejeitar esse Administrador?"
        confirmActionModalButton.textContent = "Rejeitar"
        colors.forEach((e) => {
            e.classList.add("bg-red-600")
            e.classList.remove("bg-sky-600")
        })
    }

    confirmActionModal.showModal()
});

confirmActionModalButton.addEventListener("click", async (event) => {
    try {
        botao.disabled = true;

        const response = await fetch(
            `${apiUrl}${adminId}/${action}/`,
            {
                method: "POST",
                headers: {
                    "Accept": "application/json",
                    "X-CSRFToken": csrfToken,
                },
            }
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                data.detail ?? "Não foi possível realizar a operação."
            );
        }

        confirmActionModal.close()

        await listarAdministradores();

    } catch (error) {
        console.error(error);
        alert(error.message);

        botao.disabled = false;
    }
})


listarAdministradores();