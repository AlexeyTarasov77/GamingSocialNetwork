import { handleHtmxRequest } from "/static/gameblog/js/htmx_events.js";

handleHtmxRequest((e) => {
    console.log(e);
    const dispatchEl = e.detail.elt
    if (dispatchEl.id === 'bookmark') {
      const xhr = e.detail.xhr
      const response = JSON.parse(xhr.responseText)
      const bookMarkIcon = dispatchEl.querySelector('#bookmark-icon')
      if (response.is_added) {
        markActive(bookMarkIcon)
      } else {
        markInactive(bookMarkIcon)
      }
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