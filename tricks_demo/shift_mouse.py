import pyautogui
import random
import time
import threading
import tkinter as tk
from tkinter import ttk, messagebox
import sys

class MouseMover:
    def __init__(self):
        self.running = False
        self.thread = None
        self.screen_width, self.screen_height = pyautogui.size()
        
    def random_mouse_mover(self, duration=30, speed=0.5, boundary=50):
        """
        随机移动鼠标
        
        Args:
            duration: 运行时间（秒），0表示无限
            speed: 移动速度（秒）
            boundary: 距离屏幕边界的像素距离
        """
        print("🐭 鼠标开始随机移动！")
        print(f"📏 屏幕尺寸: {self.screen_width}x{self.screen_height}")
        print("⏹️  按Ctrl+C或关闭窗口停止")
        
        start_time = time.time()
        move_count = 0
        
        try:
            while self.running:
                # 确保鼠标不会移出屏幕
                x = random.randint(boundary, self.screen_width - boundary)
                y = random.randint(boundary, self.screen_height - boundary)
                
                # 获取当前鼠标位置
                current_x, current_y = pyautogui.position()
                
                # 计算移动距离
                distance = ((x - current_x)**2 + (y - current_y)**2)**0.5
                
                # 移动鼠标
                pyautogui.moveTo(x, y, duration=speed)
                move_count += 1
                
                # 随机点击（可选）
                if random.random() < 0.1:  # 10%的概率点击
                    pyautogui.click()
                    print("🖱️  随机点击")
                
                # 显示移动信息
                if move_count % 5 == 0:
                    print(f"📍 第{move_count}次移动: ({current_x}, {current_y}) -> ({x}, {y})")
                    print(f"📐 移动距离: {distance:.1f}像素")
                
                # 检查是否超时
                if duration > 0 and (time.time() - start_time) >= duration:
                    print("⏰ 时间到，自动停止")
                    self.stop()
                    break
                
                # 随机等待时间
                wait_time = random.uniform(1.0, 3.0)
                time.sleep(wait_time)
                
        except KeyboardInterrupt:
            print("\n🛑 用户手动停止")
            self.stop()
        except Exception as e:
            print(f"❌ 发生错误: {e}")
            self.stop()
    
    def start(self, duration=0, speed=0.5):
        """开始移动鼠标"""
        if not self.running:
            self.running = True
            self.thread = threading.Thread(
                target=self.random_mouse_mover, 
                args=(duration, speed)
            )
            self.thread.daemon = True
            self.thread.start()
            return True
        return False
    
    def stop(self):
        """停止移动鼠标"""
        self.running = False
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=1.0)
        print("✅ 鼠标移动已停止")
    
    def create_gui(self):
        """创建图形用户界面"""
        def on_start():
            try:
                duration = int(duration_var.get())
                speed = float(speed_var.get())
                if self.start(duration, speed):
                    status_label.config(text="🐭 鼠标正在随机移动...", foreground="blue")
                    start_btn.config(state="disabled")
                    stop_btn.config(state="normal")
            except ValueError:
                messagebox.showerror("错误", "请输入有效的数字")
        
        def on_stop():
            self.stop()
            status_label.config(text="✅ 已停止", foreground="green")
            start_btn.config(state="normal")
            stop_btn.config(state="disabled")
        
        def on_exit():
            self.stop()
            root.destroy()
            sys.exit()
        
        # 创建主窗口
        root = tk.Tk()
        root.title("🐭 鼠标随机移动器")
        root.geometry("400x250")
        root.resizable(False, False)
        root.protocol("WM_DELETE_WINDOW", on_exit)
        
        # 设置样式
        style = ttk.Style()
        style.configure('TFrame', padding=10)
        style.configure('TLabel', font=('Arial', 10))
        style.configure('TButton', font=('Arial', 10))
        
        # 主框架
        main_frame = ttk.Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 标题
        title_label = ttk.Label(main_frame, text="🐭 鼠标随机移动器", 
                               font=('Arial', 16, 'bold'))
        title_label.pack(pady=10)
        
        # 设置框架
        settings_frame = ttk.Frame(main_frame)
        settings_frame.pack(fill=tk.X, pady=10)
        
        # 持续时间设置
        ttk.Label(settings_frame, text="运行时间(秒，0=无限):").grid(row=0, column=0, sticky=tk.W, pady=5)
        duration_var = tk.StringVar(value="30")
        ttk.Entry(settings_frame, textvariable=duration_var, width=10).grid(row=0, column=1, pady=5)
        
        # 移动速度设置
        ttk.Label(settings_frame, text="移动速度(秒):").grid(row=1, column=0, sticky=tk.W, pady=5)
        speed_var = tk.StringVar(value="0.5")
        ttk.Entry(settings_frame, textvariable=speed_var, width=10).grid(row=1, column=1, pady=5)
        
        # 按钮框架
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=10)
        
        start_btn = ttk.Button(button_frame, text="开始", command=on_start)
        start_btn.pack(side=tk.LEFT, padx=5)
        
        stop_btn = ttk.Button(button_frame, text="停止", command=on_stop, state="disabled")
        stop_btn.pack(side=tk.LEFT, padx=5)
        
        # 状态标签
        status_label = ttk.Label(main_frame, text="就绪", foreground="green")
        status_label.pack(pady=10)
        
        # 警告标签
        warning_label = ttk.Label(main_frame, 
                                 text="⚠️ 注意：使用期间请勿进行重要操作",
                                 foreground="red", font=('Arial', 9))
        warning_label.pack(pady=5)
        
        root.mainloop()

# 简单的命令行版本
def simple_mouse_mover():
    """简单的命令行版本"""
    mover = MouseMover()
    
    print("=" * 50)
    print("🐭 鼠标随机移动器")
    print("=" * 50)
    
    try:
        duration = int(input("请输入运行时间(秒，0=无限): ") or "30")
        speed = float(input("请输入移动速度(秒): ") or "0.5")
        
        print("\n开始移动鼠标...")
        print("按 Ctrl+C 停止")
        
        mover.start(duration, speed)
        
        # 等待线程结束或用户中断
        while mover.running:
            time.sleep(0.1)
            
    except ValueError:
        print("❌ 请输入有效的数字")
    except KeyboardInterrupt:
        print("\n🛑 用户中断")
        mover.stop()
    except Exception as e:
        print(f"❌ 发生错误: {e}")
        mover.stop()

# 直接运行版本
def run_directly():
    """直接运行版本"""
    mover = MouseMover()
    
    print("🐭 鼠标随机移动器 - 直接运行")
    print("⏹️  按 Ctrl+C 停止")
    
    try:
        mover.start(duration=0, speed=0.8)  # 无限运行，速度0.8秒
        
        # 保持主线程运行
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n✅ 程序已停止")
        mover.stop()

if __name__ == "__main__":
    # 方法1：使用图形界面（推荐）
    # mover = MouseMover()
    # mover.create_gui()
    
    # 方法2：使用命令行交互
    # simple_mouse_mover()
    
    # 方法3：直接运行（最简单的测试）
    run_directly()