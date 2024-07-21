let model;

// モデルを読み込む
async function loadModel() {
    // Note: この部分は変更が必要です。JavaScriptからjoblibファイルを直接読み込むことはできません。
    // 代わりに、サーバーサイドで予測を行うAPIを作成する必要があります。
    console.log("モデルの読み込みは、サーバーサイドで行う必要があります。");
}

// ページ読み込み時にモデルを読み込む
window.addEventListener('load', loadModel);

document.getElementById('rentForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    const area = parseFloat(document.getElementById('area').value);
    const access = parseFloat(document.getElementById('access').value);
    const age = parseFloat(document.getElementById('age').value);

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ area, access, age }),
        });

        if (!response.ok) {
            throw new Error('予測に失敗しました');
        }

        const result = await response.json();
        document.getElementById('prediction').textContent = Math.round(result.prediction).toLocaleString();
        document.getElementById('result').classList.remove('hidden');
    } catch (error) {
        console.error('Error:', error);
        alert('予測に失敗しました。もう一度お試しください。');
    }
});
