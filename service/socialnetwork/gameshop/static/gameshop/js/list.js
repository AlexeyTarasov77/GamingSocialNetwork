document.addEventListener("DOMContentLoaded", function () {
  const listBtn = document.querySelector('#list');
  const gridBtn = document.querySelector('#grid');
  const products = document.querySelectorAll('#products .item');
  listBtn.onclick = () => products.forEach(element => element.classList.add('list-group-item'));
  gridBtn.onclick = () => products.forEach(element => {element.classList.remove('list-group-item'); element.classList.add('grid-group-item')});
})


// $(document).ready(function() {
//     $('#list').click(function(event){event.preventDefault();$('#products .item').addClass('list-group-item');});
//     $('#grid').click(function(event){event.preventDefault();$('#products .item').removeClass('list-group-item');$('#products .item').addClass('grid-group-item');});
// });