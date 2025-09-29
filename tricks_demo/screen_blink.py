import tkinter as tk
import random
import time
import threading
import sys
from tkinter import ttk, messagebox
import pygame
import os
from PIL import Image, ImageTk
import math

class ScreenFlasher:
    def __init__(self):
        self.running = False
        self.thread = None
        self.root = None
        self.safety_timer = None
        
    def create_flash_window(self, mode="color"):
        """创建闪烁窗口"""
        if self.root:
            try:
                self.root.destroy()
            except:
                pass
        
        self.root = tk.Tk()
        self.root.attributes('-fullscreen', True)
        self.root.configure(background='black')
        self.root.attributes('-topmost', True)
        
        # 添加退出快捷键
        self.root.bind('<Escape>', lambda e: self.stop())
        self.root.bind('<Control-q>', lambda e: self.stop())
        
        # 根据模式设置不同的效果
        if mode == "color":
            self.root.attributes('-alpha', 1.0)
        elif mode == "transparent":
            self.root.attributes('-alpha', 0.7)
        
        return self.root
    
    def color_flash(self, intensity=1, duration=30):
        """颜色闪烁效果"""
        print("🎨 开始颜色闪烁效果！")
        print("⏹️  按ESC键或Ctrl+Q停止")
        
        colors = [
            '#FF0000', '#00FF00', '#0000FF', '#FFFF00', '#FF00FF', '#00FFFF',
            '#FFFFFF', '#000000', '#FFA500', '#800080', '#FFC0CB', '#00FF7F'
        ]
        
        start_time = time.time()
        flash_count = 0
        
        try:
            root = self.create_flash_window("color")
            
            while self.running:
                # 根据强度调整闪烁速度
                if intensity == 1:  # 慢速
                    flash_delay = random.uniform(0.3, 0.8)
                elif intensity == 2:  # 中速
                    flash_delay = random.uniform(0.1, 0.3)
                else:  # 快速
                    flash_delay = random.uniform(0.05, 0.15)
                
                # 随机选择颜色
                bg_color = random.choice(colors)
                root.configure(background=bg_color)
                root.update()
                
                flash_count += 1
                if flash_count % 10 == 0:
                    print(f"✨ 第{flash_count}次闪烁: {bg_color}")
                
                # 检查持续时间
                if duration > 0 and (time.time() - start_time) >= duration:
                    print("⏰ 时间到，自动停止")
                    self.stop()
                    break
                
                time.sleep(flash_delay)
                
        except Exception as e:
            print(f"❌ 发生错误: {e}")
            self.stop()
    
    def strobe_effect(self, frequency=10, duration=30):
        """频闪灯效果"""
        print("⚡ 开始频闪灯效果！")
        
        start_time = time.time()
        flash_count = 0
        
        try:
            root = self.create_flash_window("color")
            
            while self.running:
                # 黑白交替
                if flash_count % 2 == 0:
                    root.configure(background='white')
                else:
                    root.configure(background='black')
                
                root.update()
                flash_count += 1
                
                # 根据频率计算延迟
                delay = 1.0 / frequency
                time.sleep(delay)
                
                # 显示状态
                if flash_count % 20 == 0:
                    print(f"⚡ 频闪频率: {frequency}Hz, 次数: {flash_count}")
                
                # 检查持续时间
                if duration > 0 and (time.time() - start_time) >= duration:
                    print("⏰ 时间到，自动停止")
                    self.stop()
                    break
                    
        except Exception as e:
            print(f"❌ 发生错误: {e}")
            self.stop()
    
    def rainbow_effect(self, speed=1, duration=30):
        """彩虹渐变效果"""
        print("🌈 开始彩虹渐变效果！")
        
        start_time = time.time()
        hue = 0
        
        try:
            root = self.create_flash_window("color")
            
            while self.running:
                # 生成彩虹颜色 (HSL颜色空间)
                r, g, b = self.hsl_to_rgb(hue / 360, 1.0, 0.5)
                color = f'#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}'
                
                root.configure(background=color)
                root.update()
                
                # 更新色相
                hue = (hue + speed) % 360
                
                # 显示状态
                if int(hue) % 60 == 0:
                    print(f"🌈 色相: {int(hue)}°, 颜色: {color}")
                
                # 检查持续时间
                if duration > 0 and (time.time() - start_time) >= duration:
                    print("⏰ 时间到，自动停止")
                    self.stop()
                    break
                
                time.sleep(0.02)
                
        except Exception as e:
            print(f"❌ 发生错误: {e}")
            self.stop()
    
    def hsl_to_rgb(self, h, s, l):
        """HSL颜色空间转RGB"""
        def hue_to_rgb(p, q, t):
            if t < 0: t += 1
            if t > 1: t -= 1
            if t < 1/6: return p + (q - p) * 6 * t
            if t < 1/2: return q
            if t < 2/3: return p + (q - p) * (2/3 - t) * 6
            return p
        
        if s == 0:
            return l, l, l
        
        q = l * (1 + s) if l < 0.5 else l + s - l * s
        p = 2 * l - q
        
        r = hue_to_rgb(p, q, h + 1/3)
        g = hue_to_rgb(p, q, h)
        b = hue_to_rgb(p, q, h - 1/3)
        
        return r, g, b
    
    def matrix_effect(self, duration=30):
        """矩阵数字雨效果"""
        print("💻 开始矩阵数字雨效果！")
        
        try:
            root = self.create_flash_window("color")
            root.configure(background='black')
            
            # 创建画布
            canvas = tk.Canvas(root, bg='black', highlightthickness=0)
            canvas.pack(fill=tk.BOTH, expand=True)
            
            # 获取屏幕尺寸
            width = root.winfo_screenwidth()
            height = root.winfo_screenheight()
            
            columns = width // 20
            drops = [1] * columns
            
            start_time = time.time()
            
            while self.running:
                canvas.delete("all")
                
                # 绘制数字雨
                for i in range(columns):
                    x = i * 20
                    y = drops[i] * 20
                    
                    # 随机数字
                    char = random.choice('01010101010101010101')
                    
                    # 渐变色
                    color = f'#00FF{min(255, drops[i]*10):02x}'
                    
                    canvas.create_text(x, y, text=char, fill=color, 
                                      font=('Courier', 14), anchor=tk.NW)
                    
                    # 更新下落位置
                    if y > height or random.random() > 0.95:
                        drops[i] = 0
                    drops[i] += 1
                
                root.update()
                time.sleep(0.05)
                
                # 检查持续时间
                if duration > 0 and (time.time() - start_time) >= duration:
                    print("⏰ 时间到，自动停止")
                    self.stop()
                    break
                    
        except Exception as e:
            print(f"❌ 发生错误: {e}")
            self.stop()
    
    def start(self, effect_type="color", **kwargs):
        """开始闪烁效果"""
        if not self.running:
            self.running = True
            
            # 显示警告
            self.show_epilepsy_warning()
            
            # 启动安全计时器
            self.start_safety_timer(kwargs.get('duration', 30))
            
            # 选择效果类型
            if effect_type == "color":
                target = self.color_flash
            elif effect_type == "strobe":
                target = self.strobe_effect
            elif effect_type == "rainbow":
                target = self.rainbow_effect
            elif effect_type == "matrix":
                target = self.matrix_effect
            else:
                target = self.color_flash
            
            self.thread = threading.Thread(target=target, kwargs=kwargs)
            self.thread.daemon = True
            self.thread.start()
            return True
        return False
    
    def start_safety_timer(self, duration):
        """启动安全计时器"""
        def safety_check():
            time.sleep(duration + 2)  # 额外2秒缓冲
            if self.running:
                print("🛡️  安全计时器触发，自动停止")
                self.stop()
        
        if duration > 0:
            self.safety_timer = threading.Thread(target=safety_check)
            self.safety_timer.daemon = True
            self.safety_timer.start()
    
    def show_epilepsy_warning(self):
        """显示癫痫警告"""
        warning_text = """
        ⚠️ 癫痫警告 ⚠️
        
        此程序包含闪烁灯光效果，可能对
        光敏性癫痫患者或相关疾病患者
        造成不适或引发癫痫发作。
        
        如果您或家人有相关病史，请勿使用。
        使用时请确保环境安全。
        
        确定要继续吗？
        """
        
        root = tk.Tk()
        root.withdraw()
        result = messagebox.askyesno("癫痫警告", warning_text, icon='warning')
        root.destroy()
        
        if not result:
            print("❌ 用户取消操作")
            sys.exit(0)
    
    def stop(self):
        """停止闪烁效果"""
        self.running = False
        if self.root:
            try:
                self.root.after(100, self.root.destroy)
            except:
                pass
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=2.0)
        print("✅ 闪烁效果已停止")
    
    def create_gui(self):
        """创建图形用户界面"""
        def on_start():
            try:
                effect = effect_var.get()
                duration = int(duration_var.get())
                intensity = intensity_var.get()
                
                if effect == "color":
                    self.start("color", intensity=intensity, duration=duration)
                elif effect == "strobe":
                    freq = int(freq_var.get())
                    self.start("strobe", frequency=freq, duration=duration)
                elif effect == "rainbow":
                    speed = speed_var.get()
                    self.start("rainbow", speed=speed, duration=duration)
                elif effect == "matrix":
                    self.start("matrix", duration=duration)
                
                status_label.config(text="🎬 效果运行中...", foreground="blue")
                start_btn.config(state="disabled")
                stop_btn.config(state="normal")
                
            except ValueError:
                messagebox.showerror("错误", "请输入有效的数字")
        
        def on_stop():
            self.stop()
            status_label.config(text="✅ 已停止", foreground="green")
            start_btn.config(state="normal")
            stop_btn.config(state="disabled")
        
        def on_effect_change(*args):
            effect = effect_var.get()
            if effect == "strobe":
                freq_frame.pack()
                speed_frame.pack_forget()
            elif effect == "rainbow":
                speed_frame.pack()
                freq_frame.pack_forget()
            else:
                freq_frame.pack_forget()
                speed_frame.pack_forget()
        
        # 创建主窗口
        root = tk.Tk()
        root.title("🎬 屏幕闪烁效果")
        root.geometry("500x400")
        root.resizable(False, False)
        
        # 主框架
        main_frame = ttk.Frame(root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题
        title_label = ttk.Label(main_frame, text="🎬 屏幕闪烁效果生成器", 
                               font=('Arial', 16, 'bold'))
        title_label.pack(pady=10)
        
        # 效果选择
        ttk.Label(main_frame, text="选择效果:").pack(anchor=tk.W)
        effect_var = tk.StringVar(value="color")
        effect_combo = ttk.Combobox(main_frame, textvariable=effect_var,
                                  values=["color", "strobe", "rainbow", "matrix"])
        effect_combo.pack(fill=tk.X, pady=5)
        effect_var.trace('w', on_effect_change)
        
        # 持续时间
        ttk.Label(main_frame, text="持续时间(秒):").pack(anchor=tk.W)
        duration_var = tk.StringVar(value="15")
        ttk.Entry(main_frame, textvariable=duration_var).pack(fill=tk.X, pady=5)
        
        # 强度选择
        ttk.Label(main_frame, text="强度:").pack(anchor=tk.W)
        intensity_var = tk.IntVar(value=2)
        ttk.Radiobutton(main_frame, text="温和", variable=intensity_var, value=1).pack(anchor=tk.W)
        ttk.Radiobutton(main_frame, text="中等", variable=intensity_var, value=2).pack(anchor=tk.W)
        ttk.Radiobutton(main_frame, text="强烈", variable=intensity_var, value=3).pack(anchor=tk.W)
        
        # 频闪频率（动态显示）
        freq_frame = ttk.Frame(main_frame)
        ttk.Label(freq_frame, text="频闪频率(Hz):").pack(anchor=tk.W)
        freq_var = tk.StringVar(value="10")
        ttk.Entry(freq_frame, textvariable=freq_var, width=10).pack(anchor=tk.W)
        
        # 彩虹速度（动态显示）
        speed_frame = ttk.Frame(main_frame)
        ttk.Label(speed_frame, text="彩虹速度:").pack(anchor=tk.W)
        speed_var = tk.IntVar(value=3)
        ttk.Radiobutton(speed_frame, text="慢速", variable=speed_var, value=1).pack(anchor=tk.W)
        ttk.Radiobutton(speed_frame, text="中速", variable=speed_var, value=3).pack(anchor=tk.W)
        ttk.Radiobutton(speed_frame, text="快速", variable=speed_var, value=5).pack(anchor=tk.W)
        
        # 按钮
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=10)
        
        start_btn = ttk.Button(btn_frame, text="开始", command=on_start)
        start_btn.pack(side=tk.LEFT, padx=5)
        
        stop_btn = ttk.Button(btn_frame, text="停止", command=on_stop, state="disabled")
        stop_btn.pack(side=tk.LEFT, padx=5)
        
        # 状态
        status_label = ttk.Label(main_frame, text="就绪", foreground="green")
        status_label.pack(pady=5)
        
        # 警告
        warning_label = ttk.Label(main_frame, 
            text="⚠️ 警告：可能引发光敏性癫痫！有相关病史者请勿使用！",
            foreground="red", font=('Arial', 9))
        warning_label.pack(pady=5)
        
        root.mainloop()

# 简单测试函数
def test_flash_effect():
    """简单测试闪烁效果"""
    flasher = ScreenFlasher()
    
    print("选择测试效果:")
    print("1. 颜色闪烁")
    print("2. 频闪效果")
    print("3. 彩虹效果")
    print("4. 矩阵效果")
    
    try:
        choice = input("请输入选择(1-4): ").strip()
        duration = int(input("持续时间(秒): ") or "10")
        
        if choice == "1":
            flasher.start("color", duration=duration, intensity=2)
        elif choice == "2":
            flasher.start("strobe", duration=duration, frequency=8)
        elif choice == "3":
            flasher.start("rainbow", duration=duration, speed=3)
        elif choice == "4":
            flasher.start("matrix", duration=duration)
        else:
            print("无效选择")
            return
        
        # 等待效果完成
        while flasher.running:
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("\n用户中断")
        flasher.stop()
    except Exception as e:
        print(f"错误: {e}")
        flasher.stop()

if __name__ == "__main__":
    # 方法1：使用图形界面（推荐）
    flasher = ScreenFlasher()
    flasher.create_gui()
    
    # 方法2：简单测试
    # test_flash_effect()
    
    # 方法3：直接运行颜色闪烁（10秒）
    # flasher = ScreenFlasher()
    # flasher.start("color", duration=10, intensity=2)
    # time.sleep(12)  # 等待完成