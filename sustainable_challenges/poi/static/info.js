

function get_loc(){
    function success(position) {
    const latitude = position.coords.latitude;
    const longitude = position.coords.longitude;
    const accuracy = position.coords.accuracy;

    document.getElementById('lat_id').value = latitude;
    document.getElementById('lon_id').value = longitude;
    document.getElementById('acc_id').value = accuracy;

    document.getElementById('loc_form').submit();
    }

    function error() {
        console.log("Unable to retrieve your location");
    }

    if (!navigator.geolocation) {
        console.log("Location not supported by your browser");
    } else {
        navigator.geolocation.getCurrentPosition(success, error, {enableHighAccuracy: true});
    }
}

var pos = JSON.parse(document.getElementById('position').textContent);
console.log(pos);

var map = L.map('map', {dragging: false}).setView([pos['lat'], pos['lon']], 20);
// L.tileLayer('https://api.maptiler.com/maps/openstreetmap/{z}/{x}/{y}@2x.jpg?key=5CproNoEKyotlpqU4SO8', {
//     attribution: '<a href="https://www.maptiler.com/copyright/" target="_blank">&copy; MapTiler</a> <a href="https://www.openstreetmap.org/copyright" target="_blank">&copy; OpenStreetMap contributors</a>',
//     tileSize: 512,
//     zoomOffset: -1,}).addTo(map);
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: 'Maps <a href="https://www.openstreetmap.org/copyright" target="_blank">&copy; OpenStreetMap contributors</a>',
    tileSize: 512,
    zoomOffset: -1,
pixelRatio:1,}).addTo(map);

marker = new L.marker([pos['lat'], pos['lon']], {dragging: false});
    // marker.on('dragend', function(event){
    //     var marker = event.target;
    //     var position = marker.getLatLng();
    //     marker.setLatLng(new L.LatLng(position.lat, position.lng),{draggable:'false'});
    //     map.panTo(new L.LatLng(position.lat, position.lng))
    // });
map.addLayer(marker);

if(pos['close'] == 'False'){
    document.getElementById("close").innerHTML = "Not close enough to vist place.";
}
else {
    document.getElementById("close").innerHTML = "Visted place of interest succefully.";
}