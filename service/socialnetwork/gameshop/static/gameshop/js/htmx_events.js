import { handleHtmxRequest, modalHandler } from "/static/gameblog/js/htmx_events.js";

handleHtmxRequest(cartActions);
modalHandler();

function cartActions (e) {
  const xhr = e.detail.xhr
  const dispatchEl = e.detail.elt // the element that dispatched a request
  if (dispatchEl.id === 'cart-action') {
    // checking cart actions to add some functionality (applicable only for cart)
    switch (dispatchEl.getAttribute('data-action')) {
      case 'remove':
        dispatchEl.closest('.product-item').remove();
        break;
      case 'order':
        getPayment(xhr.responseText)
        break;
    }
  }
}

const getPayment = (url) => {
  modal.hide();
  window.location.href = url
};