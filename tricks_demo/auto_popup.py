import tkinter as tk
from tkinter import messagebox, ttk
import random
import time
import threading
import json
import os
import sys
from datetime import datetime
import math
from PIL import Image, ImageTk
import pygame

class PopupPrank:
    def __init__(self):
        self.running = False
        self.thread = None
        self.active_windows = []
        self.config_file = "popup_config.json"
        self.load_config()
        
        # 初始化pygame用于音效
        try:
            pygame.mixer.init()
        except:
            print("音效功能不可用")
    
    def load_config(self):
        """加载配置文件"""
        default_config = {
            "popup_speed": 1.0,
            "popup_duration": 5.0,
            "max_windows": 10,
            "sound_effects": True,
            "recent_messages": [
                "你的电脑已被感染！",
                "发现病毒！立即扫描！",
                "系统文件损坏",
                "内存不足，请关闭程序",
                "网络连接已断开",
                "软件更新可用",
                "安全警告：可疑活动",
                "电池电量低，请充电",
                "磁盘空间不足",
                "防火墙已阻止程序"
            ],
            "animation_effects": True,
            "window_styles": ["error", "warning", "info", "question"]
        }
        
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
            else:
                self.config = default_config
                self.save_config()
        except:
            self.config = default_config
    
    def save_config(self):
        """保存配置文件"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
        except:
            pass
    
    def play_sound(self, sound_type):
        """播放音效"""
        if not self.config.get('sound_effects', True):
            return
            
        try:
            if sound_type == "error":
                pygame.mixer.Sound(self.generate_beep_sound(440, 0.5)).play()
            elif sound_type == "warning":
                pygame.mixer.Sound(self.generate_beep_sound(330, 0.3)).play()
            elif sound_type == "info":
                pygame.mixer.Sound(self.generate_beep_sound(523, 0.2)).play()
        except:
            pass
    
    def generate_beep_sound(self, frequency, duration):
        """生成简单的蜂鸣声"""
        sample_rate = 44100
        n_samples = int(round(duration * sample_rate))
        buf = numpy.zeros((n_samples, 2), dtype=numpy.int16)
        max_sample = 2**(16 - 1) - 1
        
        for s in range(n_samples):
            t = float(s) / sample_rate
            buf[s][0] = int(max_sample * math.sin(2 * math.pi * frequency * t))
            buf[s][1] = int(max_sample * math.sin(2 * math.pi * frequency * t))
            
        return buf
    
    def create_popup_window(self, message, style="error"):
        """创建弹窗窗口"""
        if len(self.active_windows) >= self.config.get('max_windows', 10):
            return
            
        try:
            root = tk.Toplevel()
            root.attributes('-topmost', True)
            root.attributes('-alpha', 0.95)
            root.configure(bg='white')
            root.resizable(False, False)
            
            # 随机位置
            screen_width = root.winfo_screenwidth()
            screen_height = root.winfo_screenheight()
            x = random.randint(100, screen_width - 400)
            y = random.randint(100, screen_height - 200)
            root.geometry(f"300x150+{x}+{y}")
            
            # 设置标题和图标
            if style == "error":
                root.title("错误")
                icon_color = "#ff4444"
            elif style == "warning":
                root.title("警告")
                icon_color = "#ffaa00"
            elif style == "info":
                root.title("信息")
                icon_color = "#4488ff"
            else:
                root.title("问题")
                icon_color = "#44aa44"
            
            # 主框架
            main_frame = tk.Frame(root, bg='white', padx=20, pady=20)
            main_frame.pack(fill=tk.BOTH, expand=True)
            
            # 图标和消息
            icon_frame = tk.Frame(main_frame, bg='white')
            icon_frame.pack(side=tk.LEFT, padx=(0, 15))
            
            # 简单的图标模拟
            icon_canvas = tk.Canvas(icon_frame, width=32, height=32, bg='white', 
                                  highlightthickness=0)
            icon_canvas.pack()
            
            if style == "error":
                icon_canvas.create_oval(6, 6, 26, 26, fill=icon_color, outline='')
                icon_canvas.create_text(16, 16, text="!", fill='white', 
                                     font=('Arial', 16, 'bold'))
            elif style == "warning":
                icon_canvas.create_polygon(16, 6, 6, 26, 26, 26, fill=icon_color)
                icon_canvas.create_text(16, 16, text="!", fill='white', 
                                     font=('Arial', 14, 'bold'))
            else:
                icon_canvas.create_oval(6, 6, 26, 26, fill=icon_color, outline='')
                icon_canvas.create_text(16, 16, text="i", fill='white', 
                                     font=('Arial', 16, 'bold'))
            
            # 消息文本
            msg_frame = tk.Frame(main_frame, bg='white')
            msg_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            
            msg_label = tk.Label(msg_frame, text=message, bg='white', 
                               font=('Arial', 10), wraplength=180, justify=tk.LEFT)
            msg_label.pack(anchor=tk.W)
            
            # 按钮
            btn_frame = tk.Frame(main_frame, bg='white')
            btn_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(10, 0))
            
            if random.random() < 0.3:  # 30%的概率有多个按钮
                tk.Button(btn_frame, text="确定", command=root.destroy, 
                        width=8).pack(side=tk.LEFT, padx=5)
                tk.Button(btn_frame, text="取消", command=root.destroy, 
                        width=8).pack(side=tk.LEFT, padx=5)
            else:
                tk.Button(btn_frame, text="确定", command=root.destroy, 
                        width=10).pack()
            
            # 动画效果
            if self.config.get('animation_effects', True):
                self.animate_window(root)
            
            # 播放音效
            self.play_sound(style)
            
            self.active_windows.append(root)
            
            # 自动关闭计时器
            close_time = self.config.get('popup_duration', 5.0)
            root.after(int(close_time * 1000), lambda: self.close_window(root))
            
            root.protocol("WM_DELETE_WINDOW", lambda: self.close_window(root))
            
        except Exception as e:
            print(f"创建弹窗失败: {e}")
    
    def animate_window(self, window):
        """窗口动画效果"""
        try:
            # 震动效果
            def shake():
                x = window.winfo_x()
                y = window.winfo_y()
                for i in range(5):
                    offset = random.randint(-5, 5)
                    window.geometry(f"+{x+offset}+{y+offset}")
                    window.update()
                    time.sleep(0.05)
                window.geometry(f"+{x}+{y}")
            
            # 淡入效果
            def fade_in():
                for alpha in range(0, 100, 5):
                    window.attributes('-alpha', alpha/100)
                    window.update()
                    time.sleep(0.02)
                window.attributes('-alpha', 0.95)
            
            # 随机选择动画
            animations = [shake, fade_in]
            random.choice(animations)()
            
        except:
            pass
    
    def close_window(self, window):
        """关闭窗口"""
        try:
            if window in self.active_windows:
                self.active_windows.remove(window)
            window.destroy()
        except:
            pass
    
    def close_all_windows(self):
        """关闭所有弹窗"""
        for window in self.active_windows[:]:
            try:
                window.destroy()
            except:
                pass
        self.active_windows.clear()
    
    def get_random_message(self):
        """获取随机消息"""
        messages = self.config.get('recent_messages', [])
        if not messages:
            messages = [
                "系统错误：0x80070005",
                "内存访问冲突",
                "磁盘读取错误",
                "网络超时",
                "软件许可证过期",
                "需要管理员权限",
                "文件正在被使用",
                "备份失败",
                "安全证书无效",
                "驱动程序不兼容"
            ]
        
        tech_terms = ["CPU", "GPU", "RAM", "SSD", "USB", "DNS", "HTTP", "SSL", "IP"]
        formats = [
            "{}使用率过高",
            "{}驱动程序需要更新",
            "{}缓存已满",
            "{}温度异常",
            "{}连接不稳定"
        ]
        
        if random.random() < 0.7:  # 70%概率使用预设消息
            return random.choice(messages)
        else:  # 30%概率生成技术消息
            term = random.choice(tech_terms)
            format_str = random.choice(formats)
            return format_str.format(term)
    
    def get_random_style(self):
        """获取随机样式"""
        styles = self.config.get('window_styles', ["error", "warning", "info", "question"])
        weights = [0.4, 0.3, 0.2, 0.1]  # 错误>警告>信息>问题
        return random.choices(styles, weights=weights, k=1)[0]
    
    def popup_prank_mode(self, duration=60, intensity=2):
        """弹窗恶作剧模式"""
        print("🪟 弹窗恶作剧模式启动！")
        print("⏹️  按停止按钮或关闭程序停止")
        
        start_time = time.time()
        popup_count = 0
        
        try:
            while self.running:
                # 根据强度调整弹窗频率
                if intensity == 1:  # 温和
                    delay = random.uniform(3.0, 8.0)
                elif intensity == 2:  # 中等
                    delay = random.uniform(1.5, 4.0)
                else:  # 强烈
                    delay = random.uniform(0.5, 2.0)
                
                # 创建弹窗
                message = self.get_random_message()
                style = self.get_random_style()
                
                self.create_popup_window(message, style)
                popup_count += 1
                
                if popup_count % 5 == 0:
                    print(f"📊 已创建{popup_count}个弹窗，当前活跃: {len(self.active_windows)}")
                
                # 检查持续时间
                if duration > 0 and (time.time() - start_time) >= duration:
                    print("⏰ 时间到，自动停止")
                    break
                
                time.sleep(delay)
                
        except Exception as e:
            print(f"❌ 发生错误: {e}")
        finally:
            self.running = False
            self.close_all_windows()
            print("✅ 弹窗模式已停止")
    
    def fake_scan_mode(self, duration=30):
        """假扫描模式"""
        print("🔍 假系统扫描模式启动！")
        
        scan_messages = [
            "正在扫描系统文件...",
            "检测到潜在威胁",
            "清理临时文件中",
            "优化注册表",
            "检查磁盘错误",
            "验证系统完整性",
            "更新安全定义",
            "扫描网络连接",
            "分析启动程序",
            "检查浏览器插件"
        ]
        
        try:
            for i, message in enumerate(scan_messages):
                if not self.running:
                    break
                
                style = "info" if random.random() < 0.7 else "warning"
                self.create_popup_window(f"{message} ({i+1}/{len(scan_messages)})", style)
                
                # 模拟扫描进度
                if i == len(scan_messages) - 1:
                    self.create_popup_window("扫描完成！发现0个威胁", "info")
                
                time.sleep(random.uniform(2.0, 4.0))
                
        except Exception as e:
            print(f"❌ 发生错误: {e}")
        finally:
            self.running = False
            self.close_all_windows()
            print("✅ 扫描模式已停止")
    
    def start(self, mode="popup", **kwargs):
        """开始弹窗"""
        if not self.running:
            self.running = True
            
            if mode == "popup":
                target = self.popup_prank_mode
            elif mode == "scan":
                target = self.fake_scan_mode
            else:
                target = self.popup_prank_mode
            
            self.thread = threading.Thread(target=target, kwargs=kwargs)
            self.thread.daemon = True
            self.thread.start()
            return True
        return False
    
    def stop(self):
        """停止弹窗"""
        self.running = False
        self.close_all_windows()
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=2.0)
        print("✅ 弹窗已停止")
    
    def create_gui(self):
        """创建图形用户界面"""
        def on_start():
            try:
                mode = mode_var.get()
                duration = int(duration_var.get())
                intensity = intensity_var.get()
                
                if mode == "popup":
                    self.start("popup", duration=duration, intensity=intensity)
                elif mode == "scan":
                    self.start("scan", duration=duration)
                
                status_label.config(text="🪟 弹窗运行中...", foreground="blue")
                start_btn.config(state="disabled")
                stop_btn.config(state="normal")
                
            except ValueError:
                messagebox.showerror("错误", "请输入有效的数字")
        
        def on_stop():
            self.stop()
            status_label.config(text="✅ 已停止", foreground="green")
            start_btn.config(state="normal")
            stop_btn.config(state="disabled")
        
        def on_settings():
            """打开设置窗口"""
            settings_win = tk.Toplevel()
            settings_win.title("⚙️ 弹窗设置")
            settings_win.geometry("400x300")
            settings_win.resizable(False, False)
            
            ttk.Label(settings_win, text="弹窗持续时间(秒):").pack(pady=5)
            duration_var = tk.StringVar(value=str(self.config.get('popup_duration', 5.0)))
            ttk.Entry(settings_win, textvariable=duration_var).pack(pady=5)
            
            ttk.Label(settings_win, text="最大同时弹窗数:").pack(pady=5)
            max_win_var = tk.StringVar(value=str(self.config.get('max_windows', 10)))
            ttk.Entry(settings_win, textvariable=max_win_var).pack(pady=5)
            
            sound_var = tk.BooleanVar(value=self.config.get('sound_effects', True))
            ttk.Checkbutton(settings_win, text="启用音效", variable=sound_var).pack(pady=5)
            
            anim_var = tk.BooleanVar(value=self.config.get('animation_effects', True))
            ttk.Checkbutton(settings_win, text="启用动画效果", variable=anim_var).pack(pady=5)
            
            def save_settings():
                try:
                    self.config['popup_duration'] = float(duration_var.get())
                    self.config['max_windows'] = int(max_win_var.get())
                    self.config['sound_effects'] = sound_var.get()
                    self.config['animation_effects'] = anim_var.get()
                    self.save_config()
                    settings_win.destroy()
                    messagebox.showinfo("成功", "设置已保存")
                except ValueError:
                    messagebox.showerror("错误", "请输入有效的数字")
            
            ttk.Button(settings_win, text="保存", command=save_settings).pack(pady=10)
        
        # 创建主窗口
        root = tk.Tk()
        root.title("🎭 自动弹窗恶作剧")
        root.geometry("500x400")
        root.resizable(False, False)
        
        # 主框架
        main_frame = ttk.Frame(root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题
        title_label = ttk.Label(main_frame, text="🎭 自动弹窗恶作剧", 
                               font=('Arial', 16, 'bold'))
        title_label.pack(pady=10)
        
        # 模式选择
        ttk.Label(main_frame, text="选择模式:").pack(anchor=tk.W)
        mode_var = tk.StringVar(value="popup")
        mode_combo = ttk.Combobox(main_frame, textvariable=mode_var,
                                values=["popup", "scan"])
        mode_combo.pack(fill=tk.X, pady=5)
        
        # 持续时间
        ttk.Label(main_frame, text="运行时间(秒，0=无限):").pack(anchor=tk.W)
        duration_var = tk.StringVar(value="30")
        ttk.Entry(main_frame, textvariable=duration_var).pack(fill=tk.X, pady=5)
        
        # 强度选择
        ttk.Label(main_frame, text="弹窗强度:").pack(anchor=tk.W)
        intensity_var = tk.IntVar(value=2)
        ttk.Radiobutton(main_frame, text="温和", variable=intensity_var, value=1).pack(anchor=tk.W)
        ttk.Radiobutton(main_frame, text="中等", variable=intensity_var, value=2).pack(anchor=tk.W)
        ttk.Radiobutton(main_frame, text="强烈", variable=intensity_var, value=3).pack(anchor=tk.W)
        
        # 按钮框架
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=15)
        
        start_btn = ttk.Button(btn_frame, text="开始弹窗", command=on_start)
        start_btn.pack(side=tk.LEFT, padx=5)
        
        stop_btn = ttk.Button(btn_frame, text="停止", command=on_stop, state="disabled")
        stop_btn.pack(side=tk.LEFT, padx=5)
        
        settings_btn = ttk.Button(btn_frame, text="设置", command=on_settings)
        settings_btn.pack(side=tk.LEFT, padx=5)
        
        # 状态标签
        status_label = ttk.Label(main_frame, text="就绪", foreground="green")
        status_label.pack(pady=5)
        
        # 统计信息
        stats_label = ttk.Label(main_frame, text="活跃弹窗: 0", foreground="gray")
        stats_label.pack(pady=2)
        
        # 更新统计信息
        def update_stats():
            if self.running:
                stats_label.config(text=f"活跃弹窗: {len(self.active_windows)}")
            root.after(1000, update_stats)
        
        update_stats()
        
        # 说明文本
        help_text = """
        💡 使用说明:
        1. 选择模式和强度后点击"开始弹窗"
        2. 程序会自动创建随机弹窗
        3. 弹窗会自动关闭，也可手动关闭
        4. 点击"停止"按钮终止程序
        5. 在"设置"中调整详细参数
        """
        
        help_label = ttk.Label(main_frame, text=help_text, foreground="gray", 
                              font=('Arial', 9), justify=tk.LEFT)
        help_label.pack(pady=5, anchor=tk.W)
        
        # 警告
        warning_label = ttk.Label(main_frame, 
            text="⚠️ 警告：仅供娱乐，请勿用于恶意目的！",
            foreground="red", font=('Arial', 9))
        warning_label.pack(pady=5)
        
        root.mainloop()

# 简单测试函数
def quick_test():
    """快速测试"""
    prank = PopupPrank()
    
    print("🎭 弹窗恶作剧 - 快速测试")
    print("选择模式:")
    print("1. 随机弹窗模式")
    print("2. 假系统扫描模式")
    
    try:
        choice = input("请输入选择(1-2): ").strip()
        duration = int(input("运行时间(秒): ") or "20")
        
        if choice == "1":
            print("🪟 启动随机弹窗模式...")
            prank.start("popup", duration=duration, intensity=2)
        elif choice == "2":
            print("🔍 启动假扫描模式...")
            prank.start("scan", duration=duration)
        else:
            print("无效选择")
            return
        
        # 等待完成
        while prank.running:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n用户中断")
        prank.stop()
    except Exception as e:
        print(f"错误: {e}")
        prank.stop()

if __name__ == "__main__":

    
    # 方法1：使用图形界面（推荐）
    prank = PopupPrank()
    prank.create_gui()
    
    # 方法2：快速测试
    # quick_test()
    
    # 方法3：直接运行弹窗模式
    # prank = PopupPrank()
    # prank.start("popup", duration=30, intensity=2)
    # time.sleep(35)  # 等待完成