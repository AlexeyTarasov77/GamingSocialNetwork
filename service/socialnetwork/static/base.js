document.addEventListener('DOMContentLoaded', function () {
  const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
  const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))
  const toastElList = document.querySelectorAll('.toast')
  const toastList = [...toastElList].map(toastEl => new bootstrap.Toast(toastEl))
  const userID = parseInt(document.querySelector('#userId').value)
    
  showNotification()

  if (userID) {
    const socket = new WebSocket(`ws://${window.location.host}/ws/gameblog/online-status/`)
  }

});

function showNotification() {
  const messages = document.querySelectorAll('.msg');
  if (messages.length > 0) {
    handleClass(messages, 'opacity-0', 'opacity-100')
    setTimeout(() => {
      handleClass(messages, 'opacity-100', 'opacity-0')
    }, 5000)
  }
}

function handleClass(objects, className1, className2) {
  objects.forEach(obj => obj.classList.remove(className1))
  objects.forEach(obj => obj.classList.add(className2))
}