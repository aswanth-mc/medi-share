function openModal(id) {
    document.getElementById("modal-" + id).classList.add("show");
}

function closeModal(id) {
    document.getElementById("modal-" + id).classList.remove("show");
}
console.log(typeof closeModal);

window.onclick = function(event) {
    document.querySelectorAll('.modal').forEach(modal => {
        if (event.target === modal) {
            modal.classList.remove("show");
        }
    });
};