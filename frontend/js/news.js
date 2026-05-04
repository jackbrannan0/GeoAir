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