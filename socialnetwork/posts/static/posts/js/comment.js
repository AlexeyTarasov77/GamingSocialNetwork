import showErrorToast from './notifications.js'
import btnStatus from './btnStatus.js';
document.addEventListener("DOMContentLoaded", function() {
    if (document.forms.commentForm) {
    const csrftoken = document.querySelector('form input[name="csrfmiddlewaretoken"]').value
    const commentForm = document.forms.commentForm;
    const commentFormContent = commentForm.content;
    const commentFormParentInput = commentForm.parent;
    const commentFormSubmit = commentForm.commentSubmit;
    const commentPostId = commentForm.getAttribute('data-post-id');

    commentForm.addEventListener('submit', createComment);
    replyUser()
    likeComment()

    function replyUser() {
    document.querySelectorAll('.btn-reply').forEach(e => {
        e.addEventListener('click', replyComment);
        });
    }

    function likeComment() {
        $('.comment-like').click(function () {
        let commentId = $(this).data('likecomment-id');
        let commentLike = $(this);
        $.ajax({
            type: 'POST',
            url: $('#comment-url').text(),
            data: {object_id: commentId, csrfmiddlewaretoken: csrftoken}
        })
        .done(function (data) {
            commentLike.closest('.comment-head').find('.num-likes-count').text(data.likes_count);
            if (data.is_liked) {
                commentLike.removeClass('bi-heart');
                commentLike.addClass('bi-heart-fill text-danger')
            }  else { 
                commentLike.removeClass('text-danger', 'bi-heart-fill')
                commentLike.addClass('bi-heart')
            };
        })

        .fail(function (err) {
            showErrorToast()
        })
      })
    }


    function replyComment() {
    const commentUsername = this.getAttribute('data-comment-username');
    const commentMessageId = this.getAttribute('data-comment-id');
    commentFormContent.value = `${commentUsername}, `;
    commentFormParentInput.value = commentMessageId;
    }
    async function createComment(event) {
        event.preventDefault();
        btnStatus(false, 'Ожидаем ответа от сервера...', commentFormSubmit)
        try {
            const response = await fetch(`http://localhost:8000/posts/comment-post/${commentPostId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken,
                    'X-Requested-With': 'XMLHttpRequest',
                },
                body: new FormData(commentForm),
            });
            const comment = await response.json();
            let commentTemplate = `<ul id="comment-thread-${comment.id}" class="comments-list">
            <li>
                <div class="comment-main-level">
                    <div class="comment-avatar"><img src="http://i9.photobucket.com/albums/a88/creaticode/avatar_1_zps8e1c80cd.jpg" alt=""></div>
                    <div class="comment-box">
                        <div class="comment-head">
                            <h6 class="comment-name {% if node.is_root_node or node.get_root.author.username == node.author.username%}by-author{% endif %} ${comment.by_author ? "by-author" : ""}">${comment.author}</h6>
                            <span>${formatDateTime(comment.time_create)}</span>
                            <a href="#commentForm" data-comment-id="${comment.id}" data-comment-username="${comment.author}" class="btn-reply"><i class="bi bi-reply"></i></a>
                            <i class="bi bi-heart"></i>
                        </div>
                        <div class="comment-content">
                            ${comment.content}
                        </div>
                    </div>
                </div>
            </li>
        </ul>`;
        if (comment.is_child) {
            document.querySelector(`#comment-thread-${comment.parent}`).insertAdjacentHTML("beforeend", commentTemplate);
        }
        else {
            document.querySelector('.nested-comments').insertAdjacentHTML("beforeend", commentTemplate)
        }
        commentForm.reset()
        btnStatus(true, "Добавить комментарий", commentFormSubmit)
        commentFormParentInput.value = null;
        replyUser();
    }
        catch (error) {
            console.log(error)
        }
    }
  }

    function commentsReplyList() {
    $('.reply-list .comments-list').hide()
    $('.reply-list .comments-list').hide()
    $('.reply-list .comments-list li:first').show()
    $('.reply-list .comments-list').hide()
    $('.reply-list .comments-list li:first').show()

        $(".show-more-replies").click(function() {
            let commentId = $(this).data("comment-id");
            $(".reply-comment-" + commentId + " .comments-list").show();
            $(this).hide();
            $(".hide-replies[data-comment-id='" + commentId + "']").show();
        });

        $(".hide-replies").click(function() {
            let commentId = $(this).data("comment-id");
            $(".reply-comment-" + commentId + " .comments-list").hide();
            $(this).hide();
            $(".show-more-replies[data-comment-id='" + commentId + "']").show();
        });
    }

    function formatDateTime(isoDateTime) {
        const date = new Date(isoDateTime);
        const months = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря'];
        const outputDate = {day: date.getDate(), month: months[date.getMonth()], year: date.getFullYear(), hours: date.getHours(), minutes: date.getMinutes()}
        return `${outputDate.day} ${outputDate.month} ${outputDate.year} г. ${outputDate.hours}:${outputDate.minutes < 10 ? '0' + outputDate.minutes : outputDate.minutes}`;
    }
    commentsReplyList()
});