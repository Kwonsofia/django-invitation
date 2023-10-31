// const modal = document.getElementById("guestbook-modal");
// const openModalBtn = document.getElementById("write-guestbook");
// const closeModalBtn = document.getElementById("close-guestbook");
// const modalBg = document.getElementById("guestbook-modal-background");

// // 모달창 열기
// openModalBtn.addEventListener("click", () => {
//   modal.style.display = "block";
//   //   document.body.style.overflow = "hidden"; // 스크롤바 제거
// });

// // 모달창 닫기
// closeModalBtn.addEventListener("click", () => {
//   modal.style.display = "none";
//   //   document.body.style.overflow = "auto"; // 스크롤바 보이기
// });

var writeButton = document.querySelector("#write-guestbook");
var guestbookModalContainer = document.querySelector("#guestbook-modal");
var writeCloseModal = document.querySelector('#close-guestbook')
var comment = document.querySelector("#comment");
var btnWriteId = "write";

writeButton.addEventListener("click", function () {
  guestbookModalContainer.removeAttribute("class");
  guestbookModalContainer.classList.add(btnWriteId);
  comment.classList.add("modal-active");
});

writeCloseModal.addEventListener("click", function () {
  guestbookModalContainer.classList.add("out");
  comment.classList.remove("modal-active");
});


// var deleteButton = document.querySelector("#delete-guestbook");
// var deleteModalContainer = document.querySelector("#delete-modal");
// var deleteCloseModal = document.querySelector('#close-delete-guestbook')
// var detail = document.querySelector("#guestbook-content");
// var btnDeleteId = "delete";

// deleteButton.addEventListener("click", function () {
//   deleteModalContainer.removeAttribute("class");
//   deleteModalContainer.classList.add(btnDeleteId);
//   detail.classList.add("modal-active");
// });

// deleteCloseModal.addEventListener("click", function () {
//   deleteModalContainer.classList.add("out");
//   detail.classList.remove("modal-active");
// });

let deleteButtons = document.querySelectorAll("#guestbook-content");
deleteButtons.forEach((target) => {
  console.log(target)
  var deleteButton = target.querySelector("#delete-guestbook");
  var deleteModalContainer = target.querySelector("#delete-modal");
  var deleteCloseModal = target.querySelector('#close-delete-guestbook')
  var detail = target.querySelector("#guestbook-content");
  var btnDeleteId = "delete";

  deleteButton.addEventListener("click", function () {
    deleteModalContainer.removeAttribute("class");
    deleteModalContainer.classList.add(btnDeleteId);
    detail.classList.add("modal-active");
  });
  
  deleteCloseModal.addEventListener("click", function () {
    deleteModalContainer.classList.add("out");
    detail.classList.remove("modal-active");
  });
});