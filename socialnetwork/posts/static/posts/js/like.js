import showErrorToast from './notifications.js'
$(document).ready(function() {
    const csrftoken = $('input[name="csrfmiddlewaretoken"]').val()
    $(".heart").click(function() {
        let postId = $(this).data("post-id");
        let heartEl = $(this)
        // Отправляем асинхронный запрос на сервер
        $.ajax({
            type: "POST",
            url: $('#like-url').val(),
            data: { object_id: postId, csrfmiddlewaretoken: csrftoken},
            })
        .done(function(data) {
            let numLikesEl = heartEl.closest('.card-body').find('#num-likes-count')
            numLikesEl.length > 0 ? numLikesEl.text(data.likes_count) : $('#num-likes-count').text(data.likes_count);
                if (data.is_liked) {
                    heartEl.addClass("is-active")
                }
                else {
                    heartEl.removeClass("is-active")
                } 
        })
        .fail(function(err) {
            showErrorToast()
        })
    });
});