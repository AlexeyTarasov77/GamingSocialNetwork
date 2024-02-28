import showToast from "../../../../static/notifications.js";

$(document).ready(function () {
  if ($('.is_owner').text() == 'True') {
    // showNotification();
    changeAvatar()
  } else {
    subscribe()
  }
})
const csrftoken = $('input[name="csrfmiddlewaretoken"]').val();
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

function subscribe() {
  const subscribeBtn = $('#follow');
  subscribeBtn.click(function () {
  console.log(csrftoken);

    $.ajax({
      type: 'PATCH',
      url: `/accounts/profile/subscribe/${subscribeBtn.data('user-slug')}/`,
      beforeSend: (xhr, settings) => xhr.setRequestHeader('X-CSRFToken', csrftoken),
      // data: {csrfmiddlewaretoken: csrftoken}
    })
    .done(function (data) {
      if (data.is_subscribed) {
        subscribeBtn.removeClass('btn-dark');
        subscribeBtn.addClass('btn-danger');
        subscribeBtn.text('Отписаться');
        showToast("Вы подписаны!")
      } else {
        subscribeBtn.removeClass('btn-danger');
        subscribeBtn.addClass('btn-dark');
        subscribeBtn.text('Подписаться');
        showToast("Вы отписались!", "warning")
      }
    })
    .fail(function (err) {
      showToast("Упс! Что-то пошло не так... Попробуйте повторить попытку позже", 'danger', 'Ошибка')
    })
  })
}
