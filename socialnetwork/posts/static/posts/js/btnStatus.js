const btnStatus = (isActive, text, btn) => {
  if (isActive) {
    btn.disabled = true;
    btn.innerText = text;
  } else {
    btn.disabled = false;
    btn.innerText = text;
  }
}

export default btnStatus;