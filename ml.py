from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from sklearn.metrics.pairwise import cosine_similarity
import spacy
import numpy as np

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///professors.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Load pre-trained word embeddings model (e.g., spaCy)
nlp = spacy.load('en_core_web_md')

# Define Professor model
class Professor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    area_of_work = db.Column(db.String(255), nullable=False)
    cabin_number = db.Column(db.String(20))
    contact_details = db.Column(db.String(100))

# Function to preprocess and vectorize text using spaCy
def preprocess_text(text):
    doc = nlp(text)
    return doc.vector.reshape(1, -1)

# Function to recommend professors based on student interests using NLP
def recommend_professors_nlp(student_interests):
    # Preprocess student interests
    student_vector = preprocess_text(student_interests)

    # Load professor data from the database
    professors = Professor.query.all()

    # Preprocess professor areas of work and calculate similarity
    similarities = []
    for professor in professors:
        professor_vector = preprocess_text(professor.area_of_work)
        similarity = cosine_similarity(student_vector, professor_vector)[0][0]
        similarities.append((professor, similarity))

    # Sort professors by similarity and return top recommendations
    recommendations = sorted(similarities, key=lambda x: x[1], reverse=True)[:5]
    recommended_professors = [{'name': professor.name, 'area_of_work': professor.area_of_work, 'cabin_number': professor.cabin_number, 'contact_details': professor.contact_details} for professor, _ in recommendations]
    return recommended_professors

# Route for recommending professors based on student interests
@app.route('/recommend_professors_nlp', methods=['POST'])
def recommend_professors_nlp_endpoint():
    data = request.json
    if 'interests' not in data:
        abort(400)  # Bad request
    student_interests = data['interests']
    recommended_professors = recommend_professors_nlp(student_interests)
    return jsonify(recommended_professors)

if __name__ == '__main__':
    app.run(debug=True)

