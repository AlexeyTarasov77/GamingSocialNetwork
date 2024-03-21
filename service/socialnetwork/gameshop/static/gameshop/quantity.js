document.addEventListener("DOMContentLoaded", function () {
    const plusBtn = document.querySelector('#plus-btn');
    const minusBtn = document.querySelector('#minus-btn');
    const quantity = document.querySelector('#quantity');
    plusBtn.onclick = () => {
        let value = parseInt(quantity.value);
        value += 1;
        quantity.value = value;
    }
    minusBtn.onclick = () => {
        let value = parseInt(quantity.value);
        if(value > 1){
            value -= 1;
            quantity.value = value;
        }
    }
})

