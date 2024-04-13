import showToast from "../../../../static/notifications.js";

const modal = new bootstrap.Modal(document.getElementById("modal"));

htmx.on('htmx:afterRequest', (e) => {
    const xhr = e.detail.xhr
    const dispatchEl = e.detail.elt // the element that dispatched a request
    console.log(dispatchEl);
    if (dispatchEl.id === 'cart-action') {
      console.log('cart-action');
        if (xhr.status >= 200 && xhr.status < 300 && xhr.readyState === 4) {
            switch (dispatchEl.getAttribute('data-action')) {
              case 'remove':
                dispatchEl.closest('.product-item').remove();
                break;
              case 'order':
                getPayment(xhr.responseText)
                break;
            }
            const msg = dispatchEl.getAttribute('data-success-msg')
            msg ? showToast(msg) : ""
        } 
    }
    if(xhr.status >= 400 && xhr.status < 600) {
      console.log(xhr.status, xhr.responseText);
      let msg = 'Упс! Что-то пошло не так... Попробуйте повторить попытку позже'
      if (xhr.status === 401) {
        msg = `Для выполнения этого действия необходимо авторизоваться. Для этого перейдите по ссылке ниже\n<a href='${window.location.origin}/accounts/login/?next=${window.location.pathname}' class="btn btn-dark">Авторизация</a>`
      }
        showToast(msg, 'danger', 'Ошибка');
    }
})

;(function () {
    htmx.on('htmx:afterSwap', function (e) {
      if (e.detail.target.id == 'dialog') {
        modal.show();
      }
    })
    htmx.on('htmx:beforeSwap', function (e) {
      if (e.detail.target.id == 'dialog' && !e.detail.xhr.responseText) {
        modal.hide();
      }
    })
  })()

function getPayment(url) {
  modal.hide()
  window.location.href = url
}