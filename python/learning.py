import os
from sklearn.model_selection import train_test_split
import pandas as pd
import lightgbm as lgb
import joblib

# カレントディレクトリを変更
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# データの読み込み
df = pd.read_csv("minato-ku_data2.csv")

# 目的変数を作成
df['total_rent'] = df['家賃+管理費']

# 説明変数と目的変数を分ける
y = df['total_rent']
X = df[['築年数', '面積', 'アクセス']]

# 学習用データと評価用データに分割
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=0)

# LightGBM用のデータセット作成
lgb_train = lgb.Dataset(X_train, y_train)
lgb_eval = lgb.Dataset(X_test, y_test, reference=lgb_train)

# LightGBMのパラメータ設定
lgbm_params = {
    'objective': 'regression',
    'metric': 'rmse',        
    'num_leaves': 60
}

# 特徴量の名前を明示的に指定
feature_names = ['築年数', '面積', 'アクセス']

# LightGBM モデルのトレーニング
model = lgb.train(
    lgbm_params,
    lgb_train,
    valid_sets=[lgb_eval],
    num_boost_round=100,
    callbacks=[lgb.early_stopping(stopping_rounds=10)],
    feature_name=feature_names
)

# モデルを保存
joblib.dump(model, '../model/rent_prediction_model.joblib')

# 特徴量重要度の情報を表示
importance = model.feature_importance()
feature_importance = pd.DataFrame({'feature': feature_names, 'importance': importance})
feature_importance = feature_importance.sort_values('importance', ascending=False)

print("\n特徴量重要度:")
for index, row in feature_importance.iterrows():
    print(f"{row['feature']}: {row['importance']}")

print("\nモデルが保存されました。")
