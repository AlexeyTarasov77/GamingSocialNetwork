$(document).ready(function () {
  $('.profile__photo img').click(() => $('#photoInput').click())
  $('#photoInput').on('change', function () {
    console.log($(this).prop('files')[0]);
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
      console.log(response.path);
      $('.profile__photo img').attr('src', response.path);
    })
    .fail((err) => {
      console.log(err);
    })
  })
})

