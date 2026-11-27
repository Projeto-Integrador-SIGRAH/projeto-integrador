import {Map, TileLayer, FeatureGroup, Control, Polyline} from 'leaflet';

document.addEventListener('DOMContentLoaded', function() {
    // https://leafletjs.com/reference-2.0.0.html#map
    // https://leafletjs.com/reference-2.0.0.html#map-locate
    const addCanoButton = document.querySelector('#add-cano-button');
    const encanamentoLayerCheckbox = document.querySelector('#encanamento-layer-checkbox');

    const canoModal = document.querySelector('#modal-cano');
    const closeButtonModal = document.querySelector('#close-button-modal');
    const form = document.querySelector("#form-cano");

    const alertasLayerCheckbox = document.querySelector('#alertas-layer-checkbox');
    let zoomLevel = 15;
    const deltaCoords = 0.0001;
    let can_create_cano = false;

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
    let polyline_to_create = [];

    const renderCanos = (canos) => {
        canos.forEach((cano) => {
            const coords = JSON.parse(cano.coordenadas);
            const latlngs = coords.map(coord => ({lat: coord[0], lng: coord[1]}));
            polyline_coords.push(...latlngs);
            const polyline = new Polyline(latlngs, {color: 'blue'});
            polyline.addTo(map);
        });
    };

    const getAllCanos = async () => {
        try {
            const response = await fetch('/api/canos/');
            if (!response.ok) {
                throw new Error('Erro ao buscar os canos.');
            }
            const canos = await response.json();
            renderCanos(canos);
        } catch (error) {
            console.error(error);
        }
    };

    getAllCanos();

    map.on('click', function(e) {
        if (!can_create_cano) {
            return;
        }
        const latlng = e.latlng;
        if (clickedLatLngs.length > 1) {
            clickedLatLngs.pop();
            clickedLatLngs.push(latlng);
            let delta = (deltaCoords / zoomLevel) * (map.getZoom());

            for (let i = 0; i < polyline_coords.length; i++) {
                if (Math.abs(polyline_coords[i].lat - latlng.lat) < delta && Math.abs(polyline_coords[i].lng - latlng.lng) < delta) {
                    clickedLatLngs.pop();
                    clickedLatLngs.push(polyline_coords[i]);
                    polyline_path.setLatLngs(clickedLatLngs);
                    polyline_to_create = [];
                    polyline_to_create.push(...clickedLatLngs);
                    break;
                }
            }


            polyline_coords.push(...clickedLatLngs);
            polyline_to_create = [];
            polyline_to_create.push(...clickedLatLngs);
            clickedLatLngs = [];
            polyline_path = null;
            canoModal.showModal();
            return;
        }


        clickedLatLngs.push(latlng);
        polyline_path = new Polyline(clickedLatLngs, {color: 'blue'})
        polyline_path.addTo(map);
    });

    map.on('pointermove', function(e) {
        if (clickedLatLngs.length > 0 && can_create_cano) {
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



    addCanoButton?.addEventListener('click', function() {
        can_create_cano = !can_create_cano;
        if (can_create_cano) {
            addCanoButton.classList.add('bg-red-600');
            addCanoButton.classList.remove('bg-sky-800');
            addCanoButton.classList.add('hover:bg-red-700');
            addCanoButton.classList.remove('hover:bg-sky-700');
            addCanoButton.classList.add('rotate-45');
            addCanoButton.classList.remove('rotate-0');
        } else {
            addCanoButton.classList.add('bg-sky-800');
            addCanoButton.classList.remove('bg-red-600');
            addCanoButton.classList.add('hover:bg-sky-700');
            addCanoButton.classList.remove('hover:bg-red-700');
            addCanoButton.classList.add('rotate-0');
            addCanoButton.classList.remove('rotate-45');
        }
    });

    encanamentoLayerCheckbox.addEventListener('change', function() {
        if (this.checked) {
            getAllCanos();
        } else {
            polyline_coords = [];
            map.eachLayer(function(layer) {
                if (layer instanceof Polyline) {
                    map.removeLayer(layer);
                }
            });
        }
    });

    closeButtonModal.addEventListener('click', function() {
        canoModal.close();
    });

    form.addEventListener("submit", async (event) => {
        event.preventDefault();

        if (!form.reportValidity()) return;

        const formData = new FormData(form);
        const payload = Object.fromEntries(formData.entries());
        const coordinates = JSON.stringify(polyline_to_create.map(coord => [coord.lat, coord.lng]));
        polyline_to_create = [];
        payload.coordenadas = coordinates;

        try {
            const response = await fetch(form.action, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                    "X-CSRFToken": formData.get("csrfmiddlewaretoken"),
                },
                body: JSON.stringify(payload),
            }).catch(error => {
                alert("Erro na requisição:", error);
            });

            const data = await response.json();

            if (!response.ok) {
                alert("Erro ao cadastrar:", JSON.stringify(data, null, 2));
                return;
            }

            form.reset();
            canoModal.close();

        } catch (error) {
            console.error("Erro na requisição:", error);
        }
    });
});