document.addEventListener("htmx:afterSwap", function(event) {
    console.log(event.detail.target.id);
    if (event.detail.target.id === 'chat_list') {
        const showNavbar = (toggleId, navId, bodyId) => {
            const toggle = document.getElementById(toggleId),
                nav = document.getElementById(navId),
                bodypd = document.getElementById(bodyId)
            console.log(toggle, nav, bodypd);
            if (toggle && nav && bodypd) {
                toggle.addEventListener('click', () => {
                    nav.classList.toggle('show');
                    toggle.classList.toggle('bx-x');
                    bodypd.classList.toggle('body-pd');
                });
            }
        }
        
        // Вызов функции с указанными идентификаторами элементов
        showNavbar('header-toggle', 'nav-bar', 'body');
    }
});