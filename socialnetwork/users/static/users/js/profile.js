$(document).ready(function () {
  if ($('.is_owner').text() == 'True') {
    // showNotification();
    changeAvatar()
  }
})

function changeAvatar() {
  $('.profile__photo img').click(() => $('#photoInput').click())
  $('#photoInput').on('change', function () {
    var formData = new FormData();
    formData.append('csrfmiddlewaretoken', $('input[name="csrfmiddlewaretoken"]').val());
    formData.append('user_id', $(this).data('user_id'));
    formData.append('image', $(this).prop('files')[0]);

    $.ajax({
      type: 'POST',
      url: $('#url').val(),
      beforeSend: (xhr, settings) => xhr.setRequestHeader('X-CSRFToken', $('input[name="csrfmiddlewaretoken"]').val()),
      data: formData,
      processData: false,  // Не обрабатывать данные
      contentType: false,  // Не устанавливать Content-Type заголовок
    })
    .done((response) => {
      $('.profile__photo img').attr('src', response.path);
    })
    .fail((err) => {
      console.log(err);
    })
  })
}

// function showNotification() {
//   const msg = document.querySelector('.msg');
//   if (msg) {
//     handleClass('opacity-0', 'opacity-100')
//     setTimeout(() => {
//       handleClass('opacity-100', 'opacity-0')
//     }, 5000)
//   }
// }

// function handleClass(className1, className2) {
//   msg.classList.remove(className1);
//   msg.classList.add(className2);
// }

