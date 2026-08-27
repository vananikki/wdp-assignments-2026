// Lấy element đầu tiên có class "card"
let card = document.querySelector(".card");


// 1. innerHTML
console.log(card.innerHTML);


// 2. textContent
console.log(card.textContent);


// 3. getAttribute()
console.log(card.getAttribute("data-id"));


// 4. setAttribute()
card.setAttribute("data-id", "42");


// 5. style
card.style.color = "red";

// set timeout for 3 seconds to change the color back to black
function showError() {
    let errorMsg = document.createElement("p");

    errorMsg.textContent = "This field is required.";
    errorMsg.style.color = "red";

    let form = document.querySelector("#house-form");

    form.appendChild(errorMsg);

    setTimeout(function () {
        card.style.color = "black";
        form.removeChild(errorMsg);
    }, 3000); //3000ms -> 3s
}

showError();