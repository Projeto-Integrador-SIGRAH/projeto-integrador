document.addEventListener('DOMContentLoaded', function () {
    const indicador = document.getElementById('indicador');
    const admin = document.getElementById('admin');
    const cidadao = document.getElementById('cidadao');

    if (!indicador) return;
    if (admin) {
        admin.addEventListener('click', function (event) {
        event.preventDefault();

        indicador.style.transform = 'translateX(100%)';

        setTimeout(function () {
            window.location.href = admin.href;
        }, 300);
    });
    }
    if (cidadao) {
    cidadao.addEventListener('click', function (event) {
        event.preventDefault();

        indicador.style.transform = 'translateX(0)';

        setTimeout(function () {
            window.location.href = cidadao.href;
        }, 300);
    });
    }
});