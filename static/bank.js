// <!-- Button -->
// 토글 참고: https://rading.kr/programming/javascript/js-shortcode/5865/
// const ruleToggleButton = document.getElementById("rule-toggle-button");
// ruleToggleButton.onclick = () => {
//   var divElement = document.querySelector(".rule-toggle");
//   divElement.classList.toggle("disable");
// };

// const ruleToggleButton2 = document.getElementById("rule-toggle-button2");
// ruleToggleButton2.onclick = () => {
//   var divElement = document.querySelector(".rule-toggle2");
//   divElement.classList.toggle("disable");
// };

let clipBoard = document.querySelectorAll(".clipboard");
clipBoard.forEach((target) =>
  target.querySelector("button").addEventListener("click", function () {
    copyAccount(target);
  })
);

function copyAccount(target) {
  var targetText = target.querySelector(".account");
  window.navigator.clipboard.writeText(targetText.textContent).then(() => {
    alert("계좌번호가 복사되었습니다 :)");
  });
}

// 토글 참고: https://jeongah-story.tistory.com/162
let slideUp = (target, duration = 500) => {
  target.style.transitionProperty = "height, margin, padding";
  target.style.transitionDuration = duration + "ms";
  target.style.boxSizing = "border-box";
  target.style.height = target.offsetHeight + "px";
  console.log(target);
  target.offsetHeight;
  target.style.overflow = "hidden";
  target.style.height = 0;
  target.style.paddingTop = 0;
  target.style.paddingBottom = 0;
  target.style.marginTop = 0;
  target.style.marginBottom = 0;
  window.setTimeout(() => {
    target.style.display = "none";
    target.style.removeProperty("height");
    target.style.removeProperty("padding-top");
    target.style.removeProperty("padding-bottom");
    target.style.removeProperty("margin-top");
    target.style.removeProperty("margin-bottom");
    target.style.removeProperty("overflow");
    target.style.removeProperty("transition-duration");
    target.style.removeProperty("transition-property");
  }, duration);
};
let slideDown = (target, duration = 500) => {
  target.style.removeProperty("display");
  let display = window.getComputedStyle(target).display;

  if (display === "none") display = "block";

  target.style.display = display;
  let height = target.offsetHeight;
  target.style.overflow = "hidden";
  target.style.height = 0;
  target.style.paddingTop = 0;
  target.style.paddingBottom = 0;
  target.style.marginTop = 0;
  target.style.marginBottom = 0;
  target.offsetHeight;
  target.style.boxSizing = "border-box";
  target.style.transitionProperty = "height, margin, padding";
  target.style.transitionDuration = duration + "ms";
  target.style.height = height + "px";
  target.style.removeProperty("padding-top");
  target.style.removeProperty("padding-bottom");
  target.style.removeProperty("margin-top");
  target.style.removeProperty("margin-bottom");
  window.setTimeout(() => {
    target.style.removeProperty("height");
    target.style.removeProperty("overflow");
    target.style.removeProperty("transition-duration");
    target.style.removeProperty("transition-property");
  }, duration);
};
let slideToggle = (target, duration = 500) => {
  if (window.getComputedStyle(target).display === "none") {
    return slideDown(target, duration);
  } else {
    return slideUp(target, duration);
  }
};

// ====

let speedAnimation = 400;

let targetIdList = document.querySelectorAll(".bank-list");
targetIdList.forEach((target) =>
  target.querySelector(".triggerToggle").addEventListener("click", function () {
    openToggle(target);
  })
);

function openToggle(target) {
  var targetToggle = target.querySelector(".target");
  slideToggle(targetToggle, speedAnimation);
}
