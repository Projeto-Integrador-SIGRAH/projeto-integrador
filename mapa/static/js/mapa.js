import {Map, TileLayer, FeatureGroup, Control, Polyline} from 'leaflet';

document.addEventListener('DOMContentLoaded', function() {
    // https://leafletjs.com/reference-2.0.0.html#map
    // https://leafletjs.com/reference-2.0.0.html#map-locate
    let zoomLevel = 15;
    const deltaCoords = 0.0001;

    const map = new Map('map', {
        center: [-6.11, -38.2],
        zoom: zoomLevel,
    })

    new TileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        referrerPolicy: 'no-referrer-when-downgrade',
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(map);

    let clickedLatLngs = [];
    // https://leafletjs.com/reference-2.0.0.html#polyline
    let polyline_path = null;
    let polyline_coords = [];

    map.on('click', function(e) {
        const latlng = e.latlng;
        if (clickedLatLngs.length > 1) {
            clickedLatLngs.pop();
            clickedLatLngs.push(latlng);
            let delta = (deltaCoords / zoomLevel) * (map.getZoom());

            for (let i = 0; i < polyline_coords.length; i++) {
                if (Math.abs(polyline_coords[i].lat - latlng.lag) < delta && Math.abs(polyline_coords[i].lng - latlng.lng) < delta) {
                    clickedLatLngs.pop();
                    clickedLatLngs.push(polyline_coords[i]);
                    polyline_path.setLatLngs(clickedLatLngs);
                    break;
                }
            }


            polyline_coords.push(...clickedLatLngs);
            clickedLatLngs = [];
            polyline_path = null;
            return;
        }


        clickedLatLngs.push(latlng);
        polyline_path = new Polyline(clickedLatLngs, {color: 'blue'})
        polyline_path.addTo(map);
    });

    map.on('pointermove', function(e) {
        if (clickedLatLngs.length > 0) {
            let zoomMap = map.getZoom();
            let delta = (deltaCoords / zoomLevel) * (zoomMap);
            const latlng = e.latlng;
            if (clickedLatLngs.length > 1) {
                clickedLatLngs.pop();
            }

            let lag = latlng.lat;
            let lng = latlng.lng;

            for (let i = 0; i < polyline_coords.length; i++) {
                if (Math.abs(polyline_coords[i].lat - lag) < delta && Math.abs(polyline_coords[i].lng - lng) < delta) {
                    clickedLatLngs.push(polyline_coords[i]);
                    polyline_path.setLatLngs(clickedLatLngs);
                    return;
                }
            }

            clickedLatLngs.push(latlng);
            polyline_path.setLatLngs(clickedLatLngs);
        }
    });
});