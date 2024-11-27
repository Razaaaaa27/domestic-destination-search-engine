import os
import csv
import pandas as pd
import re

# Folder input untuk info dan content
folders = {
    "domestic-destination": {
        "content_folder": "domestic-destination/cleaned_content/",
        "info_folder": "domestic-destination/info/"
    }
}

# Daftar untuk menyimpan semua data gabungan
all_data = []

# Loop untuk setiap kategori
for category, paths in folders.items():
    content_folder = paths["content_folder"]
    info_folder = paths["info_folder"]
    
    # Loop melalui setiap file info di folder info
    for info_filename in os.listdir(info_folder):
        # Baca info metadata
        info_path = os.path.join(info_folder, info_filename)
        with open(info_path, 'r', encoding='utf-8') as info_file:
            info_content = info_file.read()
        
        # Parsing metadata dari file info
        metadata = {"Category": category}  # Tambahkan kategori ke metadata
        for line in info_content.splitlines():
            if line:
                key, value = line.split(": ", 1)
                metadata[key.strip()] = value.strip()
        
        # Pastikan file content sesuai dengan nama file info
        content_filename = info_filename  # Nama file content sama dengan info
        content_path = os.path.join(content_folder, content_filename)
        
        # Baca konten artikel jika file content ada
        if os.path.exists(content_path):
            with open(content_path, 'r', encoding='utf-8') as content_file:
                content = content_file.read()
            metadata["Content"] = content
        else:
            metadata["Content"] = "Content not found"
        
        # Tambahkan data gabungan ke list
        all_data.append(metadata)

# Membaca data dari file CSV yang berisi document index dan titles
document_index = pd.read_csv('document_index_and_titles.csv')

# Fungsi untuk membersihkan dan menormalkan judul
def clean_title(title):
    # Menghapus karakter non-alfabet dan mengganti beberapa karakter khusus
    title = re.sub(r'[^\w\s]', '', title)  # Menghapus tanda baca
    title = title.lower()  # Menjadikan huruf kecil semua
    return title.strip()

# Menyimpan semua data gabungan dalam DataFrame
combined_data = pd.DataFrame(all_data)

# Membersihkan kolom 'Title' di kedua DataFrame
combined_data['Title_clean'] = combined_data['Title'].apply(clean_title)
document_index['Title_clean'] = document_index['Title'].apply(clean_title)

# Melakukan pencocokan berdasarkan judul yang telah dibersihkan
merged_data = pd.merge(combined_data, document_index, left_on='Title_clean', right_on='Title_clean', how='left')

# Memeriksa apakah ada nilai NaN pada 'Doc ID' setelah penggabungan
missing_doc_ids = merged_data[merged_data['Doc ID'].isna()]

# Menampilkan baris yang tidak cocok
if not missing_doc_ids.empty:
    print("Beberapa judul tidak cocok, berikut adalah baris tanpa Doc ID:")
    print(missing_doc_ids[['Title', 'Doc ID']])

# Menghapus kolom 'Title_x' dan 'Title_y' dari hasil penggabungan
merged_data = merged_data.drop(columns=['Title_x', 'Title_y'], errors='ignore')

# Mengatur ulang urutan kolom supaya 'Doc ID' ada di posisi pertama
cols = ['Doc ID'] + [col for col in merged_data.columns if col != 'Doc ID']
merged_data = merged_data[cols]

# Menyimpan hasil penggabungan ke file baru
merged_data.to_csv('merged_combined_data.csv', index=False)

print("Penggabungan selesai, hasil disimpan di 'merged_combined_data.csv'")
