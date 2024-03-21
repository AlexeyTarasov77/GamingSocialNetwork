import showToast from "../../../static/notifications.js";

htmx.on('htmx:afterRequest', (e) => {
    if (e.detail.elt.id === 'add-to-cart-form') {
        if (xhr.status >= 200 && xhr.status < 300 && xhr.readyState === 4) {
            showToast('Товар добавлен в корзину');
        } 
    }
    if(xhr.status >= 400 && xhr.status < 600) {
        showToast('Упс! Что-то пошло не так... Попробуйте повторить попытку позже', 'danger', 'Ошибка');
    }
})