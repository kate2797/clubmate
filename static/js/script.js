displayMap();

function displayMap() {
    if (document.getElementById("coordinates") !== null) {
        let coordinates = document.getElementById("coordinates").value; // Get the coordinates
        let coordinatesArray = coordinates.split(/\s+/);
        coordinatesArray = coordinatesArray.map(Number); // Turn them into floats
        let map = L.map('map').setView([coordinatesArray[0], coordinatesArray[1]], 13); // Display the map
        L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
            attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
            maxZoom: 18,
            id: 'mapbox/streets-v11',
            tileSize: 512,
            zoomOffset: -1,
            accessToken: 'pk.eyJ1Ijoia2F0ZTg2OHQ3OCIsImEiOiJja3o4b3dmc2wweHllMnZueHR4bHhjdXAzIn0.H5EziiaRXBMU0V_EbbEZEw'
        }).addTo(map);
        L.marker([coordinatesArray[0], coordinatesArray[1]]).addTo(map);
    }
}

// pushing rejected??????????
function search() {
    let input, filter, ul, li, a, textValue, inputValue;
    input = document.getElementById("search-input");
    filter = input.value.toUpperCase();
    ul = document.getElementById("elements");
    li = ul.getElementsByTagName("li");
    ul.style.display = 'block'; // Starts being hidden, show it now
    inputValue = input.value;

    if (!inputValue.match(/\S/)) { // If input empty again, hide all search results again
        ul.style.display = 'none';
    }

    for (let i = 0; i < li.length; i++) {
        a = li[i].getElementsByTagName("a")[0];
        textValue = a.textContent || a.innerText;
        if (textValue.toUpperCase().indexOf(filter) > -1) {
            li[i].style.display = "";
        } else {
            li[i].style.display = "none";
        }
    }
}

/** Helper function to conditionally show and hide elements. */
function conditionalDisplay(array) {
    array.forEach(function (element) {
        if (element.style.display === "none") { // If currently hidden, display them
            element.style.display = "block";
        }
    });
}

function resetFilter() {
    let filters = document.getElementsByClassName("filter"); // All filterable elements
    let filtersArr = [].slice.call(filters);
    conditionalDisplay(filtersArr);

    let message = document.getElementById("div-filtering-message");
    if (message.style.display === 'block') { // Hide the error message if it is there
        message.style.display = 'none';
    }
}

function filterBy(condition) {
    let selection = document.getElementsByClassName(condition);
    let filters = document.getElementsByClassName("filter"); // All filterable elements
    let filtersArr = [].slice.call(filters); // Turn into an array
    let selectionArr = [].slice.call(selection);
    let difference = filtersArr.filter(x => selectionArr.indexOf(x) === -1); // Elements that do not have the given

    if (selectionArr.length === 0) {
        displayNoMatchMessage();
    }

    difference.forEach(function (element) {
        element.style.display = "none"; // Display filtered selection
    });
}

/** Helper function that announces that no match was found if user selection is empty. */
function displayNoMatchMessage() {
    let message = document.getElementById("div-filtering-message");
    message.style.display = 'block';
}

function orderReset() {
    let filters = document.getElementsByClassName("filter");
    let filtersArr = [].slice.call(filters);
    conditionalDisplay(filtersArr);
}

function orderHighToLow() {
    let filters = document.getElementsByClassName("filter"); // All filterable elements
    let filtersArr = [].slice.call(filters);
    let div = document.getElementById("filtering");
    let filtersArrLowToHigh = filtersArr.reverse();
    removeDiv(filtersArrLowToHigh, div); // Reset the previous state
    appendDiv(filtersArr, div); // Append in the correct order
}

function orderLowToHigh() {
    let filters = document.getElementsByClassName("filter"); // All filterable elements
    let filtersArr = [].slice.call(filters);
    let filtersArrLowToHigh = filtersArr.reverse(); // Low to High
    let div = document.getElementById("filtering");
    removeDiv(filtersArr, div);
    appendDiv(filtersArrLowToHigh, div); // Append in the correct order
}

/** Helper function to remove a div from another div. */
function removeDiv(array, parent) {
    array.forEach(function (element) {
        parent.parentNode.appendChild(element);
    });
}

/** Helper function to append a div to another div. */
function appendDiv(array, parent) {
    array.forEach(function (element) {
        parent.parentNode.appendChild(element);
    });
}