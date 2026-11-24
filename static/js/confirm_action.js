document.addEventListener("DOMContentLoaded", () => {
    const closesModal = document.querySelectorAll(".close-confirm-action-modal")
    const modal = document.querySelector("#modal-confirm-action")

    closesModal.forEach((e) => {
        e.addEventListener("click", () => {
            modal.close()
        })
    })
})