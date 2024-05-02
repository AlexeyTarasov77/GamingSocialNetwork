import showToast from "../../../../static/notifications.js";

$(document).ready(function () {
  $('.save').click(function () {
    const postId = $(this).data('post-id')
    $.ajax({
      type: "PATCH",
      url: `${window.location.origin}/api/posts/save-post/${postId}/`,
      beforeSend: (xhr, settings) => xhr.setRequestHeader('X-CSRFToken', $('input[name="csrfmiddlewaretoken"]').val()),
    })
    .done((data) => {
        const saveText = $(this).find('.save-text')
        const saveIcon = $(this).find('.save-icon')
        if (data.is_saved) {
          postSaveHandler(true, saveText, saveIcon)
        }
        else {
          postSaveHandler(false, saveText, saveIcon)
        }
      })
  })
})

function postSaveHandler(isSaved, saveText, saveIcon) {
  if (isSaved)  {
    saveText.text("Сохранено")
    saveIcon.html(`
      <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" fill="currentColor" class="bi bi-floppy-fill text-warning" viewBox="0 0 16 16">
      <path d="M0 1.5A1.5 1.5 0 0 1 1.5 0H3v5.5A1.5 1.5 0 0 0 4.5 7h7A1.5 1.5 0 0 0 13 5.5V0h.086a1.5 1.5 0 0 1 1.06.44l1.415 1.414A1.5 1.5 0 0 1 16 2.914V14.5a1.5 1.5 0 0 1-1.5 1.5H14v-5.5A1.5 1.5 0 0 0 12.5 9h-9A1.5 1.5 0 0 0 2 10.5V16h-.5A1.5 1.5 0 0 1 0 14.5z"/>
      <path d="M3 16h10v-5.5a.5.5 0 0 0-.5-.5h-9a.5.5 0 0 0-.5.5zm9-16H4v5.5a.5.5 0 0 0 .5.5h7a.5.5 0 0 0 .5-.5zM9 1h2v4H9z"/>
      </svg>
    `)
    showToast("Пост сохранен.")
  } else {
    saveText.text("Сохранить")
    saveIcon.html(`
      <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" fill="currentColor" class="bi bi-bookmark-fill text-warning" viewBox="0 0 16 16">
      <path d="M2 2v13.5a.5.5 0 0 0 .74.439L8 13.069l5.26 2.87A.5.5 0 0 0 14 15.5V2a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2"/>
      </svg>
    `)
    showToast("Пост удален из сохраненных.")
  }


}
