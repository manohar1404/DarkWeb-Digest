

---

# DarkWeb Digest - Cybersecurity News Aggregator

This project is a simple web application that aggregates and displays the latest cybersecurity news related to India, fetched from Google News RSS feeds. The app is built using Python's Flask framework for the backend, BeautifulSoup for parsing XML, and TailwindCSS for the frontend. The news feed updates every hour and displays the most recent news articles related to cybersecurity.

## Features
- Aggregates cybersecurity news from Google News based on RSS feeds.
- Auto-updates the news feed every hour.
- Displays the title, source, publication date, and a brief description of each article.
- Clean, dark-themed UI built with TailwindCSS.
- Responsive layout for desktop and mobile devices.
- Auto-refreshes the news feed every 5 minutes on the client side.

## Requirements
- Python 3.x
- Flask
- BeautifulSoup
- Requests
- lxml

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/manohar1404/DarkWeb-Digest.git
   cd darkweb-digest
   ```

2. **Install dependencies**
   It's recommended to use a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Run the Flask app**
   ```bash
   python app.py
   ```

4. **Access the application**
   Once the server starts, open your browser and navigate to `http://127.0.0.1:5000/` to view the app.

## Project Structure

```
.
├── app.py               # Main Flask application
├── requirements.txt     # Python dependencies
├── README.md            # Project documentation
```

## How it Works

- **Fetching News**: The `fetch_cyber_news()` function sends a GET request to the Google News RSS feed. The feed URL is configured to search for news articles related to "cybersecurity" in India.
  
- **Parsing News**: The `parse_news()` function uses BeautifulSoup to parse the XML content of the RSS feed and extracts the relevant fields (title, link, pubDate, description, and source) from each news item.

- **Auto-Updating**: The `update_news()` function runs in a separate thread and updates the news feed every hour by fetching the latest articles and storing them in a global list.

- **Frontend**: The frontend is built using TailwindCSS. The news feed is dynamically updated every 5 minutes using JavaScript's `fetch()` to get new articles from the Flask backend.

## License
This project is licensed under the MIT License.

