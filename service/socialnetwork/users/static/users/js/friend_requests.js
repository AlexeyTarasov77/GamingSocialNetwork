import showToast from "../../../../static/notifications.js"
const csrftoken = $('input[name="csrfmiddlewaretoken"]').val();

$(document).ready(function () {
  requestHandler()
})

function requestHandler() {
  $('.handling-btn').click(function () {
    $.ajax({
      type: $(this).data('type'),
      url: $(this).data('url'),
      data: {"user_pk": $(this).data('user-pk')},
      beforeSend: (xhr, settings) => xhr.setRequestHeader('X-CSRFToken', csrftoken),
    })
    .done((resp)=>{
        if (resp.accepted) {
          showToast("Пользователь добавлен в друзья")
        } else {
            showToast("Заявка отклонена")
        }
        $(this).closest('.column__row').remove();
        
    })
    .fail(()=>{
        showToast("Упс! Что-то пошло не так... Попробуйте повторить попытку позже", 'danger', 'Ошибка')
    })
  })
}