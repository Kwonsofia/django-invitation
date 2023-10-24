// 달력 생성 : 해당 달에 맞춰 테이블을 만들고, 날짜를 채워 넣는다.
function buildCalendar(wedding_year, wedding_month, wedding_day, wedding_time) {
  let firstDate = new Date(wedding_year, wedding_month, 1); // 이번달 1일
  let lastDate = new Date(wedding_year, wedding_month + 1, 0); // 이번달 마지막날

  let tbody_Calendar = document.querySelector("#calender-table > tbody");
  document.getElementById("calYear").innerText = wedding_year; // 연도 숫자 갱신
  document.getElementById("calMonth").innerText = wedding_month + 1; // leftPad(wedding_month + 1);
  document.getElementById("calDay").innerText = wedding_day;
  document.getElementById("calTime").innerText = wedding_time;

  while (tbody_Calendar.rows.length > 0) {
    // 이전 출력결과가 남아있는 경우 초기화
    tbody_Calendar.deleteRow(tbody_Calendar.rows.length - 1);
  }

  let nowRow = tbody_Calendar.insertRow(); // 첫번째 행 추가

  for (let j = 0; j < firstDate.getDay(); j++) {
    // 이번달 1일의 요일만큼
    let nowColumn = nowRow.insertCell(); // 열 추가
  }

  for (let nowDay = firstDate; nowDay <= lastDate; nowDay.setDate(nowDay.getDate() + 1)) {
    // day는 날짜를 저장하는 변수, 이번달 마지막날까지 증가시키며 반복

    let nowColumn = nowRow.insertCell(); // 새 열을 추가하고
    nowColumn.innerText = nowDay.getDate(); // leftPad(nowDay.getDate());  // 추가한 열에 날짜 입력

    // if (nowDay.getDay() == 0) {
    //   // 일요일인 경우 글자색 빨강으로
    //   nowColumn.style.color = "#DC143C";
    // }
    if (nowDay.getDay() == 6) {
      // 토요일인 경우 글자색 파랑으로 하고
      //   nowColumn.style.color = "#0000CD";
      nowRow = tbody_Calendar.insertRow(); // 새로운 행 추가
    }

    if (nowDay.getMonth() == wedding_month && nowDay.getDate() == wedding_day) {
      nowColumn.className = "today";
    }
  }
}

function countWeddingDay(wedding_year, wedding_month, wedding_day) {
  var day_count = document.querySelector("#day-count>span");
  var day_sentence = document.querySelector("#day-count>p");
  const toDate = new Date();
  const weddingDate = new Date(wedding_year, wedding_month, wedding_day);
  let diff = weddingDate.getTime() - toDate.getTime();
  if (diff == 0) {
    day_sentence.innerText = "오늘입니다.";
  } else {
    diff = Math.ceil(diff / (1000 * 60 * 60 * 24));
    if (diff < 0) {
      day_sentence.innerText = "지났습니다.";
    } else {
      day_count.innerText = diff;
      day_sentence.innerText = "일 남았습니다.";
    }
  }
}

fetch("http://localhost:8000/wedding-day", {
    "method":"GET",
    credentials: "include"})
    .then(res => res.json())
    .then(res => {
        let wedding_year = res['wedding_year'];
        let wedding_month = res['wedding_month'];
        let wedding_day = res['wedding_day'];
        let wedding_time = res['wedding_time'];

        window.onload = function () {
          buildCalendar(wedding_year, wedding_month, wedding_day, wedding_time);
        }; // 웹 페이지가 로드되면 buildCalendar 실행
        countWeddingDay(wedding_year, wedding_month, wedding_day);
    })

// input값이 한자리 숫자인 경우 앞에 '0' 붙혀주는 함수
// function leftPad(value) {
//     if (value < 10) {
//         value = "0" + value;
//         return value;
//     }
//     return value;
// }


