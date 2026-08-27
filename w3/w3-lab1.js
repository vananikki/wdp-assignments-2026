const predictions = [
    { id: 1, name: "An", result: 80 },
    { id: 2, name: "Binh", result: 65 },
    { id: 3, name: "Chi", result: 90 },
    { id: 4, name: "Dung", result: 75 }
];

//  vd filter predictions with result >= 80
function filterPredictions(predictions) {
    const filtered = [];

    for (let i = 0; i < predictions.length; i++) {
        if (predictions[i].result >= 80) {
            filtered.push(predictions[i]);
        }
    }

    return filtered;
}

console.log(filterPredictions(predictions));

// sum the "result" field of all predictions
function sumField(predictions) {
    let total = 0;

    for (let i = 0; i < predictions.length; i++) {
        total += predictions[i].result;
    }

    return total;
}

console.log(sumField(predictions));

// find the prediction with the largest "result" field
function findLargest(predictions) {
    let largest = predictions[0];

    for (let i = 1; i < predictions.length; i++) {
        if (predictions[i].result > largest.result) {
            largest = predictions[i];
        }
    }

    return largest;
}

console.log(findLargest(predictions));

// arrow function
function sumField(predictions) {
    let total = 0;

    for (let i = 0; i < predictions.length; i++) {
        total += predictions[i].result;
    }

    return total;
}