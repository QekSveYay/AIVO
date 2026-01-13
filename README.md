# SmartPlayer

簡介
- 一個以 Python 實作的簡易音樂與文字轉語音播放器。

快速開始（macOS / conda）

1. 建立並啟用 conda 環境（可選名稱 `smartplayer_env`）：

```bash
conda create -n smartplayer_env python=3.10 -y
conda activate smartplayer_env
```

2. 安裝相依套件（建議在啟用的環境下執行）：

```bash
pip install -r requirements.txt
```

> 我已將 `edge_tts` 新增到 `requirements.txt`。

3. 執行程式：

```bash
python gui_main.py
```

常見問題與備註
- 如果使用不同的 Python/conda 環境，請確保在該環境中安裝 `requirements.txt` 內的套件。
- 若要匯出目前環境以便重現，可用：

```bash
conda activate smartplayer_env
conda list --export > conda-packages.txt
pip freeze > pip-freeze.txt
```

需要我為您生成 `environment.yml`（包含套件版本）或把 `requirements.txt` 固定版本嗎？