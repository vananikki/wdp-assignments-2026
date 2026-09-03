const button = document.getElementById("loadBtn");
const predictionList = document.getElementById("predictionList");

button.addEventListener("click", async () => {

    try {
        const response = await fetch("data.json");

        const data = await response.json();

        predictionList.innerHTML = "";

        data.forEach(house => {

            const card = document.createElement("div");

            const title = document.createElement("h3");
            title.textContent = `House ${house.house_id}`;

            const area = document.createElement("p");
            area.textContent = `Area: ${house.area} m²`;

            const bedrooms = document.createElement("p");
            bedrooms.textContent = `Bedrooms: ${house.bedrooms}`;

            const prediction = document.createElement("p");
            prediction.textContent =
                `Predicted Price: ${house.prediction.toLocaleString()} VND`;

            card.appendChild(title);
            card.appendChild(area);
            card.appendChild(bedrooms);
            card.appendChild(prediction);

            predictionList.appendChild(card);
        });

    } catch (error) {
        console.error("Failed to load data:", error);
    }
});