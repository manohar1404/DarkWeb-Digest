import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template_string, jsonify
import threading
import time

app = Flask(__name__)

news_data = []
last_update = None

def fetch_cyber_news():
    url = "https://news.google.com/rss/search?q=cybersecurity+india&hl=en-IN&gl=IN&ceid=IN:en"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.content
    except requests.RequestException as e:
        print(f"Error fetching news: {e}")
        return None

def parse_news(content):
    if not content:
        return []
    
    try:
        soup = BeautifulSoup(content, 'lxml-xml')
        items = soup.find_all('item')
        
        parsed_items = []
        for item in items:
            parsed_items.append({
                'title': item.title.text if item.title else "No title",
                'link': item.link.text if item.link else "No link",
                'pubDate': item.pubDate.text if item.pubDate else "No date",
                'description': item.description.text if item.description else "No description",
                'source': item.source.text if item.source else "Google News"
            })
        
        return parsed_items
    except Exception as e:
        print(f"Error parsing news: {e}")
        return []

def update_news():
    global news_data, last_update
    while True:
        content = fetch_cyber_news()
        news_data = parse_news(content)
        last_update = time.strftime("%Y-%m-%d %H:%M:%S")
        print("Data updated.")
        time.sleep(3600)  # Update every hour

@app.route('/')
def index():
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>DarkWeb Digest</title>
        <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
        <style>
            body {
                background-color: #1a1a1a;
                color: #e0e0e0;
            }
            .news-card {
                background-color: #2a2a2a;
                border-left: 4px solid #4a90e2;
                transition: all 0.3s ease;
            }
            .news-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 10px 20px rgba(74, 144, 226, 0.2);
            }
        </style>
    </head>
    <body class="min-h-screen">
        <nav class="bg-gray-900 p-4">
            <div class="container mx-auto text-center">
                <h1 class="text-4xl font-bold text-white">DarkWeb Digest</h1>
            </div>
        </nav>
        <div class="container mx-auto px-4 py-8">
            <p id="lastUpdate" class="text-sm text-gray-500 mb-4"></p>
            <div id="newsFeed" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"></div>
        </div>
        <script>
        function updateNews() {
            fetch('/get_news')
                .then(response => response.json())
                .then(data => {
                    const newsFeed = document.getElementById('newsFeed');
                    newsFeed.innerHTML = '';
                    data.news.forEach(item => {
                        const article = document.createElement('div');
                        article.className = 'news-card p-6 rounded-lg shadow-lg';
                        article.innerHTML = `
                            <h2 class="text-xl font-semibold mb-3 text-blue-400">${item.title}</h2>
                            <p class="text-gray-400 mb-2 text-sm"><span class="font-semibold">Source:</span> ${item.source}</p>
                            <p class="text-gray-400 mb-4 text-sm"><span class="font-semibold">Date:</span> ${item.pubDate}</p>
                            <p class="mb-4 text-gray-300">${item.description}</p>
                            <a href="${item.link}" target="_blank" class="text-blue-400 hover:underline">Read full article</a>
                        `;
                        newsFeed.appendChild(article);
                    });
                    document.getElementById('lastUpdate').textContent = `Last updated: ${data.last_update}`;
                });
        }
        setInterval(updateNews, 300000);  // Update every 5 minutes
        updateNews();  // Initial update
        </script>
    </body>
    </html>
    ''')

@app.route('/get_news')
def get_news():
    return jsonify({
        'news': news_data,
        'last_update': last_update
    })

if __name__ == "__main__":
    threading.Thread(target=update_news, daemon=True).start()
    app.run(debug=True)
