// function fetchData() {
//     return new Promise((resolve) => {
//         setTimeout(() => {
//             resolve("Data received!");
//         }, 2000);
//     });
// }

// console.log("Start");

// fetchData()
//     .then((data) => {
//         console.log(data);
//     });

// console.log("End");

function fetchData() {
    return new Promise((resolve) => {
        setTimeout(() => {
            resolve("Data received!");
        }, 2000);
    });
}

async function getData() {
    console.log("Start");

    const data = await fetchData();

    console.log(data);
    console.log("End");
}

getData();