window.addEventListener("load", (event) => {
    function success(position) {
        const latitude = position.coords.latitude;
        const longitude = position.coords.longitude;

        document.getElementById('lat_field').value = latitude;
        document.getElementById('lon_field').value = longitude;
    }

    function error() {
        console.log("Unable to retrieve your location");
        var form = document.getElementById("form").parentElement;
        form.innerHTML = "<div class='col-sm-12 col-md-8 d-flex justify-content-center align-items-center bg-white rounded text-center'>You cannot report without location services enabled.</div>";
    }

    if (!navigator.geolocation) {
        console.log("Location not supported by your browser");
        var form = document.getElementById("form").parentElement;
        form.innerHTML = "<div class='col-sm-12 col-md-8 d-flex justify-content-center align-items-center bg-white rounded text-center'>You cannot report without location services enabled.</div>";
    } else {
        navigator.geolocation.getCurrentPosition(success, error, {enableHighAccuracy: true});
    }
});