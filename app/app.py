from flask import Flask, render_template, request
import re
import csv
import math
import os
from collections import Counter, defaultdict

app = Flask(__name__)

# Tentukan path file berdasarkan lokasi app.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Lokasi folder app/
INDEX_PATH = os.path.join(BASE_DIR, '..', 'inverted_index.txt')
COMBINED_DATA_PATH = os.path.join(BASE_DIR, '..', 'merged_combined_data.csv')

# Fungsi untuk memuat inverted index dari file
def load_inverted_index(file_path):
    inverted_index = defaultdict(lambda: defaultdict(int))
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            word, postings = line.strip().split(': ')
            doc_list = re.findall(r'\((\d+), (\d+)\)', postings)
            for doc_id, freq in doc_list:
                inverted_index[int(doc_id)][word] = int(freq)
    return inverted_index

# Fungsi untuk memuat data dokumen dari file CSV
def load_combined_data(file_path):
    combined_data = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            doc_id = int(row['Doc ID'])
            combined_data[doc_id] = {
                'category': row['Category'],
                'title': row['Title_clean'],
                'date': row['Date'],
                'image_url': row['Image URL'],
                'url': row['URL'],
                'content': row['Content'],
            }
    return combined_data

# Fungsi untuk menghitung Jaccard Similarity
def calculate_jaccard_similarity(query_words, doc_words):
    intersection = len(query_words & doc_words)
    union = len(query_words | doc_words)
    return intersection / union if union != 0 else 0

# Fungsi untuk menghitung Cosine Similarity
def calculate_cosine_similarity(query_words, doc_words):
    # Representasi vektor
    query_freq = Counter(query_words)
    doc_freq = doc_words

    # Dot product
    dot_product = sum(query_freq[word] * doc_freq.get(word, 0) for word in query_freq)

    # Magnitude
    query_magnitude = math.sqrt(sum(freq**2 for freq in query_freq.values()))
    doc_magnitude = math.sqrt(sum(freq**2 for freq in doc_freq.values()))

    return dot_product / (query_magnitude * doc_magnitude) if query_magnitude and doc_magnitude else 0

# Fungsi untuk melakukan pencarian
def search_with_algorithm(query, inverted_index, combined_data, algorithm='jaccard', target_category=None):
    query_words = query.lower().split()
    
    results = []
    for doc_id, doc_words_freq in inverted_index.items():
        doc_data = combined_data.get(doc_id, {})
        
        # Filter berdasarkan kategori jika ada
        if target_category and doc_data.get('category', '').lower() != target_category.lower():
            continue
        
        if algorithm == 'jaccard':
            doc_words = set(doc_words_freq.keys())
            query_set = set(query_words)
            similarity = calculate_jaccard_similarity(query_set, doc_words)
        elif algorithm == 'cosine':
            similarity = calculate_cosine_similarity(query_words, doc_words_freq)

        if similarity > 0:
            results.append({
                'content_id': doc_id,
                'title': doc_data.get('title', 'Unknown Title'),
                'similarity': similarity,
                'category': doc_data.get('category', 'Unknown Category'),
                'date': doc_data.get('date', 'Unknown Date'),
                'image_url': doc_data.get('image_url', ''),
                'url': doc_data.get('url', ''),
            })
    
    results = sorted(results, key=lambda x: x['similarity'], reverse=True)
    return results

# Muat data
inverted_index = load_inverted_index(INDEX_PATH)
combined_data = load_combined_data(COMBINED_DATA_PATH)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
def search_results():
    query = request.form.get('query') if request.method == 'POST' else request.args.get('query')
    category = request.form.get('category') if request.method == 'POST' else request.args.get('category', None)
    algorithm = request.form.get('algorithm', 'jaccard')
    
    results = search_with_algorithm(query, inverted_index, combined_data, algorithm=algorithm, target_category=category)
    
    results_per_page = 10
    page = request.args.get('page', 1, type=int)
    total_results = len(results)
    total_pages = (total_results // results_per_page) + (1 if total_results % results_per_page > 0 else 0)
    
    start = (page - 1) * results_per_page
    end = start + results_per_page
    paginated_results = results[start:end]
    
    page_range = range(max(1, page - 3), min(total_pages, page + 2) + 1)

    return render_template(
        'result.html',
        query=query,
        results=paginated_results,
        total_pages=total_pages,
        current_page=page,
        page_range=page_range,
        category=category,
        algorithm=algorithm
    )

@app.route('/content/<int:content_id>')
def content(content_id):
    doc = combined_data.get(content_id, {})
    return render_template('content.html', content=doc)

if __name__ == '__main__':
    app.run(debug=True)
