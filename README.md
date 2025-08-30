# 🛡️ Watch Out - Privacy Protection Assistant

When colleagues approach behind you, sensitive content on your screen will automatically be blurred to protect your privacy.

**Extended Scenarios:** When working in public places like cafes or airports, it also prevents prying eyes from seeing your screen, protecting business secrets or personal privacy from being exposed.

## 🎯 **Smart Face Detection**: Uses lightweight face recognition models with NPU acceleration support.
- 🔒 **Automatic Privacy Protection**: Automatically activates privacy mode when multiple people are detected.
- 📱 **Customizable Privacy Applications**: Configure which applications to open in privacy mode, supporting different operating system configurations.
- ⚡ **Real-time Response**: Low-latency detection and response.
- 🛠️ **CLI Configuration Tool**: Simple command-line interface for adjusting settings.
- 📝 **Detailed Logging**: Complete detection records.

---

## Team Members

| Name | Email |
|------|--------|
| 高崇宸 | ms0683436@gmail.com |
| 吳尚祐 | lupinwu@gmail.com |
| 吳念臻 | love56565656@gmail.com |

---

## 📦 Installation Steps and Dependencies

Please follow these steps to set up and run Watch Out.

### 1. Prerequisites

- Python 3.9 or higher.
- System with `git` installed.

### 2. Download Project

```bash
git clone https://github.com/ms0683436/watchout.git
cd watchout
```

### 3. Create Virtual Environment

It's recommended to run this project in a virtual environment to avoid package version conflicts.

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# macOS / Linux
source venv/bin/activate
# Windows
venv\Scripts\activate
```

### 4. Install Dependencies

This project provides two installation methods, please choose based on your execution environment:

#### 🖥️ CPU Execution Environment

If you want to use CPU execution on a regular computer:

```bash
pip install -r requirements.txt
```

#### ⚡ NPU Acceleration Environment (Snapdragon X Series)

If you're using a device with Snapdragon X Elite/Plus and want to use NPU acceleration:

```bash
pip install -r requirements-qnn.txt
```

#### Dependencies Explanation

**Basic Packages** (requirements.txt):
- `opencv-python`: For image processing and camera control
- `onnxruntime`: For running ONNX AI models (CPU version)
- `numpy`: High-performance numerical computation library
- `pyautogui`: For screen control (not used in current version, reserved for future features)
- `pillow`: Image processing library
- `scipy`: For scientific computing, optimizes face detection post-processing in this project

**NPU Acceleration Packages** (requirements-qnn.txt):
- Includes all basic packages above
- `onnxruntime-qnn`: ONNX Runtime version supporting Qualcomm NPU

---

## ⚙️ Running and Testing

### 1. Configuration and Launch (Recommended Method)

**It's recommended to use the configuration tool for parameter adjustment and direct program launch**, this is the most convenient way to use:

```bash
python setup.py
```

The configuration tool provides the following features:

- Adjust detection sensitivity, camera index, delay time and other parameters
- **Configure privacy protection applications**: Set applications to open for different operating systems
- Test whether the camera is working properly
- **Test privacy applications**: Verify that applications can open normally
- Save settings
- **Launch Watch Out directly from the tool after configuration**

In the configuration tool's main menu, select "5. Launch Watch Out" to automatically save settings and start the program.

### 2. Direct Main Program Launch (Advanced Usage)

If you have completed the configuration, you can also directly run the main program:

```bash
python main.py
```

> **How to exit the program**:
>
> - **In preview mode**: When the face preview window is open, press the `ESC` key to exit.
> - **In background mode**: Press `Ctrl+C` in the terminal to end the program.

### 3. Testing and Verification Methods

This project currently doesn't have automated test scripts, but you can verify functionality through the following manual methods:

1. **Camera Test**:
    - Run `python setup.py`.
    - Select the "Test Camera" option.
    - A window should pop up showing real-time video. Press `ESC` key to close.

2. **Face Detection Verification**:
    - Run `python main.py`.
    - Enable face preview function (can be set in `setup.py`).
    - After the program starts, you should see a preview window with rectangles drawn around detected faces.

3. **Privacy Application Test**:
    - Run `python setup.py`.
    - Select "2. Modify Settings" → "7. Privacy Protection Application Settings" → "4. Test Open Application".
    - The system will attempt to open your configured privacy protection application.

4. **Privacy Mode Verification**:
    - Keep the program running.
    - **Single person scenario**: Ensure only you are in the camera view, this should be "safe mode" with normal screen.
    - **Multiple people scenario**: Have another colleague or friend enter the camera view. After a brief delay, the program should switch to "privacy mode" and automatically open your configured privacy protection application.
    - **Temporary disable**: Press the `ESC` key, privacy mode should be temporarily disabled.

---

## 📱 Privacy Protection Application Configuration

Watch Out supports customizing applications to open in privacy mode. You can choose any application you prefer to provide privacy protection.

### Supported Configuration Methods

### Configuration Methods

#### 1. Configure via Configuration Tool (Recommended)

```bash
python setup.py
```

**Configuration Steps**:
1. Select "2. Modify Settings"
2. Select "6. Privacy Protection Application Settings"
3. Select the operating system to configure (macOS/Windows)
4. Enter application information as prompted:
   - Application name
   - Launch command
   - Backup path (optional)
5. Select "4. Test Open Application" to verify settings
6. Return to main menu and select "4. Save Settings"

#### 2. Configuration Examples

**macOS Configuration Examples**:
- Application names: `Google Chrome`, `Safari`, `Notes`
- Launch commands: `open -a 'Google Chrome'`, `open -a 'Safari'`
- Backup paths: `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`

**Windows Configuration Examples**:
- Application names: `Microsoft Edge`, `Notepad`, `Calculator`
- Launch commands: `msedge.exe`, `notepad.exe`, `calc.exe`
- Backup paths: (optional)

#### 3. Custom Application Paths

If you need to use specific application paths, you can set custom application paths in the configuration tool (option 7), entering the full executable path:

**Examples**:
- macOS: `/Applications/MyApp.app/Contents/MacOS/MyApp`
- Windows: `C:\Program Files\MyApp\MyApp.exe`

### Backup Mechanism

The system provides multi-layer backup mechanisms to ensure privacy protection reliability:

1. **Custom path priority**: If custom application path is set, it will be used first
2. **Primary application**: Use the primary application configured for the current operating system
3. **Backup path**: If the primary command fails, try using the backup path
4. **Backup application**: Finally try to open the system default backup application

### Common Application Configuration Examples

**Browser Category**:
- Chrome: `open -a 'Google Chrome'` (macOS) / `chrome.exe` (Windows)
- Safari: `open -a 'Safari'` (macOS)
- Edge: `msedge.exe` (Windows)

**System Tools Category**:
- Notepad: `notepad.exe` (Windows)
- Calculator: `open -a 'Calculator'` (macOS) / `calc.exe` (Windows)
- Text Editor: `open -a 'TextEdit'` (macOS)

---

## ⚖️ License

- **Project Source Code**: This project uses **MIT License**. For details, please refer to the [LICENSE](LICENSE) file.
- **AI Model**:
  - **Model Name**: Lightweight-Face-Detection (`w8a8` quantized version)
  - **Model Source**: Downloaded from [Qualcomm AI Hub](https://aihub.qualcomm.com/compute/models/face_det_lite).
  - **Model License**: This model uses **BSD 3-Clause "New" or "Revised" License**. Full license text can be found in the `model.onnx/LICENSE` file.
