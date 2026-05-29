from flask import Flask, request, jsonify
from flasgger import Swagger
import pickle
import os

# Load model and vectorizer
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

with open("vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

app = Flask(__name__)
swagger = Swagger(app)

@app.route("/")
def home():
    return "Sentiment Analysis API is running!"

@app.route("/predict", methods=["POST"])
def predict():
    """
    Predict sentiment from a review text
    ---
    tags:
      - Sentiment Analysis
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            review:
              type: string
              example: "this product is amazing"
    responses:
      200:
        description: Prediction result
        schema:
          type: object
          properties:
            review:
              type: string
            prediction:
              type: integer
            label:
              type: string
    """
    data = request.get_json()
    review = data["review"]

    review_vec = vectorizer.transform([review])
    prediction = model.predict(review_vec)[0]

    label = "positive" if prediction == 1 else "negative"

    return jsonify({
        "review": review,
        "prediction": int(prediction),
        "label": label
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port)
    
