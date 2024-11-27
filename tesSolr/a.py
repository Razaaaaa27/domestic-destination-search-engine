from flask import Flask, request, render_template_string
import pysolr

app = Flask(__name__)

SOLR_URL = "http://localhost:8983/solr/nutch"
solr = pysolr.Solr(SOLR_URL, always_commit=True, timeout=100)

# Template HTML sederhana untuk antarmuka pencarian
html_template = """
<!doctype html>
<html lang="id">
<head><title>Search Engine</title></head>
<body>
    <h1>Pencarian Dokumen</h1>
    <form action="/" method="get">
        <input type="text" name="query" placeholder="Masukkan kata kunci" required>
        <button type="submit">Cari</button>
    </form>
    {% if results %}
        <h2>Hasil Pencarian:</h2>
        <ul>
        {% for result in results %}
            <li><strong>{{ result.title }}</strong><br>
            {{ result.content[:150] }}...<br>
            <a href="{{ result.url }}">Selengkapnya</a></li>
        {% endfor %}
        </ul>
    {% endif %}
</body>
</html>
"""

@app.route("/")
def search():
    query = request.args.get("query", "")
    results = []
    if query:
        # Gunakan field `text` sebagai default field untuk pencarian
        solr_results = solr.search(query, rows=100, **{'df': 'text'})
        for result in solr_results:
            results.append({
                "title": result.get("title", "Judul tidak ditemukan"),  # Sesuaikan nama field ini
                "content": result.get("content", "Konten tidak ditemukan"),  # Sesuaikan nama field ini
                "url": result.get("url", "#")  # Sesuaikan nama field ini
            })
    return render_template_string(html_template, results=results)

if __name__ == "__main__":
    app.run(debug=True)
