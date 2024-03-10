document.addEventListener("DOMContentLoaded", function () {
  listBtn = document.querySelector('#list');
  gridBtn = document.querySelector('#grid');
  products = document.querySelectorAll('#products .item');
  listBtn.onclick = () => products.forEach(element => element.addClass('list-group-item'));
  gridBtn.onclick = () => products.forEach(element => {element.removeClass('list-group-item'); element.addClass('grid-group-item')});
})


// $(document).ready(function() {
//     $('#list').click(function(event){event.preventDefault();$('#products .item').addClass('list-group-item');});
//     $('#grid').click(function(event){event.preventDefault();$('#products .item').removeClass('list-group-item');$('#products .item').addClass('grid-group-item');});
// });