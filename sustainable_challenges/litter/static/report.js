window.addEventListener("load", (event) => {
    function success(position) {
        const latitude = position.coords.latitude;
        const longitude = position.coords.longitude;

        document.getElementById('lat_field').value = latitude;
        document.getElementById('lon_field').value = longitude;
    }

    function error() {
        console.log("Unable to retrieve your location");
    }

    if (!navigator.geolocation) {
        console.log("Location not supported by your browser");
    } else {
        navigator.geolocation.getCurrentPosition(success, error);
    }
});