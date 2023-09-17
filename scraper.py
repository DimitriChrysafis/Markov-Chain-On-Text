import requests
from bs4 import BeautifulSoup
from newsapi import NewsApiClient

with open('key.txt', 'r') as key_file:
    API_KEY = key_file.read().strip()

newsapi = NewsApiClient(api_key=API_KEY)

with open('topics.txt', 'r') as topics_file:
    topics = topics_file.read().splitlines()

page_size = 30

with open('writing.txt', 'w', encoding='utf-8') as file:
    for topic in topics:
        try:
            search_results = newsapi.get_everything(q=topic, page_size=page_size)

            if search_results['status'] == 'ok':
                articles = search_results['articles']
                for idx, article in enumerate(articles):
                    title = article['title']
                    link = article['url']

                    article_response = requests.get(link)
                    if article_response.status_code == 200:
                        soup = BeautifulSoup(article_response.text, 'html.parser')

                        article_text = soup.get_text().replace('\n', ' ').strip()

                        article_text = ' '.join(article_text.split())

                        file.write(f"Topic: {topic}\nTitle: {title}\nContent: {article_text}\nLink: {link}\n\n")
                    else:
                        print(f"Failed to retrieve article content from {link}")

                    print(f"Article {idx + 1} for topic '{topic}'")
            else:
                print(f"Failed to retrieve {topic} news from the News API")
        except Exception as e:
            print(f"An error occurred for topic '{topic}': {str(e)}")
