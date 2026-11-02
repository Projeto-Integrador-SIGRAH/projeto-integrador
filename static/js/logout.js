document.addEventListener("DOMContentLoaded", () => {
    const logoutForm = document.querySelector("#logout-form");

    if (!logoutForm) return;

    logoutForm.addEventListener("submit", async (event) => {
        event.preventDefault();
        const response = await fetch(event.target.action, {
            method: "POST",
            headers: {
                "X-CSRFToken": event.target.querySelector(
                    "[name=csrfmiddlewaretoken]"
                ).value,
            },
        });

        if (response.ok) {
            window.location.href = logoutForm.dataset.loginUrl || "/";
        };
    });
});