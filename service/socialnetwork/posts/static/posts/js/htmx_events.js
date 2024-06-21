import { handleHtmxRequest, modalHandler } from "/static/gameblog/js/htmx_events.js";

handleHtmxRequest((e) => {
  const dispatchEl = e.detail.elt
  console.log(dispatchEl);
  if (dispatchEl.id === 'like') {
      const xhr = e.detail.xhr
      const response = JSON.parse(xhr.responseText)
      console.log(response);
      if (response.is_liked) {
          dispatchEl.classList.add("is-active")
      } else {
          dispatchEl.classList.remove("is-active")
      }
      const countLikes = dispatchEl.closest('.card').querySelector('#num-likes-count')
      countLikes.innerText = response.likes_count
  }
});
modalHandler();

