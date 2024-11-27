import os
import re
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer

# Direktori input dan output
input_directories = ["domestic-destination/cleaned_content"]
output_directories = ["domestic-destination/content_processed"]

# Membuat direktori output jika belum ada
for output_directory in output_directories:
    os.makedirs(output_directory, exist_ok=True)

# Inisialisasi Lemmatizer NLTK
lemmatizer = WordNetLemmatizer()

# Daftar stopwords terbaru
custom_stopwords = {
    "ada", "adanya", "adalah", "adapun", "agak", "agaknya", "agar", "akan", "akankah", "akhirnya", "aku", "akulah",
    "amat", "amatlah", "anda", "andalah", "antar", "diantaranya", "antara", "antaranya", "diantara", "apa", "apaan",
    "mengapa", "apabila", "apakah", "apalagi", "apatah", "atau", "ataukah", "ataupun", "bagai", "bagaikan", "sebagai",
    "sebagainya", "bagaimana", "bagaimanapun", "sebagaimana", "bagaimanakah", "bagi", "bahkan", "bahwa", "bahwasanya",
    "sebaliknya", "banyak", "sebanyak", "beberapa", "seberapa", "begini", "beginian", "beginikah", "beginilah",
    "sebegini", "begitu", "begitukah", "begitulah", "begitupun", "sebegitu", "belum", "belumlah", "sebelum", 
    "sebelumnya", "sebenarnya", "berapa", "berapakah", "berapalah", "berapapun", "betulkah", "sebetulnya", "biasa", 
    "biasanya", "bila", "bilakah", "bisa", "bisakah", "sebisanya", "boleh", "bolehkah", "bolehlah", "buat", "bukan", 
    "bukankah", "bukanlah", "bukannya", "cuma", "percuma", "dahulu", "dalam", "dan", "dapat", "dari", "daripada", 
    "dekat", "demi", "demikian", "demikianlah", "sedemikian", "dengan", "depan", "di", "dia", "dialah", "dini", "diri", 
    "dirinya", "terdiri", "dong", "dulu", "enggak", "enggaknya", "entah", "entahlah", "terhadap", "terhadapnya", "hal", 
    "hampir", "hanya", "hanyalah", "harus", "haruslah", "harusnya", "seharusnya", "hendak", "hendaklah", "hendaknya", 
    "hingga", "sehingga", "ia", "ialah", "ibarat", "ingin", "inginkah", "inginkan", "ini", "inikah", "inilah", "itu", 
    "itukah", "itulah", "jangan", "jangankan", "janganlah", "jika", "jikalau", "juga", "justru", "kala", "kalau", 
    "kalaulah", "kalaupun", "kalian", "kami", "kamilah", "kamu", "kamulah", "kan", "kapan", "kapankah", "kapanpun", 
    "dikarenakan", "karena", "karenanya", "ke", "kecil", "kemudian", "kenapa", "kepada", "kepadanya", "ketika", 
    "seketika", "khususnya", "kini", "kinilah", "kiranya", "sekiranya", "kita", "kitalah", "kok", "lagi", "lagian", 
    "selagi", "lah", "lain", "lainnya", "melainkan", "selaku", "lalu", "melalui", "terlalu", "lama", "lamanya", 
    "selama", "selama", "selamanya", "lebih", "terlebih", "bermacam", "macam", "semacam", "maka", "makanya", 
    "makin", "malah", "malahan", "mampu", "mampukah", "mana", "manakala", "manalagi", "masih", "masihkah", 
    "semasih", "masing", "mau", "maupun", "semaunya", "memang", "mereka", "merekalah", "meski", "meskipun", 
    "semula", "mungkin", "mungkinkah", "nah", "namun", "nanti", "nantinya", "nyaris", "oleh", "olehnya", "seorang", 
    "seseorang", "pada", "padanya", "padahal", "paling", "sepanjang", "pantas", "sepantasnya", "sepantasnyalah", 
    "para", "pasti", "pastilah", "per", "pernah", "pula", "pun", "merupakan", "rupanya", "serupa", "saat", "saatnya", 
    "sesaat", "saja", "sajalah", "saling", "bersama", "sama", "sesama", "sambil", "sampai", "sana", "sangat", 
    "sangatlah", "saya", "sayalah", "se", "sebab", "sebabnya", "sebuah", "tersebut", "tersebutlah", "sedang", 
    "sedangkan", "sedikit", "sedikitnya", "segala", "segalanya", "segera", "sesegera", "sejak", "sejenak", "sekali", 
    "sekalian", "sekalipun", "sesekali", "sekaligus", "sekarang", "sekitar", "sekitarnya", "sela", "selain", 
    "selalu", "seluruh", "seluruhnya", "semakin", "sementara", "sempat", "semua", "semuanya", "sendiri", "sendirinya", 
    "seolah", "seperti", "sepertinya", "sering", "seringnya", "serta", "siapa", "siapakah", "siapapun", "disini", 
    "disinilah", "sini", "sinilah", "sesuatu", "sesuatunya", "suatu", "sesudah", "sesudahnya", "sudah", "sudahkah", 
    "sudahlah", "supaya", "tadi", "tadinya", "tak", "tanpa", "setelah", "telah", "tentang", "tentu", "tentulah", 
    "tentunya", "tertentu", "seterusnya", "tapi", "tetapi", "setiap", "tiap", "setidaknya", "tidak", "tidakkah", 
    "tidaklah", "toh", "waduh", "wah", "wahai", "sewaktu", "walau", "walaupun", "wong", "yaitu", "yakni", "yang"
}

# Fungsi untuk preprocessing teks
def preprocess_text(text):
    # 1. Case folding (huruf kecil semua)
    text = text.lower()
    # 1. Remove punctuations dan angka
    text = re.sub(r'\d+', '', text)  # Hapus angka
    text = re.sub(r'[^\w\s]', '', text)  # Hapus tanda baca
    
    # 2. Hapus stopwords
    tokens = text.split()
    filtered_tokens = [token for token in tokens if token not in custom_stopwords]
    
    # 3. Lemmatization
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in filtered_tokens]
    
    # 4. Return token hasil
    return lemmatized_tokens

# Looping melalui direktori input dan file txt di dalamnya
for input_dir, output_dir in zip(input_directories, output_directories):
    for file_name in os.listdir(input_dir):
        if file_name.endswith(".txt"):
            # Baca teks dari file
            with open(os.path.join(input_dir, file_name), 'r', encoding='utf-8') as f:
                text = f.read()
            
            # Preprocessing teks
            processed_tokens = preprocess_text(text)
            
            # Simpan hasil preprocessing ke file baru, tiap kata di baris baru
            output_path = os.path.join(output_dir, file_name)
            with open(output_path, 'w', encoding='utf-8') as f:
                for token in processed_tokens:
                    f.write(token + '\n')  # Menulis setiap token di baris baru

print("Preprocessing selesai!")
