import {Map, TileLayer, FeatureGroup, Control, Polyline} from 'leaflet';

document.addEventListener('DOMContentLoaded', function() {
    // https://leafletjs.com/reference-2.0.0.html#map
    // https://leafletjs.com/reference-2.0.0.html#map-locate
    const map = new Map('map', {
        center: [-6.11, -38.2],
        zoom: 15
    })

    new TileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        referrerPolicy: 'no-referrer-when-downgrade',
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(map);

    let clickedLatLngs = [];
    // https://leafletjs.com/reference-2.0.0.html#polyline
    let polyline_path = null;

    map.on('click', function(e) {
        const latlng = e.latlng;

        clickedLatLngs.push(latlng);
        polyline_path = new Polyline(clickedLatLngs, {color: 'blue'})
        polyline_path.addTo(map);
        if (clickedLatLngs.length > 1) {
            clickedLatLngs = [];
            polyline_path = null;
        }
    });

    map.on('pointermove', function(e) {
        if (clickedLatLngs.length > 0) {
            const latlng = e.latlng;
            if (clickedLatLngs.length > 1) {
                clickedLatLngs.pop(); // Remove the last point to avoid drawing a line to the same point
            }
            clickedLatLngs.push(latlng);
            polyline_path.setLatLngs(clickedLatLngs);
        }
    });
});