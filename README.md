# 🛡️ Watch Out - 隱私保護助手

當同事走到你身後時，螢幕上敏感的內容會自動模糊處理，保護你的隱私。

**情境擴展：** 在咖啡廳、機場等公開場所工作時，也能防止旁人窺視，保護商業機密或個人隱私不外洩。

## ✨ 功能特色

- 🎯 **智慧臉部偵測**: 使用輕量級臉部辨識模型，支援 NPU 加速。
- 🔒 **自動隱私保護**: 偵測到多人時自動啟動隱私模式。
- ⚡ **即時響應**: 低延遲的偵測和響應。
- 🛠️ **CLI 設定工具**: 簡單的命令列介面調整設定。
- 📝 **詳細日誌**: 完整的偵測記錄。

---

## 📦 安裝步驟與相依套件

請遵循以下步驟來設定與執行 Watch Out。

### 1. 前置需求

- Python 3.9 或更高版本。
- 系統已安裝 `git`。

### 2. 下載專案

```bash
git clone https://github.com/ms0683436/watchout.git
cd watchout
```

### 3. 建立虛擬環境

建議在虛擬環境中執行此專案，以避免套件版本衝突。

```bash
# 建立虛擬環境
python3 -m venv venv

# 啟動虛擬環境
# macOS / Linux
source venv/bin/activate
# Windows
venv\Scripts\activate
```

### 4. 安裝相依套件

本專案的相依套件已列於 `requirements.txt`。

```bash
pip install -r requirements.txt
```

相依套件列表：

- `opencv-python`: 用於影像處理與攝影機控制。
- `onnxruntime`: 用於運行 ONNX AI 模型。
- `numpy`: 高效的數值運算函式庫。
- `pyautogui`: 用於螢幕控制（目前版本未使用，為未來功能保留）。
- `pillow`: 圖像處理函式庫。
- `scipy`: 用於科學計算，在此專案中優化臉部偵測的後處理。

---

## 🚀 在 Snapdragon X 系列筆電上運行 (NPU 加速)

> ⚠️ **注意**: 此功能尚未在實際的 Snapdragon X 系列硬體上進行測試，功能可行性有待驗證。

為了在搭載 Snapdragon X Elite/Plus 的筆電上獲得最佳效能，建議使用 `QNN` 執行緒提供者 (Execution Provider) 來驅動 NPU 進行 AI 運算。

### 1. ONNX Runtime 的 QNN 執行緒提供者

`onnxruntime` 需要特定組態才能使用 Snapdragon NPU (也稱為 Qualcomm AI Engine)。這通常需要使用為了 Windows on Arm (WoA) 編譯的版本，並包含 QNN 支援。

- **QNN 僅適用於 Windows 且具備 Qualcomm NPU 的裝置。**
- **使用 QnnExecutionProvider 前，請先安裝 `onnxruntime-qnn`：**

  ```bash
  pip install onnxruntime-qnn
  ```

### 2. 如何啟用 NPU 加速

本專案程式碼**預設會嘗試使用 NPU**。`main.py` 中的模型載入邏輯會優先選擇 `QnnExecutionProvider`。如果 QNN 不可用，它會自動切換回 `CPUExecutionProvider`。

您無需修改程式碼即可利用 NPU 加速。只需確保您的 `onnxruntime` 安裝正確。

### 3. 驗證 NPU 是否啟用

運行程式時，請觀察終端機的啟動訊息。

- 如果看到 `['QnnExecutionProvider', 'CPUExecutionProvider']` 或類似的日誌，表示程式正在嘗試使用 QNN。
- 如果 `onnxruntime` 成功初始化 QNN，通常表示 NPU 已被驅動。如果失敗，它會回退到 CPU，您可能會在日誌中看到相關警告。

---

## ⚙️ 運行與測試

### 1. 設定與啟動 (推薦方式)

**推薦使用設定工具進行參數調整並直接啟動程式**，這是最便利的使用方式：

```bash
python setup.py
```

設定工具提供以下功能：

- 調整偵測靈敏度、攝影機索引、延遲時間等參數
- 測試攝影機是否正常運作
- 儲存設定
- **設定完成後可直接從工具內啟動 Watch Out**

在設定工具的主選單中選擇「5. 啟動 Watch Out」即可自動儲存設定並啟動程式。

### 2. 直接啟動主程式 (進階用法)

如果您已完成設定，也可以直接執行主程式：

```bash
python main.py
```

> **如何結束程式**:
>
> - **預覽模式下**: 當臉部預覽視窗開啟時，直接按 `ESC` 鍵即可退出。
> - **背景模式下**: 在終端機中按下 `Ctrl+C` 來結束程式。

### 3. 測試與驗證方式

本專案目前沒有自動化的測試腳本，但您可以透過以下手動方式驗證功能是否正常：

1. **攝影機測試**:
    - 運行 `python setup.py`。
    - 選擇「測試攝影機」選項。
    - 應會彈出視窗顯示即時影像。按 `ESC` 鍵關閉。

2. **臉部偵測驗證**:
    - 運行 `python main.py`。
    - 啟用臉部預覽功能（可於 `setup.py` 中設定）。
    - 程式啟動後，您應該會看到一個預覽視窗，並在偵測到的臉部周圍繪製方框。

3. **隱私模式驗證**:
    - 保持程式運行。
    - **單人場景**: 確保只有您一人在攝影機畫面中，此時應為「安全模式」，螢幕正常。
    - **多人場景**: 請另一位同事或朋友進入攝影機畫面。在短暫延遲後，程式應切換至「隱私模式」，並在終端機顯示提示訊息。
    - **暫時停用**: 按下 `ESC` 鍵，隱私模式應會暫時解除。

---

## ⚖️ 開源授權

- **專案原始碼**: 本專案採用 **MIT License**。詳細內容請參閱 [LICENSE](LICENSE) 檔案。
- **AI 模型**:
  - **模型名稱**: Lightweight-Face-Detection (`w8a8` 量化版本)
  - **模型來源**: 從 [Qualcomm AI Hub](https://aihub.qualcomm.com/compute/models/face_det_lite) 下載。
  - **模型授權**: 此模型採用 **BSD 3-Clause "New" or "Revised" License**。授權全文請見 `model.onnx/LICENSE` 檔案。
