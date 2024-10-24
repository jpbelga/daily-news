import asyncio
import aiohttp
from bs4 import BeautifulSoup
from django.http import JsonResponse

# Asynchronous version of the YCombinator news scraper
async def scrape_YCnews():
    url = "https://news.ycombinator.com/"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            html_content = await response.text()
            soup = BeautifulSoup(html_content, "html.parser")
            
            # Example of scraping headlines (adjust based on your target site)
            headlines = []
            for item in soup.find_all('tr', class_='athing'):
                anchor = item.find('span', class_='titleline').find('a')
                title = anchor.text
                link = anchor['href'] if anchor['href'].startswith('http') else f"https://news.ycombinator.com/{anchor['href']}"
                headlines.append({'title': title, 'link': link})
    
            return headlines

# Asynchronous version of the BBC news scraper
async def scrape_BBCnews():
    url = "https://bbc.com"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            html_content = await response.text()
            soup = BeautifulSoup(html_content, "html.parser")
    
            articles = soup.find('div', {'data-testid': 'vermont-section'})
            testid = ['westminster-card', 'edinburgh-card', 'manchester-card']
            
            articles_filtered = []
            for id in testid:
                anchor = articles.find_all('div', {'data-testid': id})
                articles_filtered = articles_filtered + anchor
    
            # List to hold scraped articles
            scraped_articles = []

            # Extract data from each article card
            for article in articles_filtered:
                title = article.find('h2', {'data-testid': 'card-headline'}).text
                description = article.find('p', {'data-testid': 'card-description'}).text
                link = article.find('a')['href'] if article.find('a')['href'].startswith('http') else f"https://bbc.com{article.find('a')['href']}"
                image = article.find_all('img')[1]['src'] if article.find('img') else None
    
                # Append article data to the list
                scraped_articles.append({
                    'title': title,
                    'description': description,
                    'link': link,
                    'image': image
                })
    
            return scraped_articles
        
async def scrape_Guardian():
    url = "https://www.theguardian.com/international"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            html_content = await response.text()
            soup = BeautifulSoup(html_content, "html.parser")
    
            #print(soup.find('div', {'id': "container-headlines"}).find('ul'))
            article_containers = soup.find('div', {'id': "container-headlines"}).find_all('li')
    
            # Extract the required information from each article
            articles = []
            titles = set()
            for container in article_containers:
                # Find the title
                title_element = container.find('h3')
                if(title_element):
                    title = title_element.get_text(strip=True)
                else: continue
                if(title in titles): continue
                titles.add(title)
                # Find the description
                description_element = container.find('div', class_='dcr-1s6fk2h')
                description = description_element.get_text(strip=True) if description_element else None

                # Find the link
                link_element = container.find('a', href=True)
                link = f"https://www.theguardian.com/{link_element['href']}" if link_element else None

                # Find the image
                image_element = container.find('img')
                image = image_element['src'] if image_element else None

                # Append the article to the list
                articles.append({
                    'title': title,
                    'description': description,
                    'link': link,
                    'image': image
                })

            return articles

async def scrape_Valor():
    url = "https://valor.globo.com/"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            html_content = await response.text()
            soup = BeautifulSoup(html_content, "html.parser")
    
            articles = []
            for highlight in soup.find_all('div', class_='highlight'):
                title_tag = highlight.find('h2', class_='highlight__title')
                description_tag = highlight.find('p', class_='highlight__subtitle')
                image_tag = highlight.find('img')  # Find the image tag
                if title_tag and description_tag:
                    # Extract title and description text
                    title = title_tag.get_text(strip=True)
                    description = description_tag.get_text(strip=True)
                    link = title_tag.find('a')['href']
                    # Set image to None (no image extraction logic is implemented here)
                    image = image_tag['src'] if image_tag else None

                    articles.append({
                        'title': title,
                        'description': description,
                        'link': link,
                        'image': image
                    })

        # Print extracted articles
        return articles
    
# Main function to run both scrapers concurrently
async def run_scrapers():
    tasks = [
        asyncio.create_task(scrape_YCnews()),
        asyncio.create_task(scrape_BBCnews()),
        asyncio.create_task(scrape_Guardian()),
        asyncio.create_task(scrape_Valor())
    ]
    
    # Wait for both scrapers to complete
    results = await asyncio.gather(*tasks)
    
    return {'BBCnews': results[1], 'YCnews': results[0], 'Guardian': results[2], 'Valor':results[3]}

# Running the asynchronous scrapers
if __name__ == "__main__":
    asyncio.run(run_scrapers())
