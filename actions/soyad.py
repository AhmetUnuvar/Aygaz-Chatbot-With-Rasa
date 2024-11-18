import requests
from bs4 import BeautifulSoup
import time

visited_links = set()
surnames = set()  # 'surnames' dictionary yerine set kullanarak benzersiz soyisimleri saklayacağız

def scrape_surnames(url, letter):
    if url in visited_links:
        return
    visited_links.add(url)
    
    print(f"Searching in {letter}: {url}")
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    next_links = soup.select('a.desplegable-item')
    
    if next_links:
        for link in next_links:
            next_url = link['href']
            surname_list_items = soup.select('li.list-item a')
            for item in surname_list_items:
                surname = item.text.split('(')[0].strip()  # Parantezden önceki kısmı alıyoruz
                surnames.add(surname)  # Benzersiz soyisimleri set'e ekliyoruz
            scrape_surnames(next_url, link.text.strip())
    else:
        surname_list_items = soup.select('li.list-item a')
        for item in surname_list_items:
            surname = item.text.split('(')[0].strip()  # Parantezden önceki kısmı alıyoruz
            surnames.add(surname)

def save_surnames(filename):
    with open(filename, 'w', encoding='utf-8') as file:
        for surname in sorted(surnames):
            file.write(f"{surname}\n")  # Sadece soyisimleri yazıyoruz
    print(f"Saved {len(surnames)} unique surnames to {filename}")

def main():
    base_url = 'https://soyadlari.com/turkiye/'
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'r', 's', 't', 'u', 'v', 'y', 'z']
    
    for letter in letters:
        scrape_surnames(f"{base_url}{letter}", letter)
        time.sleep(1)  # to avoid overwhelming the server
        
    save_surnames('turkish_surnames.txt')

if __name__ == "__main__":
    main()
