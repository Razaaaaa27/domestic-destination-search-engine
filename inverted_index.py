import os
from collections import Counter

# Fungsi untuk membangun Inverted Index dari file yang sudah diproses
def build_inverted_index_from_processed_file(file_path, doc_id):
    with open(file_path, 'r', encoding='utf-8') as file:
        tokens = file.read().splitlines()  # Membaca file dan memisahkan setiap token per baris
    
    # Menghitung frekuensi term dalam dokumen
    term_frequency = Counter(tokens)
    
    # Membuat inverted index
    index = {}
    for term, freq in term_frequency.items():
        if term not in index:
            index[term] = []
        index[term].append((doc_id, freq))
    
    return index

# Direktori tempat file hasil yang sudah diproses
output_folder = r"c:\Python\Final-Project-PI-Kelompok-3\tesdulu\domestic-destination\content_processed"
output_files = os.listdir(output_folder)

# Membuat inverted index global
inverted_index = {}

for doc_id, output_file in enumerate(output_files):
    if output_file.endswith('.txt'):
        file_path = os.path.join(output_folder, output_file)

        # Membuat inverted index untuk dokumen ini
        index = build_inverted_index_from_processed_file(file_path, doc_id)

        # Memasukkan ke dalam inverted index global
        for term, positions in index.items():
            if term not in inverted_index:
                inverted_index[term] = []
            inverted_index[term].extend(positions)

# Menyimpan Inverted Index ke dalam berkas
index_file_path = os.path.join('inverted_index.txt')
with open(index_file_path, 'w', encoding='utf-8') as index_file:
    for term, doc_freq_pairs in inverted_index.items():
        doc_freq_str = ', '.join([f"({doc_id}, {freq})" for doc_id, freq in doc_freq_pairs])
        index_file.write(f"{term}: {doc_freq_str}\n")

print(f"Inverted index telah disimpan ke dalam {index_file_path}.")
