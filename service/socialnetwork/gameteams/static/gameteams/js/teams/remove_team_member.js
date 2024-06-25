import { handleHtmxRequest } from "/static/gameblog/js/htmx_events.js";

document.addEventListener("DOMContentLoaded", function () {
    handleHtmxRequest((e) => {
        const dispatchEl = e.detail.elt
        if (dispatchEl.id === 'remove-member') {
            dispatchEl.closest(".member-card").remove()
        } 
    });
})