import { handleHtmxRequest } from "/static/gameblog/js/htmx_events.js";

handleHtmxRequest((e) => {
    console.log(e);
    const dispatchEl = e.detail.elt
    if (dispatchEl.dataset.id === 'tab') {
       clearActiveTabs()
       markActive(dispatchEl)
    }
})

const clearActiveTabs = () => {
    const tabs = document.querySelectorAll('.filter-tab')
    tabs.forEach(tab => markInactive(tab))
}


const markActive = (el) => {
    el.classList.remove('text-white')
    el.classList.add('text-slate-400')
}

const markInactive = (el) => {
    el.classList.remove('text-slate-400')
    el.classList.add('text-white')
}