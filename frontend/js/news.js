function fetchArticles() {
    fetch('/api/news/db')
        .then(response => response.json())
        .then(data => {
            const articlesContainer = document.getElementById('articles');
            articlesContainer.innerHTML = ''; 

            data.forEach(article => {
                const articleElement = document.createElement('div');
                articleElement.classList.add('article');

                const title = document.createElement('h3');
                title.textContent = article.title;
                articleElement.appendChild(title);

                const description = document.createElement('p');
                description.textContent = article.description;
                articleElement.appendChild(description);
                
                const link = document.createElement('a');
                link.href = article.url;
                link.textContent = 'Read more';
                link.target = '_blank';
                articleElement.appendChild(link);

                articlesContainer.appendChild(articleElement);
            });
        })
        .catch(error => {
            console.error('Error fetching articles:', error);
            const articlesContainer = document.getElementById('articles');
            articlesContainer.innerHTML = '<p>Error loading articles. Please try again.</p>';
        });
}

function fetchMapAlerts(){
    fetch('/api/map/alerts')
        .then(response => response.json())
        .then(data => {
            const alertsContainer = document.getElementById('alerts');
            alertsContainer.innerHTML = ''; 

            data.forEach(alert => {
                const alertElement = document.createElement('div');
                alertElement.classList.add('alert');

                const locationName = document.createElement('h3');
                locationName.textContent = alert.location_name;
                alertElement.appendChild(locationName);

                const latitude = document.createElement('p');
                latitude.textContent = `Latitude: ${alert.latitude}`;
                alertElement.appendChild(latitude);

                const longitude = document.createElement('p');
                longitude.textContent = `Longitude: ${alert.longitude}`;
                alertElement.appendChild(longitude);


                const signals = document.createElement('p');
                signals.textContent = `Signals: ${alert.signals}`;
                alertElement.appendChild(signals);

                alertsContainer.appendChild(alertElement);
            });
        })
        .catch(error => {
            console.error('Error fetching map alerts:', error);
            const alertsContainer = document.getElementById('alerts');
            alertsContainer.innerHTML = '<p>Error loading map alerts. Please try again.</p>';
        });
}