#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CLI 設定工具 - Watch Out
簡單的命令列介面來調整設定
"""

import json
import os
import sys
from config import *
import logging

# 設置日誌
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ConfigManager:
    def __init__(self):
        self.config_file = "privacy_guard_config.json"
        self.config = self.load_config()
        
    def load_config(self):
        """載入配置檔案"""
        default_config = {
            'detection_threshold': DETECTION_THRESHOLD,
            'privacy_delay': PRIVACY_DELAY,
            'camera_index': CAMERA_INDEX,
            'detection_interval': DETECTION_INTERVAL,
            'enable_face_preview': ENABLE_FACE_PREVIEW,
            
            # 隱私保護應用程式配置
            'privacy_apps': PRIVACY_APPS,
            'privacy_app_fallback': PRIVACY_APP_FALLBACK,
            'privacy_app_custom_path': PRIVACY_APP_CUSTOM_PATH,
        }
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    saved_config = json.load(f)
                    default_config.update(saved_config)
            except Exception as e:
                logger.error(f"載入配置檔案失敗: {e}")
                
        return default_config
        
    def save_config(self):
        """儲存配置檔案"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            logger.info("✅ 配置已儲存")
        except Exception as e:
            logger.error(f"❌ 儲存配置失敗: {e}")
            
    def show_current_config(self):
        """顯示當前配置"""
        logger.info("\n🔧 當前設定")
        logger.info("=" * 50)
        logger.info(f"1. 臉部偵測閾值: {self.config['detection_threshold']}")
        logger.info(f"2. 隱私模式延遲: {self.config['privacy_delay']} 秒")
        logger.info(f"3. 攝影機索引: {self.config['camera_index']}")
        logger.info(f"4. 偵測間隔: {self.config['detection_interval']} 秒")
        logger.info(f"5. 顯示臉部預覽: {'是' if self.config['enable_face_preview'] else '否'}")
        logger.info(f"6. 隱私保護應用程式設定")
        logger.info(f"7. 自訂應用程式路徑: {self.config.get('privacy_app_custom_path', '未設定')}")
        
    def show_privacy_apps_config(self):
        """顯示隱私保護應用程式配置"""
        logger.info("\n📱 隱私保護應用程式設定")
        logger.info("=" * 50)
        
        privacy_apps = self.config.get('privacy_apps', {})
        for os_name, app_config in privacy_apps.items():
            os_display = {"darwin": "macOS", "win32": "Windows"}.get(os_name, os_name)
            logger.info(f"\n{os_display}:")
            logger.info(f"  應用程式名稱: {app_config.get('name', '未設定')}")
            logger.info(f"  開啟命令: {app_config.get('command', '未設定')}")
            logger.info(f"  備用路徑: {app_config.get('fallback_path', '未設定')}")
        
        fallback_apps = self.config.get('privacy_app_fallback', {})
        if fallback_apps:
            logger.info("\n備用應用程式:")
            for os_name, app_config in fallback_apps.items():
                os_display = {"darwin": "macOS", "win32": "Windows"}.get(os_name, os_name)
                logger.info(f"  {os_display}: {app_config.get('name', '未設定')}")
    
    def modify_privacy_apps(self):
        """修改隱私保護應用程式設定"""
        while True:
            self.show_privacy_apps_config()
            logger.info("\n選擇操作:")
            logger.info("1. 修改 macOS 應用程式")
            logger.info("2. 修改 Windows 應用程式")
            logger.info("3. 設定自訂應用程式路徑")
            logger.info("4. 測試開啟應用程式")
            logger.info("0. 返回上級選單")
            
            try:
                choice = int(input("請輸入選項: "))
                
                if choice == 0:
                    break
                elif choice == 1:
                    self.modify_os_app("darwin", "macOS")
                elif choice == 2:
                    self.modify_os_app("win32", "Windows")
                elif choice == 3:
                    new_path = input("輸入自訂應用程式完整路徑 (留空清除): ").strip()
                    self.config['privacy_app_custom_path'] = new_path
                    logger.info("✅ 自訂路徑已更新")
                elif choice == 4:
                    self.test_privacy_app()
                else:
                    logger.error("❌ 無效選項")
                    
            except ValueError:
                logger.error("❌ 請輸入有效數字")
            except KeyboardInterrupt:
                logger.info("\n操作取消")
                break
    
    def modify_os_app(self, os_key, os_name):
        """修改特定作業系統的應用程式設定"""
        logger.info(f"\n修改 {os_name} 應用程式設定")
        
        privacy_apps = self.config.get('privacy_apps', {})
        if os_key not in privacy_apps:
            privacy_apps[os_key] = {}
        
        current_app = privacy_apps[os_key]
        
        logger.info(f"當前設定:")
        logger.info(f"  應用程式名稱: {current_app.get('name', '未設定')}")
        logger.info(f"  開啟命令: {current_app.get('command', '未設定')}")
        logger.info(f"  備用路徑: {current_app.get('fallback_path', '未設定')}")
        
        # 修改應用程式名稱
        new_name = input(f"輸入新的應用程式名稱 (當前: {current_app.get('name', '未設定')}): ").strip()
        if new_name:
            current_app['name'] = new_name
        
        # 修改開啟命令
        if os_key == "darwin":
            logger.info("macOS 命令範例: open -a 'Google Chrome'")
        elif os_key == "win32":
            logger.info("Windows 命令範例: msedge.exe, notepad.exe")
            
        new_command = input(f"輸入新的開啟命令 (當前: {current_app.get('command', '未設定')}): ").strip()
        if new_command:
            current_app['command'] = new_command
        
        # 修改備用路徑
        new_fallback = input(f"輸入備用路徑 (當前: {current_app.get('fallback_path', '未設定')}): ").strip()
        if new_fallback:
            current_app['fallback_path'] = new_fallback
        
        privacy_apps[os_key] = current_app
        self.config['privacy_apps'] = privacy_apps
        logger.info(f"✅ {os_name} 應用程式設定已更新")
    
    def test_privacy_app(self):
        """測試開啟隱私保護應用程式"""
        logger.info("\n🧪 測試隱私保護應用程式...")
        
        try:
            # 臨時匯入必要的模組來測試
            import subprocess
            import sys
            
            current_os = sys.platform
            privacy_apps = self.config.get('privacy_apps', {})
            custom_path = self.config.get('privacy_app_custom_path', '')
            
            # 如果有自訂路徑，優先測試
            if custom_path and os.path.exists(custom_path):
                try:
                    subprocess.Popen([custom_path])
                    logger.info("✅ 自訂路徑應用程式開啟成功")
                    return
                except Exception as e:
                    logger.error(f"❌ 自訂路徑開啟失敗: {e}")
            
            # 測試當前系統的應用程式
            if current_os not in privacy_apps:
                logger.error(f"❌ 未設定 {current_os} 的應用程式配置")
                return
            
            app_config = privacy_apps[current_os]
            app_name = app_config.get('name', '未知應用程式')
            app_command = app_config.get('command', '')
            
            if not app_command:
                logger.error("❌ 未設定開啟命令")
                return
            
            logger.info(f"正在測試開啟: {app_name}")
            
            if current_os == "darwin":  # macOS
                if app_command.startswith("open -a"):
                    app_name_from_cmd = app_command.split("'")[1] if "'" in app_command else app_name
                    result = subprocess.run([
                        "open", "-a", app_name_from_cmd
                    ], capture_output=True, text=True, timeout=10)
                    
                    if result.returncode == 0:
                        logger.info(f"✅ {app_name} 開啟成功")
                    else:
                        logger.error(f"❌ 開啟失敗: {result.stderr}")
                else:
                    cmd_parts = app_command.split()
                    subprocess.run(cmd_parts, capture_output=True, text=True, timeout=10)
                    logger.info(f"✅ {app_name} 開啟成功")
                    
            elif current_os == "win32":  # Windows
                cmd_parts = app_command.split()
                subprocess.Popen(cmd_parts)
                logger.info(f"✅ {app_name} 開啟成功")
            else:
                logger.error(f"❌ 不支援的作業系統: {current_os}")
                
        except subprocess.TimeoutExpired:
            logger.error("❌ 開啟命令逾時")
        except Exception as e:
            logger.error(f"❌ 測試失敗: {e}")
        
    def modify_config(self):
        """修改配置"""
        while True:
            self.show_current_config()
            logger.info("\n選擇要修改的設定 (1-7)，或按 0 返回主選單:")
            
            try:
                choice = int(input("請輸入選項: "))
                
                if choice == 0:
                    break
                elif choice == 1:
                    new_value = float(input("輸入新的臉部偵測閾值 (0.0-1.0): "))
                    if 0.0 <= new_value <= 1.0:
                        self.config['detection_threshold'] = new_value
                    else:
                        logger.error("❌ 數值必須在 0.0-1.0 之間")
                elif choice == 2:
                    new_value = float(input("輸入隱私模式延遲時間 (秒): "))
                    if new_value >= 0:
                        self.config['privacy_delay'] = new_value
                    else:
                        logger.error("❌ 時間必須大於等於 0")
                elif choice == 3:
                    new_value = int(input("輸入攝影機索引 (通常是 0): "))
                    if new_value >= 0:
                        self.config['camera_index'] = new_value
                    else:
                        logger.error("❌ 索引必須大於等於 0")
                elif choice == 4:
                    new_value = float(input("輸入偵測間隔 (秒): "))
                    if new_value > 0:
                        self.config['detection_interval'] = new_value
                    else:
                        logger.error("❌ 間隔必須大於 0")
                elif choice == 5:
                    answer = input("顯示臉部預覽? (y/n): ").lower()
                    self.config['enable_face_preview'] = answer == 'y'
                elif choice == 6:
                    self.modify_privacy_apps()
                elif choice == 7:
                    new_path = input("輸入自訂應用程式完整路徑 (留空清除): ").strip()
                    self.config['privacy_app_custom_path'] = new_path
                    logger.info("✅ 自訂路徑已更新")
                else:
                    logger.error("❌ 無效選項")
                    
            except ValueError:
                logger.error("❌ 請輸入有效數字")
            except KeyboardInterrupt:
                logger.info("\n操作取消")
                break
                
    def test_camera(self):
        """測試攝影機"""
        logger.info(f"\n📷 測試攝影機 {self.config['camera_index']}...")
        
        try:
            import cv2
            cap = cv2.VideoCapture(self.config['camera_index'])
            
            if not cap.isOpened():
                logger.error("❌ 無法開啟攝影機")
                return
                
            logger.info("✅ 攝影機正常")
            logger.info("正在顯示攝影機畫面，按 'q' 結束...")
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                cv2.putText(frame, "Press ESC to exit", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                cv2.imshow("Camera Test", frame)
                if cv2.waitKey(1) & 0xFF == 27:  # 27 is the ESC key
                    break
                    
            cap.release()
            cv2.destroyWindow("Camera Test")
            # Add a small wait to ensure the window closes properly
            for _ in range(4):
                cv2.waitKey(1)
            
        except ImportError:
            logger.error("❌ 未安裝 OpenCV")
        except Exception as e:
            logger.error(f"❌ 測試失敗: {e}")
            
    def main_menu(self):
        """主選單"""
        while True:
            logger.info("\n🛡️  Watch Out 設定工具")
            logger.info("=" * 50)
            logger.info("1. 查看當前設定")
            logger.info("2. 修改設定")
            logger.info("3. 測試攝影機")
            logger.info("4. 儲存設定")
            logger.info("5. 啟動 Watch Out")
            logger.info("0. 結束")
            
            try:
                choice = int(input("\n請選擇選項: "))
                
                if choice == 0:
                    logger.info("👋 再見！")
                    break
                elif choice == 1:
                    self.show_current_config()
                elif choice == 2:
                    self.modify_config()
                elif choice == 3:
                    self.test_camera()
                elif choice == 4:
                    self.save_config()
                elif choice == 5:
                    logger.info("\n🚀 啟動 Watch Out...")
                    self.save_config()
                    os.system("python main.py")
                else:
                    logger.error("❌ 無效選項")
                    
            except ValueError:
                logger.error("❌ 請輸入有效數字")
            except KeyboardInterrupt:
                logger.info("\n\n👋 再見！")
                break

def main():
    """主函數"""
    config_manager = ConfigManager()
    config_manager.main_menu()

if __name__ == "__main__":
    main()
