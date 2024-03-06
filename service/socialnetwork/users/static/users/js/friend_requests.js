import showToast from "../../../../static/notifications.js"
const csrftoken = $('input[name="csrfmiddlewaretoken"]').val();

$(document).ready(function () {
  requestHandler()
})

function requestHandler() {
  $('.handling-btn').click(function () {
    const userSlug = $(this).data('user-slug')
    $.ajax({
      type: $(this).data('type'),
      url: `/accounts/profile/api/friend_requests/handler/${userSlug}/`,
      data: {"user_pk": $(this).data('user-pk')},
      beforeSend: (xhr, settings) => xhr.setRequestHeader('X-CSRFToken', csrftoken),
    })
    .done((resp)=>{
        if (resp.accepted) {
          showToast(`Пользователь ${userSlug} добавлен в друзья`)
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