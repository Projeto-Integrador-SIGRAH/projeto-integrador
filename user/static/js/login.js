const form = document.querySelector("form");

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const formData = new FormData(form);
    const dadosDoFormulario = Object.fromEntries(formData.entries());

    try {
        const resposta = await fetch("/user/api/login/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": formData.get("csrfmiddlewaretoken")
            },
            body: JSON.stringify(dadosDoFormulario)
        });

        const dados = await resposta.json();

        if (!resposta.ok) {
            alert("Email ou senha inválidos.");
            return;
        }

        sessionStorage.setItem("access", dados.access);
        sessionStorage.setItem("refresh", dados.refresh);

        window.location.href = "/user/painel/";

    } catch (erro) {
        console.error("Erro ao realizar login:", erro);
        alert("Não foi possível conectar ao servidor.");
    }
});