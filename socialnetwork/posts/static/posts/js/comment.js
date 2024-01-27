// const commentForm = $('.comment-form')

// commentForm.on('submit', createComment);
// const replyUser = () => $('.reply-btn').on('click', replyComment);

// function replyComment() {
//   const commentReplyUsername = $(this).data('comment-username');
//   const commentReplyId = $(this).data('comment-id');
//   commentForm.find('[name=content]').val(`${commentReplyUsername}, `);
//   commentForm.find('[name=parent]').val(commentReplyId);
// }

// async function createComment(event) {
//   event.preventDefault();
//   commentForm.find('.comment-submit').prop('disabled', true).text('Загрузка...')
//   $.ajax({
//     type: "POST",
//     url: commentForm.attr('action'),
//     data: {formData: new FormData(commentForm) ,csrfmiddlewaretoken: $('#csrf-token').val()},
//     })
//     .done(function (json) {
//       let commentHtml = `<ul id="comments-list-${json.id}" class="comments-list">
//                             <li>
//                                 <div class="comment-main-level">
//                                     <div class="comment-avatar"><img src="http://i9.photobucket.com/albums/a88/creaticode/avatar_1_zps8e1c80cd.jpg" alt=""></div>
//                                     <div class="comment-box">
//                                         <div class="comment-head">
//                                             <h6 class="comment-name {% if node.is_root_node or node.get_root.author.username == node.author.username%}by-author{% endif %}">${comment.author}</h6>
//                                             <span${json.time_create}</span>
//                                             <a href="#comment-form" data-comment-id=${comment.id}" data-comment-username="${comment.author}" class="reply-btn"><i class="bi bi-reply"></i></a>
//                                             <i class="bi bi-heart"></i>
//                                         </div>
//                                         <div class="comment-content">
//                                             ${json.content}
//                                         </div>
//                                     </div>
//                                 </div>
//                             </li>
//                         </ul>`;
//         if (json.is_child) {
//           $(`#comments-list-${json.id} .reply-comment-${json.id}`).append(commentHtml)
//         } else {
//             $('.comments').append(commentHtml)
//         }
//         commentForm[0].reset();
//         commentForm.find('.comment-submit').prop('disabled', false).text('Добавить комментарий')
//         commentForm.find('[name=parent]').val(null);
//         replyUser()
//     })
// }
// document.addEventListener("DOMContentLoaded", function() {
//     const csrftoken = document.querySelector('form input[name="csrfmiddlewaretoken"]').value
//     const commentForm = document.forms.commentForm;
//     const commentFormContent = commentForm.content;
//     const commentFormParentInput = commentForm.parent;
//     const commentFormSubmit = commentForm.commentSubmit;
//     const commentPostId = commentForm.getAttribute('data-post-id');

//     commentForm.addEventListener('submit', createComment);

//     replyUser()

//     function replyUser() {
//     document.querySelectorAll('.reply-btn').forEach(e => {
//         e.addEventListener('click', replyComment);
//     });
//     }

//     function replyComment() {
//     const commentUsername = this.getAttribute('data-comment-username');
//     const commentMessageId = this.getAttribute('data-comment-id');
//     commentFormContent.value = `${commentUsername}, `;
//     commentFormParentInput.value = commentMessageId;
//     }
//     async function createComment(event) {
//         event.preventDefault();
//         commentFormSubmit.disabled = true;
//         commentFormSubmit.innerText = "Ожидаем ответа сервера...";
//         try {
//             const response = await fetch(`http://localhost:8000/posts/comment-post/${commentPostId}/`, {
//                 method: 'POST',
//                 headers: {
//                     'X-CSRFToken': csrftoken,
//                     'X-Requested-With': 'XMLHttpRequest',
//                 },
//                 body: new FormData(commentForm),
//             });
//             const comment = await response.json();

//             let commentTemplate = `<ul id="comments-list-${comment.id}" class="comments-list">
//                                 <li>
//                                     <div class="comment-main-level">
//                                         <div class="comment-avatar"><img src="http://i9.photobucket.com/albums/a88/creaticode/avatar_1_zps8e1c80cd.jpg" alt=""></div>
//                                         <div class="comment-box">
//                                             <div class="comment-head">
//                                                 <h6 class="comment-name {% if node.is_root_node or node.get_root.author.username == node.author.username%}by-author{% endif %}">${comment.author}</h6>
//                                                 <span${comment.time_create}</span>
//                                                 <a href="#comment-form" data-comment-id=${comment.id}" data-comment-username="${comment.author}" class="reply-btn"><i class="bi bi-reply"></i></a>
//                                                 <i class="bi bi-heart"></i>
//                                             </div>
//                                             <div class="comment-content">
//                                                 ${comment.content}
//                                             </div>
//                                         </div>
//                                     </div>
//                                 </li>
//                             </ul>`;
//             if (comment.is_child) {
//                 console.log(comment.parent_id, comment.id);
//                 document.querySelector(`#comments-list-${comment.parent_id} .reply-comment-${comment.parent_id}`).insertAdjacentHTML("beforeend", commentTemplate);
//             }
//             else {
//                 document.querySelector('.comments').insertAdjacentHTML("beforeend", commentTemplate)
//             }
//             commentForm.reset()
//             commentFormSubmit.disabled = false;
//             commentFormSubmit.innerText = "Добавить комментарий";
//             commentFormParentInput.value = null;
//             replyUser();
//         }
//         catch (error) {
//             console.log(error)
//         }
//     }
//   });
  

document.addEventListener("DOMContentLoaded", function() {
    const csrftoken = document.querySelector('form input[name="csrfmiddlewaretoken"]').value
    const commentForm = document.forms.commentForm;
    const commentFormContent = commentForm.content;
    const commentFormParentInput = commentForm.parent;
    const commentFormSubmit = commentForm.commentSubmit;
    const commentPostId = commentForm.getAttribute('data-post-id');

    commentForm.addEventListener('submit', createComment);

    replyUser()

    function replyUser() {
    document.querySelectorAll('.btn-reply').forEach(e => {
        e.addEventListener('click', replyComment);
    });
    }

    function replyComment() {
    const commentUsername = this.getAttribute('data-comment-username');
    const commentMessageId = this.getAttribute('data-comment-id');
    commentFormContent.value = `${commentUsername}, `;
    commentFormParentInput.value = commentMessageId;
    }
    async function createComment(event) {
        event.preventDefault();
        commentFormSubmit.disabled = true;
        commentFormSubmit.innerText = "Ожидаем ответа сервера...";
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
                            <h6 class="comment-name {% if node.is_root_node or node.get_root.author.username == node.author.username%}by-author{% endif %}">${comment.author}</h6>
                            <span>${comment.time_create}</span>
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
            document.querySelector(`#comment-thread-${comment.parent_id}`).insertAdjacentHTML("beforeend", commentTemplate);
        }
        else {
            document.querySelector('.nested-comments').insertAdjacentHTML("beforeend", commentTemplate)
        }
        commentForm.reset()
        commentFormSubmit.disabled = false;
        commentFormSubmit.innerText = "Добавить комментарий";
        commentFormParentInput.value = null;
        replyUser();
    }
        catch (error) {
            console.log(error)
        }
    }
  });