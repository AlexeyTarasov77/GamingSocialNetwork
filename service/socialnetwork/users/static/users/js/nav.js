$(document).ready(function () {
  const listClasses = ['.content__bio', '.content__following', '.content__followers', '.content__friends', '.content__orders'];
  const mainClass = '.content__main';
  const navBar = new NavBar(listClasses, mainClass);
  navBar.hideContent(true);

  $('.nav-link').click(function() {
    navBar.clickAction($(this).data('name'));
  })
})


export default class NavBar{
    constructor(listClasses, mainClass) {
        this.listClasses = listClasses
        this.mainClass = mainClass
    }

    hideContent(initial) {
      for (const el of this.listClasses) {
        console.log(el);
          $(el).hide();
      }
      if (!initial) {
        $(this.mainClass).hide();
        $('.nav-link').removeClass('btn-active');
      }
    }
    
    clickAction(clickedItem) {
      this.hideContent(false);
      $(`[data-name="${clickedItem}"]`).addClass('btn-active');
      $(`.content__${clickedItem}`).show();
    }
    
}
