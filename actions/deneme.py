from playwright.sync_api import sync_playwright
from urllib.parse import unquote  # URL çözme için

def get_names_from_page(page):
    # Sayfadaki tüm <a> etiketlerini buluyoruz ve href'i kontrol ediyoruz
    name_links = page.query_selector_all('a[href^="/isim/"]')

    names = []
    for link in name_links:
        href = link.get_attribute('href')
        if href and "/isim/" in href:
            # İsim kısmını href'ten alıyoruz ve çöz
            name_text = unquote(href.split("/isim/")[1])
            print(f"Bulunan isim: {name_text}")
            names.append(name_text)

    return names

def scrape_all_names():
    all_names = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Tarayıcıyı görünür yapmak için headless=False
        page = browser.new_page()

        # İlk sayfayı yükle
        page.goto("https://www.nisanyanadlar.com/tum-adlar")
        page.wait_for_load_state("networkidle")  # Sayfanın tamamen yüklenmesini bekle

        while True:
            print(f"Şu an işleniyor: Sayfa")
            names = get_names_from_page(page)
            if names:  # Eğer isimler çekildiyse
                for name in names:
                    if name not in all_names:  # Eğer daha önce eklenmemişse
                        all_names.append(name)
            else:
                print("Sayfa boş geçti veya hata oluştu.")
                break  # Hata varsa döngüyü kır

            # 'Sonraki' sayfa bağlantısını bul ve tıkla
            try:
                # 'Sonraki' sayfa bağlantısını bul
                next_button = page.query_selector('a[rel="next"]')
                if next_button:
                    print("Sonraki sayfa bağlantısı bulunuyor, tıklanıyor...")
                    next_button.click()  # Sonraki sayfaya git
                    page.wait_for_timeout(2000)  # 2 saniye bekle
                    page.wait_for_load_state("networkidle")  # Sayfanın yüklenmesini bekle
                else:
                    print("Sonraki sayfa bağlantısı bulunamadı.")
                    break
            except Exception as e:
                print(f"Hata: {e}")
                break

        # Tüm isimleri dosyaya yazalım
        with open("isimler_playwright3.txt", "w", encoding="utf-8") as file:
            for name in all_names:
                file.write(name + "\n")
        
        print("Tüm isimler 'isimler_playwright3.txt' dosyasına kaydedildi.")
        browser.close()

if __name__ == "__main__":
    scrape_all_names()
