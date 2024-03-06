import NavBar from './nav.js'; 

$(document).ready(function () {
  const listClasses = [ '.content__liked', '.content__saved', '.content__drafts'];
  const mainClass = '.content__own';
  
  const navBar = new NavBar(listClasses, mainClass);
  navBar.hideContent(true);
  $('.nav-link').click(function() {
    navBar.clickAction($(this).data('name'));
  })
});