import { handleHtmxRequest } from "/static/gameblog/js/htmx_events.js";

document.addEventListener("DOMContentLoaded", function () {
    handleHtmxRequest((e) => {
        document.querySelector('#leave-btn').remove()
    });
    toggleMembers();
})

function toggleMembers() {
    const membersContainer = document.querySelector('#members-container');
    const membersShowBtn = document.querySelector('#members-show-btn');
    membersShowBtn.onclick = () => {
        membersContainer.classList.toggle('hidden');
        membersShowBtn.classList.toggle('rotate-180');
    }
}