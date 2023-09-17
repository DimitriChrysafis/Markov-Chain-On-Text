import requests
from bs4 import BeautifulSoup
from newsapi import NewsApiClient

with open('key.txt', 'r') as key_file:
    API_KEY = key_file.read().strip()

newsapi = NewsApiClient(api_key=API_KEY)

query = 'Tesla'
page_size = 5

try:
    search_results = newsapi.get_everything(q=query, page_size=page_size)

    if search_results['status'] == 'ok':
        articles = search_results['articles']
        with open('writing.txt', 'w', encoding='utf-8') as file:
            for idx, article in enumerate(articles):
                title = article['title']
                link = article['url']

                article_response = requests.get(link)
                if article_response.status_code == 200:
                    # Parse the HTML content using BeautifulSoup
                    soup = BeautifulSoup(article_response.content, 'html.parser')

                    # Extract the text from the parsed HTML
                    article_text = soup.get_text()
                else:
                    article_text = f"Failed to retrieve article content from {link}"

                article_text = f"Title: {title}\nContent: {article_text}\nLink: {link}\n"

                file.write(article_text)

                print(f"Article {idx + 1}:\n{article_text}")
    else:
        print("Failed to retrieve Tesla news from the News API")
except Exception as e:
    print(f"An error occurred: {str(e)}")
