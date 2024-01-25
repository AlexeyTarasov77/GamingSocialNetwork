document.addEventListener('DOMContentLoaded', function () {
  const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
  const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))

  const NavLinkColor = document.querySelectorAll('.navbar-light .navbar-nav .nav-link')
  const linkColor = document.querySelectorAll('.nav_link');
  const SideBarActiveLinkId = localStorage.getItem('SideBarActiveLinkId');
  const NavBarActiveLinkId = localStorage.getItem('NavBarActiveLinkId');

  function colorLink(){
    if(linkColor){
    linkColor.forEach(l=> l.classList.remove('active'))
    this.classList.add('active');
    localStorage.setItem('SideBarActiveLinkId', this.id);
    }
  }
  function NavColorLink() {
    if (NavLinkColor) {
      NavLinkColor.forEach(l=> l.classList.remove('nav-active'));
      this.classList.add('nav-active')
      localStorage.setItem('NavBarActiveLinkId', this.id);
    }
  }
  linkColor.forEach(l=> {
    l.addEventListener('click', colorLink)
    if (l.id === SideBarActiveLinkId) {
      l.classList.add('active');
  }
  })
  localStorage.removeItem('SideBarActiveLinkId');
  
  NavLinkColor.forEach(l=> {
    l.addEventListener('click', NavColorLink)
    if (l.id === NavBarActiveLinkId) {
      l.classList.add('nav-active');
    }
  })
  localStorage.removeItem('NavBarActiveLinkId')
});

// document.addEventListener('DOMContentLoaded', function () {
//   const linkColor = document.querySelectorAll('.navbar-light .navbar-nav .nav-link');
//   const activeLinkId = localStorage.getItem('activeLinkId');
//   function colorLink() {
//       linkColor.forEach(l => l.classList.remove('active'));
//       this.classList.add('active');
//       localStorage.setItem('activeLinkId', this.id);
//   }

//   linkColor.forEach(l => {
//       l.addEventListener('click', colorLink);
//       if (l.id === activeLinkId) {
//           l.classList.add('nav-active');
//           localStorage.removeItem('activeLinkId');
//       }
//   });
// });

