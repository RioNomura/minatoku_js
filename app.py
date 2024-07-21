from flask import Flask, request, jsonify, send_from_directory
import joblib
import pandas as pd
import os

app = Flask(__name__)

# モデルの読み込み
model_path = os.path.join(os.path.dirname(__file__), 'model', 'rent_prediction_model.joblib')
model = joblib.load(model_path)

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
    data = request.json
    
    # 入力データをDataFrameに変換
    input_data = pd.DataFrame([[
        data['age'],
        data['area'],
        data['access']
    ]], columns=['築年数', '面積', 'アクセス'])
    
    # 予測を実行
    prediction = model.predict(input_data)[0]
    
    return jsonify({'prediction': float(prediction)})

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    app.run(debug=True)