const button = document.getElementById("loadBtn");
const postsContainer = document.getElementById("posts");

button.addEventListener("click", () => {

    fetch("https://jsonplaceholder.typicode.com/posts")
        .then(response => response.json())
        .then(posts => {

            // Xóa dữ liệu cũ nếu có
            postsContainer.innerHTML = "";

            // Loop through JSON response
            posts.forEach(post => {

                // Tạo card
                const card = document.createElement("div");

                const title = document.createElement("h3");
                title.textContent = post.title;

                const body = document.createElement("p");
                body.textContent = post.body;

                // Thêm title và body vào card
                card.appendChild(title);
                card.appendChild(body);

                // Thêm card vào page
                postsContainer.appendChild(card);
            });
        })
        .catch(error => {
            console.log("Error:", error);
        });
});