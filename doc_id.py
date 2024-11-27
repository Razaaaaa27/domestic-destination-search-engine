import os
import csv

# Folder yang berisi file hasil preprocessing
output_folder = r"C:\Python\Final-Project-PI-Kelompok-3\Source code Final Project Prak PI_Kelompok 4\domestic-destination\content_processed"
output_files = os.listdir(output_folder)

# Membuat daftar judul dokumen dengan doc_id sebagai kunci
document_titles = {}

for doc_id, output_file in enumerate(output_files):
    if output_file.endswith('.txt'):
        # Judul dokumen diambil dari nama file (tanpa ekstensi)
        title = os.path.splitext(output_file)[0]
        # Simpan judul dokumen dengan doc_id sebagai kunci
        document_titles[doc_id] = title

# Menyimpan Document Index dan Judul Dokumen ke dalam berkas CSV
csv_file_path = os.path.join('document_index_and_titles.csv')
with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["Doc ID", "Title"])  # Header untuk kolom CSV
    for doc_id, title in document_titles.items():
        writer.writerow([doc_id, title])

print(f"Document index beserta judul dokumen telah disimpan ke dalam {csv_file_path}.")
