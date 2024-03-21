// function success(position) {
//     const latitude = position.coords.latitude;
//     const longitude = position.coords.longitude;

//     document.getElementById('lat_id').value = latitude;
//     document.getElementById('lon_id').value = longitude;
// }

// function error() {
//     console.log("Unable to retrieve your location");
// }

// if (!navigator.geolocation) {
//     console.log("Location not supported by your browser");
// } else {
//     navigator.geolocation.getCurrentPosition(success, error);
// }

var map = L.map('map').setView([50.735214, -3.531754], 15);
// L.tileLayer('https://api.maptiler.com/maps/openstreetmap/{z}/{x}/{y}@2x.jpg?key=5CproNoEKyotlpqU4SO8', {
//     attribution: '<a href="https://www.maptiler.com/copyright/" target="_blank">&copy; MapTiler</a> <a href="https://www.openstreetmap.org/copyright" target="_blank">&copy; OpenStreetMap contributors</a>',
//     tileSize: 512,
//     zoomOffset: -1,}).addTo(map);
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: 'Maps <a href="https://www.openstreetmap.org/copyright" target="_blank">&copy; OpenStreetMap contributors</a>',
    tileSize: 512,
    zoomOffset: -1,
pixelRatio:1,}).addTo(map);

var marker = {};

function onMapClick(e) {
    if(map.hasLayer(marker)){
        map.removeLayer(marker);
    }
    marker = new L.marker(e.latlng, {draggable:'true'});
    marker.on('dragend', function(event){
        var marker = event.target;
        var position = marker.getLatLng();
        marker.setLatLng(new L.LatLng(position.lat, position.lng),{draggable:'true'});
        map.panTo(new L.LatLng(position.lat, position.lng))
    });
    map.addLayer(marker);
    document.getElementById('lat_id').value = e.latlng.lat;
    document.getElementById('lon_id').value = e.latlng.lng;
};

map.on('click', onMapClick);