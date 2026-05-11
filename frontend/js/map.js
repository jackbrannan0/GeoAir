
var layerGroup = L.layerGroup().addTo(map);

const highIcon = L.icon({
    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
    iconSize: [25, 41], iconAnchor: [12, 41], popupAnchor: [1, -34], shadowSize: [41, 41]
});

const mediumIcon = L.icon({
    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-blue.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
    iconSize: [25, 41], iconAnchor: [12, 41], popupAnchor: [1, -34], shadowSize: [41, 41]
});






function fetchMapAlerts(){
    fetch('/api/map/alerts')
        
        .then(response => response.json())
        .then(data => {
            console.log("data recieved")
            layerGroup.clearLayers(); 

            data.forEach(alert => {
                console.log("adding marker")
                const signals = JSON.stringify(alert.signals);
                const markerIcon = alert.severity_label === 'high' ? highIcon : mediumIcon;

                const marker = L.marker([alert.latitude, alert.longitude], {icon: markerIcon}).addTo(layerGroup);
                
                marker.bindPopup(`
                    <div style="font-family: sans-serif;">
                        <b style="color: ${alert.severity_label === 'high' ? 'red' : 'navy'};">
                            ${alert.location_name || 'Event Location'}
                        </b><br>
                        <hr>
                        <i>Severity: ${alert.severity_label.toUpperCase()}</i><br>
                        <i>AI Score: ${alert.sentiment_score.toFixed(2)}</i><br>
                        <p style="font-size: 0.9em;">${alert.description || 'No description available.'}</p>
                    </div>
                `);
                
            });
        })
        .catch(error => {
            console.error('Error fetching map alerts:', error);
            const alertsContainer = document.getElementById('alerts');
            alertsContainer.innerHTML = '<p>Error loading map alerts. Please try again.</p>';
        });
}