var map = null;
var marker = {};
var circle = {};

function success(position) {
    const latitude = position.coords.latitude;
    const longitude = position.coords.longitude;

    map = L.map('map').setView([latitude, longitude], 18);
    // L.tileLayer('https://api.maptiler.com/maps/openstreetmap/{z}/{x}/{y}@2x.jpg?key=5CproNoEKyotlpqU4SO8', {
    //     attribution: '<a href="https://www.maptiler.com/copyright/" target="_blank">&copy; MapTiler</a> <a href="https://www.openstreetmap.org/copyright" target="_blank">&copy; OpenStreetMap contributors</a>',
    //     tileSize: 512,
    //     zoomOffset: -1,}).addTo(map);
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: 'Maps <a href="https://www.openstreetmap.org/copyright" target="_blank">&copy; OpenStreetMap contributors</a>',
        tileSize: 512,
        zoomOffset: -1,
    pixelRatio:1,}).addTo(map);
    
    function onLocationFound(e) {
        var radius = e.accuracy / 2;
        if(map.hasLayer(marker)){
            map.removeLayer(marker);
        } 
        if(map.hasLayer(circle)){
            map.removeLayer(circle);
        }
        
        const Icon = L.Icon.extend({options: {
            iconSize: [25, 25],
            iconAnchor: [12, 12]
        }});
        const loc_icon = new Icon({iconUrl: img_src});
        marker = new L.marker(e.latlng, {icon: loc_icon}).addTo(map).bindPopup("You");
        circle = new L.circle(e.latlng, radius).addTo(map);
      }
      
    map.on('locationfound', onLocationFound);
    map.locate({watch: true, 
        enableHighAccuracy: true
    });

    var places = JSON.parse(document.getElementById('places').textContent)['places'];
    
    places.forEach(place => {
        L.marker([place['lat'], place['lon']]).addTo(map).bindPopup("<a href=/poi/info/"+ place['id'] +">" + place['title'] + "</a>");
    });
}

function error() {
    console.log("Unable to retrieve your location");
}

if (!navigator.geolocation) {
    console.log("Location not supported by your browser");
} else {
    navigator.geolocation.getCurrentPosition(success, error);
    
}

