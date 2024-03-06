import showToast from "../../../../static/notifications.js";

$(document).ready(function () {
  $('#save').click(function () {
    const postId = $(this).data('post-id')
    $.ajax({
      type: "PATCH",
      url: `${window.location.origin}/posts/save-post/${postId}/`,
      beforeSend: (xhr, settings) => xhr.setRequestHeader('X-CSRFToken', $('input[name="csrfmiddlewaretoken"]').val()),
    })
    .done(function (data) {
        if (data.is_saved) {
          $('#save-text').text("Сохранено")
          showToast("Пост сохранен.")
        }
        else {
            $('#save-text').text("Сохранить")
            showToast("Пост удален из сохраненных.")
        }
      })
  })
})