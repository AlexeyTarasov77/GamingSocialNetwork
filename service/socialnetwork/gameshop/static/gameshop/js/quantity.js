document.addEventListener("DOMContentLoaded", function () {
    const plusBtns = document.querySelectorAll('#plus-btn');
    const minusBtns = document.querySelectorAll('#minus-btn');
    plusBtns.forEach(plusBtn => {
        plusBtn.onclick = () => {
        let quantity = plusBtn.closest('#select-quantity').querySelector('input#cart-action')
        let value = parseInt(quantity.value);
        value += 1;
        quantity.value = value;
        htmx.trigger(quantity, 'change')
      }
    })

    minusBtns.forEach(minusBtn => {
        minusBtn.onclick = () => {
        let quantity = minusBtn.closest('#select-quantity').querySelector('input#cart-action')
        let value = parseInt(quantity.value);
        if(value > 1){
            value -= 1;
            quantity.value = value;
            htmx.trigger(quantity, 'change')
        }
      }
    })

})

