#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置檔案 - Privacy Guard 設定
"""

# 臉部偵測設定
DETECTION_THRESHOLD = 0.7  # 臉部偵測信心度閾值 (0.0-1.0)
PRIVACY_DELAY = 2.0        # 偵測到多人後延遲啟動隱私模式的時間 (秒)
TEMPORARY_DISABLE_TIME = 10 # 按 ESC 後暫時關閉隱私模式的時間 (秒)

# 攝影機設定
CAMERA_INDEX = 0           # 攝影機索引 (通常 0 是預設攝影機)
CAMERA_WIDTH = 640         # 攝影機解析度寬度
CAMERA_HEIGHT = 480        # 攝影機解析度高度
CAMERA_FPS = 30           # 攝影機 FPS

# 隱私模式設定
OVERLAY_ALPHA = 0.8       # 覆蓋層透明度 (0.0-1.0)
OVERLAY_COLOR = 'black'   # 覆蓋層顏色
WARNING_TEXT_SIZE = 24    # 警告文字大小

# 系統設定
DETECTION_INTERVAL = 0.1  # 偵測間隔 (秒)
LOG_LEVEL = 'INFO'        # 日誌等級 (DEBUG, INFO, WARNING, ERROR)

# 進階設定
ENABLE_FACE_PREVIEW = True   # 是否顯示臉部偵測預覽視窗 (除錯用)
SAVE_DETECTION_LOG = True    # 是否儲存偵測記錄
MAX_LOG_SIZE_MB = 10        # 最大日誌檔案大小 (MB)

# 快捷鍵設定
HOTKEY_TEMPORARY_DISABLE = 'Escape'  # 暫時關閉隱私模式的快捷鍵
HOTKEY_FORCE_PRIVACY = 'F9'          # 強制啟動隱私模式的快捷鍵
HOTKEY_EXIT = 'ctrl+c'               # 結束程式的快捷鍵

# 模型設定
MODEL_PATH = "model.onnx/model.onnx"  # ONNX 模型路徑

# 通知設定
ENABLE_SOUND_ALERT = False    # 是否啟用聲音提醒
ENABLE_DESKTOP_NOTIFICATION = True  # 是否啟用桌面通知
