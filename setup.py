#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CLI 設定工具 - Privacy Guard
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
            'overlay_alpha': OVERLAY_ALPHA,
            'detection_interval': DETECTION_INTERVAL,
            'enable_face_preview': ENABLE_FACE_PREVIEW,
            'enable_sound_alert': ENABLE_SOUND_ALERT,
            'enable_desktop_notification': ENABLE_DESKTOP_NOTIFICATION
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
        logger.info(f"4. 覆蓋層透明度: {self.config['overlay_alpha']}")
        logger.info(f"5. 偵測間隔: {self.config['detection_interval']} 秒")
        logger.info(f"6. 顯示臉部預覽: {'是' if self.config['enable_face_preview'] else '否'}")
        logger.info(f"7. 聲音提醒: {'是' if self.config['enable_sound_alert'] else '否'}")
        logger.info(f"8. 桌面通知: {'是' if self.config['enable_desktop_notification'] else '否'}")
        
    def modify_config(self):
        """修改配置"""
        while True:
            self.show_current_config()
            logger.info("\n選擇要修改的設定 (1-8)，或按 0 返回主選單:")
            
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
                    new_value = float(input("輸入覆蓋層透明度 (0.0-1.0): "))
                    if 0.0 <= new_value <= 1.0:
                        self.config['overlay_alpha'] = new_value
                    else:
                        logger.error("❌ 透明度必須在 0.0-1.0 之間")
                elif choice == 5:
                    new_value = float(input("輸入偵測間隔 (秒): "))
                    if new_value > 0:
                        self.config['detection_interval'] = new_value
                    else:
                        logger.error("❌ 間隔必須大於 0")
                elif choice == 6:
                    answer = input("顯示臉部預覽? (y/n): ").lower()
                    self.config['enable_face_preview'] = answer == 'y'
                elif choice == 7:
                    answer = input("啟用聲音提醒? (y/n): ").lower()
                    self.config['enable_sound_alert'] = answer == 'y'
                elif choice == 8:
                    answer = input("啟用桌面通知? (y/n): ").lower()
                    self.config['enable_desktop_notification'] = answer == 'y'
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
                    
                cv2.imshow("Camera Test", frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                    
            cap.release()
            cv2.destroyAllWindows()
            
        except ImportError:
            logger.error("❌ 未安裝 OpenCV")
        except Exception as e:
            logger.error(f"❌ 測試失敗: {e}")
            
    def main_menu(self):
        """主選單"""
        while True:
            logger.info("\n🛡️  Privacy Guard 設定工具")
            logger.info("=" * 50)
            logger.info("1. 查看當前設定")
            logger.info("2. 修改設定")
            logger.info("3. 測試攝影機")
            logger.info("4. 儲存設定")
            logger.info("5. 啟動 Privacy Guard")
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
                    logger.info("\n🚀 啟動 Privacy Guard...")
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
