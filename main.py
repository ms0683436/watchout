#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dynamic Focus Assistant - Watch Out
Automatically blurs the screen when multiple people are detected to protect sensitive content
Uses Qualcomm AI Hub face detection model
"""

import cv2
import numpy as np
import onnxruntime as ort
import pyautogui
import time
import threading
import sys
import json
import os
from PIL import Image, ImageFilter
import logging
from config import *
import subprocess
import tempfile

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PrivacyGuard:
    def __init__(self):
        self.session = None
        self.input_name = None
        self.in_w = None
        self.in_h = None
        self.cap = None
        self.is_running = False
        self.privacy_mode = False
        self.last_detection_time = 0
        self.app_process = None  # 用來追蹤應用程式進程
        
        # Load configuration
        self.load_user_config()
        
        # Configure pyautogui
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.1
        
    def load_user_config(self):
        """Loads user configuration"""
        config_file = "privacy_guard_config.json"
        
        # Default configuration
        self.detection_threshold = DETECTION_THRESHOLD
        self.privacy_delay = PRIVACY_DELAY
        self.camera_index = CAMERA_INDEX
        self.detection_interval = DETECTION_INTERVAL
        self.enable_face_preview = ENABLE_FACE_PREVIEW
        
        # 隱私保護應用程式設定
        self.privacy_apps = PRIVACY_APPS
        self.privacy_app_fallback = PRIVACY_APP_FALLBACK
        self.privacy_app_custom_path = PRIVACY_APP_CUSTOM_PATH
        
        # Load user custom configuration
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                    
                self.detection_threshold = user_config.get('detection_threshold', self.detection_threshold)
                self.privacy_delay = user_config.get('privacy_delay', self.privacy_delay)
                self.camera_index = user_config.get('camera_index', self.camera_index)
                self.detection_interval = user_config.get('detection_interval', self.detection_interval)
                self.enable_face_preview = user_config.get('enable_face_preview', self.enable_face_preview)
                
                # 載入隱私應用程式自訂配置
                if 'privacy_apps' in user_config:
                    self.privacy_apps.update(user_config['privacy_apps'])
                if 'privacy_app_fallback' in user_config:
                    self.privacy_app_fallback.update(user_config['privacy_app_fallback'])
                if 'privacy_app_custom_path' in user_config:
                    self.privacy_app_custom_path = user_config['privacy_app_custom_path']
                
                logger.info("User configuration loaded")
            except Exception as e:
                logger.warning(f"Failed to load user configuration, using default settings: {e}")
        
        logger.info("Configuration loaded from config.py")
        
    def load_model(self):
        """Loads the ONNX face detection model"""
        try:
            logger.info("Loading face detection model...")
            
            # Define execution providers, prioritizing QNN (NPU) over CPU
            providers = ['QNNExecutionProvider', 'CPUExecutionProvider']
            
            self.session = ort.InferenceSession(MODEL_PATH, providers=providers)
            
            # Log the actual provider being used
            logger.info(f"ONNX Runtime is using provider: {self.session.get_providers()}")
            self.input_name = self.session.get_inputs()[0].name
            self.in_w = self.session.get_inputs()[0].shape[3]
            self.in_h = self.session.get_inputs()[0].shape[2]
            logger.info(f"Model loaded successfully! Input size: {self.in_w}x{self.in_h}")
            return True
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            return False
            
    def initialize_camera(self):
        """Initializes the camera"""
        try:
            self.cap = cv2.VideoCapture(self.camera_index)
            if not self.cap.isOpened():
                logger.error("Unable to open camera!")
                return False
            
            # Set camera parameters
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)
            self.cap.set(cv2.CAP_PROP_FPS, CAMERA_FPS)
            
            # If preview is enabled, initialize window
            if self.enable_face_preview:
                logger.debug("Attempting to initialize preview window...")
                try:
                    window_name = 'Watch Out - Face Detection Preview'
                    cv2.namedWindow(window_name, cv2.WINDOW_AUTOSIZE)
                    logger.info("Preview window initialized")
                    logger.debug("Preview window initialized successfully.")
                except Exception as e:
                    logger.warning(f"Preview window initialization failed: {e}")
                    self.enable_face_preview = False
            
            logger.info(f"Camera {self.camera_index} initialized successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize camera: {e}")
            return False
            
    def detect_faces(self, frame):
        """Detects faces and returns the number of faces"""
        try:
            h, w, _ = frame.shape
            
            # Preprocess image
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            img = cv2.resize(img, (self.in_w, self.in_h))
            img = np.expand_dims(img, axis=0)
            img = np.expand_dims(img, axis=0)
            img = img.astype(np.uint8)
            
            # Run inference
            outputs = self.session.run(None, {self.input_name: img})
            
            # Parse output
            # outputs[0] = heatmap (1, 1, 60, 80)
            # outputs[1] = bbox (1, 4, 60, 80) 
            # outputs[2] = landmark (1, 10, 60, 80)
            
            heatmap = outputs[0][0, 0]  # (60, 80)
            bbox_maps = outputs[1][0]   # (4, 60, 80)
            
            # Find faces from heatmap
            # Convert uint8 to float and normalize
            heatmap_norm = heatmap.astype(np.float32) / 255.0
            
            # Use threshold to find possible face locations
            threshold = self.detection_threshold
            
            # Use morphological operations to find connected regions
            heatmap_binary = (heatmap_norm > threshold).astype(np.uint8)
            
            # Find connected components
            from scipy import ndimage
            labeled_array, num_features = ndimage.label(heatmap_binary)
            
            detected_faces = []
            face_count = 0
            
            # Process each connected component
            for i in range(1, num_features + 1):
                # Find the location of the component
                component_mask = (labeled_array == i)
                if np.sum(component_mask) < 5:  # Ignore too small regions
                    continue
                    
                # Find bounding box
                rows, cols = np.where(component_mask)
                if len(rows) == 0:
                    continue
                    
                min_row, max_row = rows.min(), rows.max()
                min_col, max_col = cols.min(), cols.max()
                
                # Convert to original image coordinates
                x1 = int(min_col * w / heatmap.shape[1])
                y1 = int(min_row * h / heatmap.shape[0])
                x2 = int((max_col + 1) * w / heatmap.shape[1])
                y2 = int((max_row + 1) * h / heatmap.shape[0])
                
                # Ensure bounding box is within image bounds
                x1 = max(0, min(x1, w-1))
                y1 = max(0, min(y1, h-1))
                x2 = max(x1+1, min(x2, w))
                y2 = max(y1+1, min(y2, h))
                
                # Calculate average confidence for the region
                region_confidence = np.mean(heatmap_norm[min_row:max_row+1, min_col:max_col+1])
                
                detected_faces.append({
                    'bbox': (x1, y1, x2, y2),
                    'confidence': region_confidence
                })
                face_count += 1
                        
            return face_count, detected_faces
            
        except ImportError:
            # If scipy is not available, use a simplified version
            logger.warning("scipy not installed, using simplified face detection")
            return self._detect_faces_simple(frame)
        except Exception as e:
            logger.error(f"Face detection failed: {e}")
            return 0, []
    
    def _detect_faces_simple(self, frame):
        """Simplified face detection (no scipy required)"""
        try:
            h, w, _ = frame.shape
            
            # Preprocess image
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            img = cv2.resize(img, (self.in_w, self.in_h))
            img = np.expand_dims(img, axis=0)
            img = np.expand_dims(img, axis=0)
            img = img.astype(np.uint8)
            
            # Run inference
            outputs = self.session.run(None, {self.input_name: img})
            heatmap = outputs[0][0, 0]  # (60, 80)
            
            # Convert uint8 to float and normalize
            heatmap_norm = heatmap.astype(np.float32) / 255.0
            
            # Use threshold to find possible face locations
            threshold = self.detection_threshold
            
            # Simple grid search
            grid_size = 8  # Size of each grid
            face_count = 0
            detected_faces = []
            
            for i in range(0, heatmap.shape[0], grid_size):
                for j in range(0, heatmap.shape[1], grid_size):
                    grid = heatmap_norm[i:i+grid_size, j:j+grid_size]
                    max_confidence = grid.max()
                    
                    if max_confidence > threshold:
                        face_count += 1
                        # Calculate position in original image
                        x1 = int(j * w / heatmap.shape[1])
                        y1 = int(i * h / heatmap.shape[0])
                        x2 = int((j + grid_size) * w / heatmap.shape[1])
                        y2 = int((i + grid_size) * h / heatmap.shape[0])
                        
                        detected_faces.append({
                            'bbox': (x1, y1, x2, y2),
                            'confidence': max_confidence
                        })
                        
            return face_count, detected_faces
            
        except Exception as e:
            logger.error(f"Simplified face detection failed: {e}")
            return 0, []
            
    def open_custom_app(self):
        """開啟隱私保護應用程式"""
        try:
            # 獲取當前操作系統
            current_os = sys.platform
            
            # 如果有自訂路徑，優先使用
            if self.privacy_app_custom_path and os.path.exists(self.privacy_app_custom_path):
                try:
                    self.app_process = subprocess.Popen([self.privacy_app_custom_path])
                    logger.info(f"隱私保護應用程式已透過自訂路徑成功開啟: {self.privacy_app_custom_path}")
                    return True
                except Exception as e:
                    logger.warning(f"自訂路徑開啟失敗: {e}")
            
            # 檢查是否支援當前操作系統
            if current_os not in self.privacy_apps:
                logger.error(f"不支援的作業系統: {current_os}")
                return False
            
            # 獲取當前系統的應用程式配置
            app_config = self.privacy_apps[current_os]
            app_name = app_config["name"]
            app_command = app_config["command"]
            fallback_path = app_config.get("fallback_path", "")
            
            logger.info(f"正在開啟隱私保護應用程式: {app_name}")
            
            # 嘗試執行主要命令
            try:
                if current_os == "darwin":  # macOS
                    if app_command.startswith("open -a"):
                        # 提取應用程式名稱
                        app_name_from_cmd = app_command.split("'")[1] if "'" in app_command else app_name
                        result = subprocess.run([
                            "open", "-a", app_name_from_cmd
                        ], capture_output=True, text=True, timeout=10)
                        
                        if result.returncode == 0:
                            logger.info(f"{app_name} 已成功開啟")
                            return True
                        else:
                            logger.warning(f"Open 命令執行失敗: {result.stderr}")
                    else:
                        # 直接執行命令
                        cmd_parts = app_command.split()
                        result = subprocess.run(cmd_parts, capture_output=True, text=True, timeout=10)
                        if result.returncode == 0:
                            logger.info(f"{app_name} 已成功開啟")
                            return True
                    
                    # 如果命令失敗，嘗試備用路徑
                    if fallback_path and os.path.exists(fallback_path):
                        self.app_process = subprocess.Popen([fallback_path])
                        logger.info(f"{app_name} 已透過備用路徑成功開啟")
                        return True
                        
                elif current_os == "win32":  # Windows
                    cmd_parts = app_command.split()
                    self.app_process = subprocess.Popen(cmd_parts)
                    logger.info(f"{app_name} 在 Windows 上成功開啟")
                    return True
                    
            except subprocess.TimeoutExpired:
                logger.warning(f"{app_name} 開啟命令逾時")
            except Exception as e:
                logger.warning(f"開啟 {app_name} 失敗: {e}")
            
            # 如果主要應用程式失敗，嘗試備用應用程式
            if current_os in self.privacy_app_fallback:
                fallback_config = self.privacy_app_fallback[current_os]
                fallback_name = fallback_config["name"]
                fallback_command = fallback_config["command"]
                
                logger.info(f"嘗試開啟備用應用程式: {fallback_name}")
                
                try:
                    if current_os == "darwin":
                        if fallback_command.startswith("open -a"):
                            app_name_from_cmd = fallback_command.split("'")[1] if "'" in fallback_command else fallback_name
                            result = subprocess.run([
                                "open", "-a", app_name_from_cmd
                            ], capture_output=True, text=True, timeout=10)
                            
                            if result.returncode == 0:
                                logger.info(f"備用應用程式 {fallback_name} 已成功開啟")
                                return True
                    elif current_os == "win32":
                        cmd_parts = fallback_command.split()
                        self.app_process = subprocess.Popen(cmd_parts)
                        logger.info(f"備用應用程式 {fallback_name} 已成功開啟")
                        return True
                        
                except Exception as e:
                    logger.warning(f"開啟備用應用程式失敗: {e}")
            
            logger.error("無法開啟任何隱私保護應用程式，請檢查配置")
            return False
            
        except Exception as e:
            logger.error(f"開啟隱私保護應用程式失敗: {e}")
            return False
    
    def close_privacy_app(self):
        """關閉隱私保護應用程式"""
        try:
            # 注意：我們不會強制關閉應用程式，因為用戶可能正在使用它
            if self.app_process:
                current_os = sys.platform
                app_name = self.privacy_apps.get(current_os, {}).get("name", "隱私保護應用程式")
                logger.info(f"{app_name} 已為隱私保護而開啟。如需要可手動關閉。")
                self.app_process = None
            
            logger.info("隱私保護應用程式模式已停用")
            return True
            
        except Exception as e:
            logger.error(f"關閉隱私保護應用程式失敗: {e}")
            return False
            
    def create_privacy_overlay(self):
        """Creates a privacy protection by opening an application"""
        try:
            self.privacy_mode = True
            # Display a clear privacy mode message in the terminal
            logger.info("\n" + "="*60)
            logger.info("🔒 Watch Out Mode Activated!")
            logger.info("Someone else detected. Opening an application for privacy protection...")
            logger.info("Press Ctrl+C to exit")
            logger.info("="*60)
            logger.info("Watch Out Mode activated")
            
            # 開啟指定的隱私保護應用程式
            app_success = self.open_custom_app()
            if app_success:
                current_os = sys.platform
                app_name = self.privacy_apps.get(current_os, {}).get("name", "隱私保護應用程式")
                logger.info(f"{app_name} 隱私保護已成功啟動")
            else:
                logger.warning("隱私保護應用程式啟動失敗，繼續使用標準模式")
            
        except Exception as e:
            logger.error(f"Failed to activate Watch Out Mode: {e}")
            
    def remove_privacy_overlay(self):
        """Removes the privacy mode"""
        try:
            if self.privacy_mode:
                self.privacy_mode = False
                logger.info("\n" + "="*60)
                logger.info("✅ Watch Out Mode Deactivated")
                logger.info("Environment secure. You can continue your work.")
                logger.info("="*60)
                logger.info("Watch Out Mode deactivated")
                
                # 關閉隱私保護應用程式
                self.close_privacy_app()
                
        except Exception as e:
            logger.error(f"Failed to deactivate Watch Out Mode: {e}")
            
    def update_privacy_status(self, face_count):
        """Updates the privacy status based on the number of detected faces"""
        current_time = time.time()
        
        if face_count > 1:  # Multiple people detected
            if not self.privacy_mode:
                if self.last_detection_time == 0:
                    self.last_detection_time = current_time
                elif current_time - self.last_detection_time >= self.privacy_delay:
                    # Activate privacy mode
                    self.create_privacy_overlay()
                    logger.info(f"Activating Watch Out Mode - {face_count} people detected")
        else:  # One person or no one
            self.last_detection_time = 0
            if self.privacy_mode:
                # Deactivate privacy mode
                self.remove_privacy_overlay()
                logger.info("Deactivating Watch Out Mode - Environment secure")
                
    def run_detection_loop(self):
        """Main detection loop"""
        logger.info("Starting face detection...")
        
        while self.is_running:
            try:
                ret, frame = self.cap.read()
                if not ret:
                    logger.warning("Unable to read frame from camera")
                    continue
                    
                # Detect faces
                face_count, faces = self.detect_faces(frame)
                
                # If preview is enabled, display face boxes
                if self.enable_face_preview:
                    display_frame = frame.copy()
                    
                    # Draw face boxes
                    for face in faces:
                        if isinstance(face, dict):
                            x1, y1, x2, y2 = face['bbox']
                            confidence = face['confidence']
                            
                            # Choose color based on confidence
                            if confidence > 0.8:
                                color = (0, 255, 0)  # Green - high confidence
                            elif confidence > 0.6:
                                color = (0, 255, 255)  # Yellow - medium confidence
                            else:
                                color = (255, 0, 0)  # Blue - low confidence
                            
                            # Draw rectangle
                            cv2.rectangle(display_frame, (x1, y1), (x2, y2), color, 2)
                            
                            # Display confidence
                            cv2.putText(display_frame, f'{confidence:.2f}', 
                                      (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 
                                      0.6, color, 2)
                        else:
                            # Compatibility with old format
                            x1, y1, x2, y2 = face
                            cv2.rectangle(display_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    
                    # Display status information
                    if self.privacy_mode:
                        status_text = "Privacy Mode"
                        status_color = (0, 0, 255)  # Red
                    else:
                        status_text = "Secure"
                        status_color = (0, 255, 0)  # Green
                    
                    # Display status on frame
                    cv2.putText(display_frame, f'Detected {face_count} people | {status_text}', 
                              (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, status_color, 2)
                    
                    # Add exit hint
                    (text_width, text_height), _ = cv2.getTextSize("Press ESC to exit", cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
                    cv2.putText(display_frame, "Press ESC to exit", 
                              (display_frame.shape[1] - text_width - 10, 30), 
                              cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                    
                    # Force display of preview window (improved)
                    window_name = 'Watch Out - Face Detection Preview'
                    logger.debug(f"Attempting to show frame in window {window_name}...")
                    try:
                        cv2.imshow(window_name, display_frame)
                        logger.debug("imshow call successful.")
                        
                        # Handle keyboard input
                        key = cv2.waitKey(1) & 0xFF

                        # On ESC key press, exit the program
                        if key == 27:
                            logger.info("ESC key pressed, exiting...")
                            self.is_running = False
                            break

                    except Exception as e:
                        logger.warning(f"Error displaying preview window: {e}")
                        self.enable_face_preview = False
                        cv2.destroyAllWindows()
                
                # Update privacy status
                self.update_privacy_status(face_count)
                
                # Display status in terminal
                if self.privacy_mode:
                    status = "🔒 Privacy Mode"
                else:
                    status = "✅ Secure"
                
                preview_info = " | Preview: On" if self.enable_face_preview else ""
                logger.info(f"Detected {face_count} people | Status: {status}{preview_info} | Press Ctrl+C to exit")
                
                # Short delay to prevent CPU overload
                time.sleep(self.detection_interval)
                
            except KeyboardInterrupt:
                logger.info("Received interrupt signal, preparing to exit...")
                self.is_running = False
                break
            except Exception as e:
                logger.error(f"Error in detection loop: {e}")
                time.sleep(1)
                
    def start(self):
        """Starts the Watch Out"""
        logger.info("Starting Dynamic Focus Assistant...")

        if not self.load_model():
            return False

        if not self.initialize_camera():
            return False

        self.is_running = True

        # If preview is enabled, run directly in the main thread to handle GUI
        if self.enable_face_preview:
            logger.info("Preview mode enabled, running in main thread.")
            try:
                # In this mode, keyboard input is handled by cv2.waitKey()
                self.run_detection_loop()
            except KeyboardInterrupt:
                logger.info("Exiting program...")
            finally:
                self.stop()
            return True

        # If preview is not enabled, run in a background thread
        try:
            # Run detection in the background
            detection_thread = threading.Thread(target=self.run_detection_loop, daemon=True)
            detection_thread.start()

            logger.info("Watch Out started!")
            logger.info("- Privacy mode will be activated automatically when multiple people are detected")
            logger.info("- Press Ctrl+C to exit")

            # Wait in the main thread
            while detection_thread.is_alive():
                detection_thread.join(0.1)

        except KeyboardInterrupt:
            logger.info("Exiting program...")
            self.is_running = False
        finally:
            self.stop()

        return True
        
    def stop(self):
        """Stops the Watch Out"""
        self.is_running = False
        
        if self.cap:
            self.cap.release()
            
        self.remove_privacy_overlay()
        
        # 確保關閉隱私保護應用程式
        self.close_privacy_app()
        
        cv2.destroyAllWindows()
        
        # Ensure all OpenCV windows are closed
        for i in range(5):
            cv2.waitKey(1)
            
        logger.info("Watch Out stopped")

def main():
    """Main function"""
    logger.info("🛡️  Dynamic Focus Assistant - Watch Out")
    logger.info("=" * 50)
    
    guard = PrivacyGuard()
    
    if not guard.start():
        logger.error("Startup failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
