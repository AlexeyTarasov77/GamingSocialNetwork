export default function showToast(msg, type='success', title='Уведомление') {
  let currDate = new Date();
  let toast = `
  <div class="toast text-bg-${type}" role="alert" aria-live="assertive" aria-atomic="true">
      <div class="toast-header">
        <strong class="me-auto">${title}</strong>
        <small class="text-body-secondary">${currDate.toLocaleString()}</small>
        <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
      </div>
      <div class="toast-body">
        ${msg}
      </div>
  </div>`
  $('.toast-container').append(toast)
  new bootstrap.Toast($('.toast')).show()
}



