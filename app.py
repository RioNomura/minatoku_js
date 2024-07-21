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

@app.route('/')
def home():
    return '''
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>家賃予測プログラム</title>
    <link rel="stylesheet" href="/static/style.css">
</head>
<body>
    <div class="container">
        <h1>家賃予測プログラム</h1>
        <form id="rentForm">
            <label for="area">面積（平方メートル）:</label>
            <input type="number" id="area" required>
            
            <label for="access">アクセス（最寄り駅からの徒歩分数）:</label>
            <input type="number" id="access" required>
            
            <label for="age">築年数:</label>
            <input type="number" id="age" required>
            
            <button type="submit">予測する</button>
        </form>
        
        <div id="result" class="hidden">
            <h2>予測結果</h2>
            <p>予測された家賃+管理費: <span id="prediction"></span>円</p>
        </div>
    </div>
    <script src="/static/script.js"></script>
</body>
</html>
    '''

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    prediction = model.predict([[data['area'], data['rooms']]])
    return jsonify({'prediction': prediction[0]})

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    app.run()
