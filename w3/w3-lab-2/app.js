const form = document.querySelector("#house-form");

form.addEventListener("submit", function (event) {

    // Prevent the form from submitting
    event.preventDefault();

    // Get values
    const name = document.querySelector("#name").value;
    const price = Number(document.querySelector("#price").value);
    const bedrooms = document.querySelector("#bedrooms").value;

    // Check validation
    if (
        name === "" ||
        price === "" || price <= 0 ||
        bedrooms === "" || bedrooms <= 0
    ) {
        // Create error message
        const errorMsg = document.createElement("p");

        errorMsg.textContent = "Please fill in all fields. Bedrooms and House Price must be positive numbers.";

        errorMsg.style.color = "red";

        // Add error to form
        form.appendChild(errorMsg);

        return;
    }

    // Success message
    const successMsg = document.createElement("p");

    successMsg.textContent = "Ready to submit";

    successMsg.style.color = "green";

    form.appendChild(successMsg);
});