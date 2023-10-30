// var button = document.querySelector("#comment-button");
// var modalContainer = document.querySelector("#guestbook-modal-container");
// var closeModal = document.querySelector('#comment-close-modal')
// var comment = document.querySelector("#comment");
// var btnId = "write";

// button.addEventListener("click", function () {
//   modalContainer.removeAttribute("class");
//   modalContainer.classList.add(btnId);
//   comment.classList.add("modal-active");
// });

// closeModal.addEventListener("click", function () {
//   modalContainer.classList.add("out");
//   comment.classList.remove("modal-active");
//   // if (modalContainer.classList.contains(btnId)) {
//   // }
// });

const modal = document.getElementById("guestbook-modal-container");
const openModalBtn = document.getElementById("comment-button");
const closeModalBtn = document.getElementById("comment-close-modal");
const modalBg = document.getElementById("guestbook-modal-background");

// 모달창 열기
openModalBtn.addEventListener("click", () => {
  modal.style.display = "block";
  //   document.body.style.overflow = "hidden"; // 스크롤바 제거
});

// 모달창 닫기
closeModalBtn.addEventListener("click", () => {
  modal.style.display = "none";
  //   document.body.style.overflow = "auto"; // 스크롤바 보이기
});