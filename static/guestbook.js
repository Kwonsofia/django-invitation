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
  phone.classList.add("modal-active");
});

writeCloseModal.addEventListener("click", function () {
  guestbookModalContainer.classList.add("out");
  phone.classList.remove("modal-active");
});