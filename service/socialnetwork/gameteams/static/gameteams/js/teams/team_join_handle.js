import { handleHtmxRequest } from "/static/gameblog/js/htmx_events.js";

const handleHtmxResponse = (e) => {
    const dispatchEl = e.detail.elt
    dispatchEl.closest(".join-request").remove()
}

handleHtmxRequest(handleHtmxResponse)