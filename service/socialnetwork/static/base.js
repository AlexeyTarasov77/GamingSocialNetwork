document.addEventListener('DOMContentLoaded', function () {
  const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
  const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))
  const toastElList = document.querySelectorAll('.toast')
  const toastList = [...toastElList].map(toastEl => new bootstrap.Toast(toastEl))

  showNotification()

  const navbarLinks = document.querySelectorAll('.navbar-light .navbar-nav .nav-link')
  const sidebarLinks = document.querySelectorAll('a.nav_link');

  const socket = new WebSocket(`ws://${window.location.host}/ws/status/`)

  
  setClick()

  function initial() {
    localStorage.clear();
    navbarLinks.forEach(nl=> {nl.classList.remove('nav-active')});
    sidebarLinks.forEach(sl=> {sl.classList.remove('active')})
  }

  function setLinkActive(e, linkType) {
    initial();
    item = e.target
    if (linkType === 'navbarActive') {
      item.classList.add('nav-active');
      localStorage.setItem(linkType, item.id)
    } else {
      item = item.parentElement
      item.classList.add('active');
      localStorage.setItem(linkType, item.id)
    }
  }

  function setClick() {
    navbarLinks.forEach(nl=> {nl.onclick = (event) => setLinkActive(event, 'navbarActive')});
    sidebarLinks.forEach(sl=> {sl.onclick = (event) => setLinkActive(event, 'sidebarActive')})
  }

  function setInitialActive(links, key, className) {
    links.forEach(l => {
      if (l.id === localStorage.getItem(key)) {
        l.classList.add(className)
      }
    })
  }

  window.onload = function () {
    if (localStorage.getItem('navbarActive')) {
      setInitialActive(navbarLinks, 'navbarActive', 'nav-active')
    } else {
      setInitialActive(sidebarLinks, 'sidebarActive', 'active')
    }
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