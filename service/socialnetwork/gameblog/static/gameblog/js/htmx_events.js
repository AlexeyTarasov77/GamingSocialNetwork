import showToast from "../../../../static/notifications.js";

export function handleHtmxRequest(callback=null) {
    htmx.on('htmx:afterRequest', (e) => {
        const xhr = e.detail.xhr
        const dispatchEl = e.detail.elt // the element that dispatched a request
    
        if (xhr.status >= 200 && xhr.status < 300 && xhr.readyState === 4) {
            callback ? callback(e) : ""
            const msg = dispatchEl.getAttribute('data-success-msg')
            msg ? showToast(msg) : ""
        } 
    
        else if (xhr.status >= 400 && xhr.status < 600) {
          console.log(xhr.status, xhr.responseText);
          let msg = 'Упс! Что-то пошло не так... Попробуйте повторить попытку позже'
          if (xhr.status === 401) {
            msg = `Для выполнения этого действия необходимо авторизоваться. Для этого перейдите по ссылке ниже\n<a href='${window.location.origin}/accounts/login/?next=${window.location.pathname}' class="btn btn-dark">Авторизация</a>`
          } 
            showToast(msg, 'danger', 'Ошибка');
        }
    })
}


export function modalHandler() {
    const modal = new bootstrap.Modal(document.getElementById("modal"));
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
  }
