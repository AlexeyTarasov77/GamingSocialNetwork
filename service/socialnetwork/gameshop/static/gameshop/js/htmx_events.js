import { handleHtmxRequest, modalHandler } from "/static/gameblog/js/htmx_events.js";

handleHtmxRequest(cartActions);
const modal = modalHandler();

function cartActions (e) {
  const xhr = e.detail.xhr
  const dispatchEl = e.detail.elt // the element that dispatched a request
  console.log("cartActions");
  if (dispatchEl.id === 'cart-action') {
    // checking cart actions to add some functionality (applicable only for cart)
    console.log("into if", dispatchEl.getAttribute('data-action'));
    switch (dispatchEl.getAttribute('data-action')) {
      case 'remove':
        dispatchEl.closest('.product-item').remove();
        break;
      case 'order':
        console.log("into order case");
        getPayment(xhr.responseText)
        break;
    }
  }
}

const getPayment = (url) => {
  console.log("into get payment", url);
  modal.hide();
  window.location.href = url
};