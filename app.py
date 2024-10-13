from flask import Flask, render_template, request, jsonify
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')

app = Flask(__name__)

# Fetch the dataset and initialize vectorizer and LSA globally
newsgroups_data = fetch_20newsgroups(subset='all', remove=('headers', 'footers', 'quotes'))

# Initialize the TF-IDF vectorizer
stop_words = stopwords.words('english')
vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
# Fit the vectorizer to the dataset and transform the documents
X_tfidf = vectorizer.fit_transform(newsgroups_data.data)

# Apply LSA (Truncated SVD for dimensionality reduction)
n_components = 100  # Number of components for LSA
lsa = TruncatedSVD(n_components=n_components, random_state=42)
X_lsa = lsa.fit_transform(X_tfidf)

# Search engine implementation
def search_engine(query):
    """
    Function to search for top 5 similar documents given a query
    Input: query (str)
    Output: documents (list), similarities (list), indices (list)
    """
    # Transform the query into the same TF-IDF space
    query_vec = vectorizer.transform([query])
    
    # Project the query vector into the LSA space
    query_lsa = lsa.transform(query_vec)
    
    # Compute cosine similarity between the query and all documents
    similarities = cosine_similarity(query_lsa, X_lsa)[0]
    
    # Get top 5 most similar documents
    top_indices = np.argsort(similarities)[::-1][:5]
    top_similarities = similarities[top_indices]
    top_documents = [newsgroups_data.data[i] for i in top_indices]
    
    return top_documents, top_similarities.tolist(), top_indices.tolist()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    documents, similarities, indices = search_engine(query)
    return jsonify({'documents': documents, 'similarities': similarities, 'indices': indices}) 

if __name__ == '__main__':
    app.run(debug=True)