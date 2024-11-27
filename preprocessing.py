import os
import re

# List folder input dan folder output
folders = {
    "domestic-destination": ("domestic-destination/content", "domestic-destination/cleaned_content")
}

# Loop melalui setiap kategori folder
for category, (input_folder, output_folder) in folders.items():
    # Buat folder output jika belum ada
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Loop melalui setiap file di folder input
    for filename in os.listdir(input_folder):
        input_file_path = os.path.join(input_folder, filename)
        
        # Pastikan hanya file teks yang diproses
        if not filename.endswith(".txt"):
            continue
        
        # Baca isi file
        with open(input_file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Hapus bagian "ADVERTISEMENT" dan teks berikutnya
        content = re.sub(r"ADVERTISEMENT\s+SCROLL TO CONTINUE WITH CONTENT", "", content)
        
        # Hapus enter berlebih (lebih dari satu newline berturut-turut)
        content = re.sub(r"\n\s*\n+", "\n\n", content)
        
        # Path untuk file output
        output_file_path = os.path.join(output_folder, filename)
        
        # Tulis konten bersih ke file di folder output
        with open(output_file_path, 'w', encoding='utf-8') as file:
            file.write(content)

print("Proses pembersihan selesai. File hasil disimpan di folder cleaned_content masing-masing kategori.")
