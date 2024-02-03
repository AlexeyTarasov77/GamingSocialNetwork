export default function showErrorToast() {
    let currDate = new Date();
    let toastErrMsg = `
    <div class="toast text-bg-warning" role="alert" aria-live="assertive" aria-atomic="true">
        <div class="toast-header">
          <strong class="me-auto">Bootstrap</strong>
          <small class="text-body-secondary">${currDate.toLocaleString()}</small>
          <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
        <div class="toast-body">
          ${'Ууупс! Для того что бы поставить лайк вам нужно авторизоваться'} →  <a href="{% url "account_login" %}" class="btn btn-danger btn-sm">Войти</a> 
        </div>
    </div>`
    $('.toast-container').append(toastErrMsg)
    new bootstrap.Toast($('.toast')).show()
}


