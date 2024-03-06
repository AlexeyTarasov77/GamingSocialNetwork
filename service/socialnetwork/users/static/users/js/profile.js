import showToast from "../../../../static/notifications.js";

const csrftoken = $('input[name="csrfmiddlewaretoken"]').val();
$(document).ready(function () {
  if ($('.is_owner').text() == 'True') {
    // showNotification();
    changeAvatar()
  } else {
    subscribe()
    friendRequest()
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

function subscribe() {
  const subscribeBtn = $('#follow');
  subscribeBtn.click(function () {
  console.log(csrftoken);

    $.ajax({
      type: 'PATCH',
      url: `/accounts/profile/subscribe/${subscribeBtn.data('user-slug')}/`,
      beforeSend: (xhr, settings) => xhr.setRequestHeader('X-CSRFToken', csrftoken),
    })
    .done(function (data) {
      if (data.is_subscribed) {
        console.log(1);
        subscribeBtn.removeClass('btn-dark');
        subscribeBtn.addClass('btn-danger');
        subscribeBtn.text('Отписаться');
        $('.toast').remove()
        showToast("Вы подписались!")
      } else {
        console.log(2);
        subscribeBtn.removeClass('btn-danger');
        subscribeBtn.addClass('btn-dark');
        subscribeBtn.text('Подписаться');
        $('.toast').remove()
        showToast("Вы отписались!", "warning")
      }
    })
    .fail(function (err) {
      showToast("Упс! Что-то пошло не так... Попробуйте повторить попытку позже", 'danger', 'Ошибка')
    })
  })
}

function friendRequest(){
  const reqBtn = $('#friend-req');
  reqBtn.click(function () {
    $.ajax({
      type: reqBtn.data("type"),
      url: `/accounts/profile/api/friend_requests/${reqBtn.data("user-slug")}/`,
      data: {"action": reqBtn.data("action")},
      beforeSend: (xhr, settings) => xhr.setRequestHeader('X-CSRFToken', csrftoken),
    })
    .done(function (data) {
      if (data?.sent) {
        reqBtn.removeClass('btn-dark');
        reqBtn.addClass('btn-danger');
        reqBtn.text('Отменить заявку');
        showToast("Заявка отправлена!")
      } else if (data.removed) {
        reqBtn.removeClass('btn-danger');
        reqBtn.addClass('btn-dark');
        reqBtn.text('Отправить заявку в друзья');
        showToast(data.msg)
      }
})
    .fail(function (err) {
      showToast("Упс! Что-то пошло не так... Попробуйте повторить попытку позже", 'danger', 'Ошибка')
    })
  })
}
