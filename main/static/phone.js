// 모달 참고
// - https://www.walterz.net/2023/04/05/javascript-modal/
// - https://sevendays.tistory.com/30

// const modal = document.getElementById("modal");
// const openModalBtn = document.getElementById("open-modal");
// const closeModalBtn = document.getElementById("close-modal");
// const modalBg = document.getElementById("modal-bg");

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



// 참고: https://webclub.tistory.com/581
var button = document.querySelector(".button");
var modalContainer = document.querySelector("#modal-container");
var closeModal = document.querySelector('#close-modal')
var phone = document.querySelector("#phone");
var btnId = "call";

button.addEventListener("click", function () {
  modalContainer.removeAttribute("class");
  modalContainer.classList.add(btnId);
  phone.classList.add("modal-active");
});

closeModal.addEventListener("click", function () {
  modalContainer.classList.add("out");
  phone.classList.remove("modal-active");
  if (modalContainer.classList.contains(btnId)) {
  }
});


