displayMap();

function displayMap() {
    if (document.getElementById("coordinates") !== null) {
        let coordinates = document.getElementById("coordinates").value;
        let coordinatesArray = coordinates.split(/\s+/);
        coordinatesArray = coordinatesArray.map(Number);
        let map = L.map('map').setView([coordinatesArray[0], coordinatesArray[1]], 13);
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

function resetFilter() {
    let filters = document.getElementsByClassName("filter"); // All filterable elements
    let filtersArr = [].slice.call(filters);
    filtersArr.forEach(function (element) {
        if (element.style.display === "none") { // If currently hidden, display them
            element.style.display = "block";
        }
    });
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

// TODO: If selection is empty, announce that no match was found
function displayNoMatchMessage() {
    // let paragraph = document.createElement("p");
    // let text = document.createTextNode("This is new.");
    // paragraph.appendChild(text);
    // paragraph.setAttribute("id", "no-match-message");
    // let child = document.getElementById('filtering');
    // child.parentNode.insertBefore(paragraph, child);

    // reset method
    // setTimeout((paragraph) => {
    //     paragraph.style.display = 'none';
    // }, 70);
}

function orderReset() {
    let filters = document.getElementsByClassName("filter");
    let filtersArr = [].slice.call(filters);
    filtersArr.forEach(function (element) {
        if (element.style.display === "none") { // If currently hidden, display them
            element.style.display = "block";
        }
    });
}

function orderHighToLow() {
    let filters = document.getElementsByClassName("filter"); // All filterable elements
    let filtersArr = [].slice.call(filters);
    let div = document.getElementById("filtering");

    let filtersArrLowToHigh = filtersArr.reverse(); // Reset the previous state
    filtersArrLowToHigh.forEach(function (element) {
        div.parentNode.removeChild(element);
    });

    filtersArr.forEach(function (element) { // Append in the correct order
        div.parentNode.appendChild(element);
    });
}

function orderLowToHigh() {
    let filters = document.getElementsByClassName("filter"); // All filterable elements
    let filtersArr = [].slice.call(filters);
    let filtersArrLowToHigh = filtersArr.reverse(); // Low to High
    let div = document.getElementById("filtering");

    filtersArr.forEach(function (element) { // Reset the previous state
        div.parentNode.removeChild(element);
    });

    filtersArrLowToHigh.forEach(function (element) { // Append in the correct order
        div.parentNode.appendChild(element);
    });
}