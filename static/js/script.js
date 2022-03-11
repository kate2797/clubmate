$(document).ready(function () {
    // JQuery code here...
});

displayMap();

function displayMap() {
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