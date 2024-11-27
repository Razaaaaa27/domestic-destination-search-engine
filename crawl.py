import requests
import datetime as dt
import os
from bs4 import BeautifulSoup, Comment
import re

# Fungsi untuk membersihkan nama file atau direktori dari karakter yang tidak valid di Windows
def sanitize_filename(filename):
    return re.sub(r'[\\/*?:"<>|]', "", filename)

# Set tanggal mulai dan tanggal akhir
start_date = dt.date(2019, 11, 6)
end_date = dt.date(2024, 11, 6)

# Target jumlah dokumen kategori
target_category = 3000

# Variabel untuk menghitung jumlah tautan kategori
links_teknologi = 0

# Buat direktori utama untuk kategori dan sub-direktori untuk content dan info
for category in ['domestic-destination']:
    if not os.path.exists(category):
        os.makedirs(category)
    for folder in ['content', 'info']:
        path = os.path.join(category, folder)
        if not os.path.exists(path):
            os.makedirs(path)

# Set untuk menyimpan URL yang sudah ada agar menghindari duplikasi
existing_urls = set()

total_downloaded = 0

# Loop untuk setiap kategori
current_date = end_date
while current_date >= start_date and links_teknologi < target_category:
    url = f'https://travel.detik.com/domestic-destination/indeks/1?date={current_date.month:02d}/{current_date.day:02d}/{current_date.year}'

    # Request halaman
    try:
        page = requests.get(url)
        page.raise_for_status()
        soup = BeautifulSoup(page.text, 'html.parser')
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while requesting the page: {e}")
        break

    articles = soup.find_all('article', class_='list-content__item')

    # Iterasi melalui setiap artikel
    for article in articles:
        if links_teknologi >= target_category:
            break  # Hentikan jika sudah mencapai target

        link = article.find('a', class_='media__link')
        if link:
            article_url = link['href']
            if article_url in existing_urls:
                continue  # Skip jika URL sudah ada

            # Mengambil URL gambar dari elemen img
            img_tag = article.find('span', class_='ratiobox ratiobox--4-3 lqd').find('img')
            img = img_tag['src'] if img_tag else "Image not found"

            # Mengambil judul artikel
            title = article.find('h3', class_='media__title').text.strip()
            date = article.find('div', class_='media__date').text.strip()


            # Bersihkan nama title untuk dijadikan nama file
            sanitized_title = sanitize_filename(title)

            # Ambil konten artikel
            try:
                cPage = requests.get(article_url)
                cPage.raise_for_status()
                cSoup = BeautifulSoup(cPage.text, 'html.parser')
            except requests.exceptions.RequestException as e:
                print(f"An error occurred while requesting the article: {e}")
                continue

            content_div = cSoup.find('div', class_='detail__body-text')
            if content_div:
                elements = content_div.find_all(['h2', 'h3', 'h4', 'p'])
                content = '\n'.join([element.get_text() for element in elements])
            else:
                content = 'Content not found'

            # Tambahkan URL ke set existing_urls
            existing_urls.add(article_url)

            # Simpan informasi (judul, tanggal, gambar, kategori, URL) ke folder info
            with open(os.path.join('domestic-destination', 'info', f'{sanitized_title}.txt'), 'w', encoding='utf-8') as info_file:
                info_file.write(f"Title: {title}\n")
                info_file.write(f"Date: {date}\n")
                info_file.write(f"Image URL: {img}\n")
                info_file.write(f"Category: domestic-destination\n")
                info_file.write(f"URL: {article_url}\n")  # Tambahkan URL

            # Simpan konten artikel ke folder content
            with open(os.path.join('domestic-destination', 'content', f'{sanitized_title}.txt'), 'w', encoding='utf-8') as content_file:
                content_file.write(content)

            # Tambahkan jumlah dokumen yang berhasil diunduh
            total_downloaded += 1
            links_teknologi += 1

            # Output setiap dokumen yang berhasil diunduh
            print(f"Document {total_downloaded} from category domestic-destination has been downloaded.")

    # Kurangi tanggal dengan 1 hari
    current_date -= dt.timedelta(days=1)

print(f"Data telah disimpan ke direktori. Total dokumen yang diunduh: {total_downloaded}")
