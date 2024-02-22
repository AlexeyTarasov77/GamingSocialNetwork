document.addEventListener('DOMContentLoaded', function () {
  const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
  const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))
  const toastElList = document.querySelectorAll('.toast')
  const toastList = [...toastElList].map(toastEl => new bootstrap.Toast(toastEl))

  const navbarLinks = document.querySelectorAll('.navbar-light .navbar-nav .nav-link')
  const sidebarLinks = document.querySelectorAll('a.nav_link');
  const userId = document.querySelector('#userId');
  
  id = userId.value !== 'None' ? userId.value : null;
  if (id) {
    console.log(id);
    const socket = new WebSocket(`ws://${window.location.host}/ws/status/${id}/`)
  }
  
  setClick()
  // const SideBarActiveLinkId = localStorage.getItem('SideBarActiveLinkId');
  // const NavBarActiveLinkId = localStorage.getItem('NavBarActiveLinkId');

  // function sidebarLinkActive(){
  //   if(sidebarLink){
  //     sidebarLink.forEach(l=> l.classList.remove('active'))
  //     this.classList.add('active');
  //     localStorage.setItem('SideBarActiveLinkId', this.id);
  //   }
  // }
  // function navbarLinkActive() {
  //   if (navbarLink) {
  //     navbarLink.forEach(l=> l.classList.remove('nav-active'));
  //     this.classList.add('nav-active')
  //     localStorage.setItem('NavBarActiveLinkId', this.id);
  //   }
  // }
  // sidebarLink.forEach(l=> {
  //   l.addEventListener('click', sidebarLinkActive)
  //   if (l.id === SideBarActiveLinkId) {
  //     l.classList.add('active');
  // }
  // })
  // localStorage.removeItem('SideBarActiveLinkId');
  
  // navbarLink.forEach(l=> {
  //   l.addEventListener('click', navbarLinkActive)
  //   if (l.id === NavBarActiveLinkId) {
  //     l.classList.add('nav-active');
  //   }
  // })
  // localStorage.removeItem('NavBarActiveLinkId')

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
