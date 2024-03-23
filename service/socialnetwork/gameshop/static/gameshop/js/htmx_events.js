import showToast from "../../../../static/notifications.js";

htmx.on('htmx:afterRequest', (e) => {
    const xhr = e.detail.xhr
    const dispatchEl = e.detail.elt // the element that dispatched a request
    if (dispatchEl.id === 'cart-action') {
        if (xhr.status >= 200 && xhr.status < 300 && xhr.readyState === 4) {
            if (dispatchEl.getAttribute('data-action') === 'remove') {
              dispatchEl.closest('.product-item').remove();
            }
            showToast(dispatchEl.getAttribute('data-success-msg'));
        } 
    }
    if(xhr.status >= 400 && xhr.status < 600) {
        showToast('Упс! Что-то пошло не так... Попробуйте повторить попытку позже', 'danger', 'Ошибка');
    }
})