import os
import joblib
from flask import Flask, request, jsonify

app = Flask(__name__)

# モデルをロードする関数
def load_model():
    model_path = os.path.join(os.path.dirname(__file__), 'model', 'rent_prediction_model.joblib')
    model = joblib.load(model_path)
    return model

# グローバル変数としてモデルを保持
model = load_model()

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    prediction = model.predict([[data['area'], data['rooms']]])
    return jsonify({'prediction': prediction[0]})

if __name__ == '__main__':
    app.run()
