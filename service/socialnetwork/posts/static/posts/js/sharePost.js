import btnStatus from "./btnStatus.js";

$('#submit').click(function () { 
    btnStatus(false, 'Отправка...', $(this))
});

// ajax