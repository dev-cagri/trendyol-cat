import requests
from bs4 import BeautifulSoup
import json

# Hedef URL'ler
base_url = "https://www.trendyol.com/oyuncu-monitor-x-c106087?sst=BEST_SELLER&pi="
page_urls = [f"{base_url}{i}" for i in range(1, 80)]

# Kullanıcı Tarayıcı Bilgileri
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Ürün Bilgilerini Saklayacağımız Liste
products = []

# Sayfa URL'lerini Gezerek Ürünleri Toplayan Fonksiyon
def scrape_page(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    cards = soup.find_all('div', class_='p-card-wrppr with-campaign-view add-to-bs-card')
    
    for card in cards:
        title = card.find('span', class_='prdct-desc-cntnr-ttl').text.strip()
        content = card.find('span', class_='prdct-desc-cntnr-name').text.strip()
        price = card.find('div', class_='prc-box-dscntd').text.strip()
        page_link = 'https://www.trendyol.com' + card.find('div', class_='p-card-chldrn-cntnr card-border').a['href'].strip()
        review_count = card.find('span', class_='ratingCount').text.strip() if card.find('span', class_='ratingCount') else '0'
        
        product_info = {
            'title': title,
            'content': content,
            'price': price,
            'page_link': page_link,
            'review_count': review_count
        }
        products.append(product_info)

# Tüm Sayfaları Gezmek İçin
for page_url in page_urls:
    scrape_page(page_url)

# JSON Dosyasına Kaydetme
filename = 'trendyol_data.json'
with open(filename, 'w') as f:
    json.dump(products, f, indent=4, ensure_ascii=False)

print(f"{len(products)} ürün verisi {filename} dosyasına kaydedildi.")
