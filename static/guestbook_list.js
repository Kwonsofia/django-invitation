let deleteButtons = document.querySelectorAll("#guestbook-content");
deleteButtons.forEach((target) => {
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

console.log(1111)

document.querySelector('#close-guestbooks').addEventListener("click", function () {
  window.history.back();
});