// Lấy phần tử HTML
const title = document.getElementById("title");
const button = document.getElementById("btn");

// Khi click button
button.addEventListener("click", function () {
    title.textContent = "Hello JavaScript!";
    button.style.backgroundColor = "white";
    button.classList.add("stop");
});
