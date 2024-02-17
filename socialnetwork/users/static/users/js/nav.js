// const links = document.querySelector('.nav-link');
// const biography = document.querySelector('.content__bio');
// const followingList = document.querySelector('.content__following');
// const followersList = document.querySelector('.content__followers');
// const friendsList = document.querySelector('.content__friends');
// const mainContent = document.querySelector('.content__main');

// links.forEach(link => link.addEventListener('click', clickAction));

// function clickAction(event) {
//   [mainContent, biography, followingList, followersList, friendsList].forEach(el => el.classList.add('none'))
//   switch (event.target.dataset.name) {
//     case "bio":
//         biography.classList.remove('none');
//         break;

//     case "friends":
//         friendsList.classList.remove('none');
//         break;

//     case "following":
//         followingList.classList.remove('none');
//         break;

//     case "followers":
//         followersList.classList.remove('none');
//         break;
  
//     default:
//         mainContent.classList.remove('none')
//         break;
//   }
// }

$(document).ready(function () {
  hideContent(true);
})

function hideContent(initial) {
  $('.content__bio').hide();
  $('.content__following').hide();
  $('.content__followers').hide();
  $('.content__friends').hide();
  if (!initial) {
    $('.content__main').hide()
    $('.nav-link').removeClass('active');
  }
  // initial ? '' : $('.content__main').hide();
  // $('.nav-link').removeClass('active');
}

function clickAction(clickedItem) {
  hideContent(false);
  $(`[data-name="${clickedItem}"]`).addClass('active');
  $(`.content__${clickedItem}`).show()
}

