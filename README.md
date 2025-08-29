# 🛡️ Watch Out - 隱私保護助手

當同事走到你身後時，螢幕上敏感的內容會自動模糊處理，保護你的隱私。

**情境擴展：** 在咖啡廳、機場等公開場所工作時，也能防止旁人窺視，保護商業機密或個人隱私不外洩。

## 🎯 **智慧臉部偵測**: 使用輕量級臉部辨識模型，支援 NPU 加速。
- 🔒 **自動隱私保護**: 偵測到多人時自動啟動隱私模式。
- 📱 **自由選擇隱私應用程式**: 可自訂在隱私模式下開啟的應用程式，支援不同作業系統配置。
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

本專案提供兩種安裝方式，請根據您的執行環境選擇：

#### 🖥️ CPU 執行環境

如果您想在一般電腦上使用 CPU 執行：

```bash
pip install -r requirements.txt
```

#### ⚡ NPU 加速環境 (Snapdragon X 系列)

如果您使用的是搭載 Snapdragon X Elite/Plus 的裝置，想要使用 NPU 加速：

```bash
pip install -r requirements-qnn.txt
```

#### 相依套件說明

**基本套件** (requirements.txt)：
- `opencv-python`: 用於影像處理與攝影機控制
- `onnxruntime`: 用於運行 ONNX AI 模型 (CPU 版本)
- `numpy`: 高效的數值運算函式庫
- `pyautogui`: 用於螢幕控制（目前版本未使用，為未來功能保留）
- `pillow`: 圖像處理函式庫
- `scipy`: 用於科學計算，在此專案中優化臉部偵測的後處理

**NPU 加速套件** (requirements-qnn.txt)：
- 包含上述所有基本套件
- `onnxruntime-qnn`: 支援 Qualcomm NPU 的 ONNX Runtime 版本

---

## ⚙️ 運行與測試

### 1. 設定與啟動 (推薦方式)

**推薦使用設定工具進行參數調整並直接啟動程式**，這是最便利的使用方式：

```bash
python setup.py
```

設定工具提供以下功能：

- 調整偵測靈敏度、攝影機索引、延遲時間等參數
- **配置隱私保護應用程式**: 為不同作業系統設定開啟的應用程式
- 測試攝影機是否正常運作
- **測試隱私應用程式**: 驗證應用程式是否能正常開啟
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

3. **隱私應用程式測試**:
    - 運行 `python setup.py`。
    - 選擇「2. 修改設定」→「7. 隱私保護應用程式設定」→「4. 測試開啟應用程式」。
    - 系統會嘗試開啟您配置的隱私保護應用程式。

4. **隱私模式驗證**:
    - 保持程式運行。
    - **單人場景**: 確保只有您一人在攝影機畫面中，此時應為「安全模式」，螢幕正常。
    - **多人場景**: 請另一位同事或朋友進入攝影機畫面。在短暫延遲後，程式應切換至「隱私模式」，並自動開啟您配置的隱私保護應用程式。
    - **暫時停用**: 按下 `ESC` 鍵，隱私模式應會暫時解除。

---

## 📱 隱私保護應用程式配置

Watch Out 支援自訂隱私模式下開啟的應用程式，您可以選擇任何您偏好的應用程式來提供隱私保護。

### 支援的配置方式

### 配置方式

#### 1. 透過設定工具配置 (推薦)

```bash
python setup.py
```

**配置步驟**：
1. 選擇「2. 修改設定」
2. 選擇「6. 隱私保護應用程式設定」
3. 選擇要配置的作業系統 (macOS/Windows)
4. 依提示輸入應用程式資訊：
   - 應用程式名稱
   - 開啟命令
   - 備用路徑 (可選)
5. 選擇「4. 測試開啟應用程式」驗證設定
6. 回到主選單選擇「4. 儲存設定」

#### 2. 配置範例

**macOS 設定範例**：
- 應用程式名稱：`Google Chrome`, `Safari`, `Notes`
- 開啟命令：`open -a 'Google Chrome'`, `open -a 'Safari'`
- 備用路徑：`/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`

**Windows 設定範例**：
- 應用程式名稱：`Microsoft Edge`, `Notepad`, `Calculator`
- 開啟命令：`msedge.exe`, `notepad.exe`, `calc.exe`
- 備用路徑：（可選）

#### 3. 自訂應用程式路徑

如需使用特定的應用程式路徑，可在設定工具中設定自訂應用程式路徑（選項 7），輸入完整的執行檔路徑：

**範例**：
- macOS: `/Applications/MyApp.app/Contents/MacOS/MyApp`
- Windows: `C:\Program Files\MyApp\MyApp.exe`

### 備用機制

系統提供多層備用機制確保隱私保護的可靠性：

1. **自訂路徑優先**: 如有設定自訂應用程式路徑，會優先使用
2. **主要應用程式**: 使用為當前作業系統配置的主要應用程式
3. **備用路徑**: 如主要命令失敗，嘗試使用備用路徑
4. **備用應用程式**: 最後嘗試開啟系統預設的備用應用程式

### 常見應用程式配置範例

**瀏覽器類**：
- Chrome: `open -a 'Google Chrome'` (macOS) / `chrome.exe` (Windows)
- Safari: `open -a 'Safari'` (macOS)
- Edge: `msedge.exe` (Windows)

**系統工具類**：
- 記事本: `notepad.exe` (Windows)
- 計算機: `open -a 'Calculator'` (macOS) / `calc.exe` (Windows)
- 文字編輯: `open -a 'TextEdit'` (macOS)

---

## ⚖️ 開源授權

- **專案原始碼**: 本專案採用 **MIT License**。詳細內容請參閱 [LICENSE](LICENSE) 檔案。
- **AI 模型**:
  - **模型名稱**: Lightweight-Face-Detection (`w8a8` 量化版本)
  - **模型來源**: 從 [Qualcomm AI Hub](https://aihub.qualcomm.com/compute/models/face_det_lite) 下載。
  - **模型授權**: 此模型採用 **BSD 3-Clause "New" or "Revised" License**。授權全文請見 `model.onnx/LICENSE` 檔案。
