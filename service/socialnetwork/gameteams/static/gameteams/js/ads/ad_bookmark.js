import { handleHtmxRequest } from "/static/gameblog/js/htmx_events.js";
import showToast from "/static/notifications.js";

handleHtmxRequest((e) => {
    const dispatchEl = e.detail.elt
    if (dispatchEl.id === 'bookmark') {
      const xhr = e.detail.xhr
      const response = JSON.parse(xhr.responseText)
      const bookMarkIcon = dispatchEl.querySelector('#bookmark-icon')
      let msg = ''
      if (response.is_added) {
        markActive(bookMarkIcon)
        msg = "Вы добавили обьявление в закладки"
      } else {
        markInactive(bookMarkIcon)
        msg = "Вы удалили обьявление из закладок"
      }
      showToast(msg)
    }

})

const markActive = (el) => {
    el.classList.remove('text-black')
    el.classList.add('text-amber-500')
}

const markInactive = (el) => {
    el.classList.remove('text-amber-500')
    el.classList.add('text-black')
}