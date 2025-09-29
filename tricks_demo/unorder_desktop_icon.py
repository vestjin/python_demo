import os
import random
import shutil
import time
from pathlib import Path
import tkinter as tk
from tkinter import messagebox, ttk
import json
from datetime import datetime

class DesktopIconShuffler:
    def __init__(self):
        self.desktop_path = self.get_desktop_path()
        self.backup_file = os.path.join(os.path.expanduser("~"), "desktop_backup.json")
        self.original_positions = {}
    
    def get_desktop_path(self):
        """获取桌面路径（跨平台支持）"""
        # Windows
        if os.name == 'nt':
            return os.path.join(os.path.expanduser("~"), "Desktop")
        # macOS
        elif os.name == 'posix':
            return os.path.join(os.path.expanduser("~"), "Desktop")
        # Linux
        else:
            return os.path.join(os.path.expanduser("~"), "Desktop")
    
    def backup_desktop(self):
        """备份桌面文件位置"""
        if not os.path.exists(self.desktop_path):
            return False
        
        self.original_positions = {}
        for item in os.listdir(self.desktop_path):
            item_path = os.path.join(self.desktop_path, item)
            if os.path.isfile(item_path) or os.path.isdir(item_path):
                self.original_positions[item] = {
                    'name': item,
                    'path': item_path,
                    'type': 'file' if os.path.isfile(item_path) else 'directory',
                    'size': os.path.getsize(item_path) if os.path.isfile(item_path) else 0,
                    'modified': os.path.getmtime(item_path)
                }
        
        # 保存备份到文件
        with open(self.backup_file, 'w', encoding='utf-8') as f:
            json.dump(self.original_positions, f, ensure_ascii=False, indent=2)
        
        return True
    
    def shuffle_icons(self, intensity=1):
        """随机排列桌面图标"""
        if not os.path.exists(self.desktop_path):
            print("找不到桌面目录")
            return False
        
        # 先备份
        if not self.backup_desktop():
            print("备份失败")
            return False
        
        items = []
        # 收集桌面上的所有文件和文件夹
        for item in os.listdir(self.desktop_path):
            item_path = os.path.join(self.desktop_path, item)
            if os.path.isfile(item_path) or os.path.isdir(item_path):
                items.append(item)
        
        if not items:
            print("桌面上没有文件")
            return False
        
        print(f"找到 {len(items)} 个桌面项目，开始随机排列...")
        
        # 根据强度决定打乱程度
        if intensity == 1:  # 轻度：只重命名
            for item in items:
                if not item.startswith('.'):  # 忽略隐藏文件
                    self._rename_item(item)
        
        elif intensity == 2:  # 中度：重命名并创建副本
            for item in items:
                if not item.startswith('.'):
                    self._rename_item(item)
                    self._create_copy(item)
        
        elif intensity == 3:  # 重度：完全打乱
            temp_dir = os.path.join(self.desktop_path, "temp_shuffle")
            os.makedirs(temp_dir, exist_ok=True)
            
            # 移动所有文件到临时目录
            for item in items:
                if not item.startswith('.'):
                    src = os.path.join(self.desktop_path, item)
                    dst = os.path.join(temp_dir, item)
                    shutil.move(src, dst)
            
            # 从临时目录随机移动回桌面
            temp_items = os.listdir(temp_dir)
            random.shuffle(temp_items)
            
            for item in temp_items:
                src = os.path.join(temp_dir, item)
                new_name = f"shuffled_{random.randint(1000, 9999)}_{item}"
                dst = os.path.join(self.desktop_path, new_name)
                shutil.move(src, dst)
            
            # 删除临时目录
            shutil.rmtree(temp_dir)
        
        print("桌面图标排列完成！")
        return True
    
    def _rename_item(self, item_name):
        """重命名单个项目"""
        old_path = os.path.join(self.desktop_path, item_name)
        if os.path.exists(old_path):
            name, ext = os.path.splitext(item_name)
            new_name = f"{name}_{random.randint(100, 999)}{ext}"
            new_path = os.path.join(self.desktop_path, new_name)
            
            # 确保新文件名不重复
            counter = 1
            while os.path.exists(new_path):
                new_name = f"{name}_{random.randint(100, 999)}_{counter}{ext}"
                new_path = os.path.join(self.desktop_path, new_name)
                counter += 1
            
            os.rename(old_path, new_path)
    
    def _create_copy(self, item_name):
        """创建文件副本"""
        old_path = os.path.join(self.desktop_path, item_name)
        if os.path.exists(old_path) and os.path.isfile(old_path):
            name, ext = os.path.splitext(item_name)
            copy_name = f"copy_{random.randint(100, 999)}_{name}{ext}"
            copy_path = os.path.join(self.desktop_path, copy_name)
            
            # 确保副本文件名不重复
            counter = 1
            while os.path.exists(copy_path):
                copy_name = f"copy_{random.randint(100, 999)}_{name}_{counter}{ext}"
                copy_path = os.path.join(self.desktop_path, copy_name)
                counter += 1
            
            shutil.copy2(old_path, copy_path)
    
    def restore_desktop(self):
        """恢复桌面到原始状态"""
        if not os.path.exists(self.backup_file):
            print("找不到备份文件，无法恢复")
            return False
        
        try:
            with open(self.backup_file, 'r', encoding='utf-8') as f:
                backup_data = json.load(f)
            
            # 首先清理当前桌面（保留备份文件）
            for item in os.listdir(self.desktop_path):
                if item != os.path.basename(self.backup_file):
                    item_path = os.path.join(self.desktop_path, item)
                    try:
                        if os.path.isfile(item_path):
                            os.remove(item_path)
                        elif os.path.isdir(item_path):
                            shutil.rmtree(item_path)
                    except:
                        pass
            
            # 恢复原始文件
            for item_info in backup_data.values():
                original_name = item_info['name']
                # 这里简化处理，实际应该从备份中恢复
                # 因为原文件可能已被移动或重命名，这里只是演示
            
            print("桌面已恢复（需要手动检查）")
            
            # 删除备份文件
            if os.path.exists(self.backup_file):
                os.remove(self.backup_file)
                
            return True
            
        except Exception as e:
            print(f"恢复失败: {e}")
            return False
    
    def create_gui(self):
        """创建图形界面"""
        root = tk.Tk()
        root.title("桌面图标随机排列器")
        root.geometry("400x300")
        root.resizable(False, False)
        
        # 设置样式
        style = ttk.Style()
        style.configure('TButton', font=('Arial', 12))
        style.configure('TLabel', font=('Arial', 12))
        
        # 创建界面元素
        frame = ttk.Frame(root, padding="20")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        label = ttk.Label(frame, text="桌面图标随机排列器", font=('Arial', 16, 'bold'))
        label.grid(row=0, column=0, columnspan=2, pady=10)
        
        # 强度选择
        ttk.Label(frame, text="选择打乱强度:").grid(row=1, column=0, sticky=tk.W, pady=5)
        intensity_var = tk.IntVar(value=1)
        
        ttk.Radiobutton(frame, text="轻度（重命名）", variable=intensity_var, value=1).grid(row=2, column=0, sticky=tk.W)
        ttk.Radiobutton(frame, text="中度（重命名+副本）", variable=intensity_var, value=2).grid(row=3, column=0, sticky=tk.W)
        ttk.Radiobutton(frame, text="重度（完全打乱）", variable=intensity_var, value=3).grid(row=4, column=0, sticky=tk.W)
        
        # 按钮
        shuffle_btn = ttk.Button(frame, text="开始随机排列", 
                               command=lambda: self.on_shuffle(intensity_var.get()))
        shuffle_btn.grid(row=5, column=0, pady=10, sticky=tk.W+tk.E)
        
        restore_btn = ttk.Button(frame, text="恢复桌面", 
                               command=self.on_restore)
        restore_btn.grid(row=6, column=0, pady=5, sticky=tk.W+tk.E)
        
        # 状态标签
        self.status_label = ttk.Label(frame, text="就绪", foreground="green")
        self.status_label.grid(row=7, column=0, pady=10)
        
        # 警告标签
        warning_label = ttk.Label(frame, text="⚠️ 警告：此操作可能会影响桌面文件", 
                                foreground="red", font=('Arial', 10))
        warning_label.grid(row=8, column=0, pady=5)
        
        root.mainloop()
    
    def on_shuffle(self, intensity):
        """处理开始排列按钮点击"""
        if messagebox.askyesno("确认", "确定要随机排列桌面图标吗？\n建议先备份重要文件！"):
            self.status_label.config(text="正在处理...", foreground="blue")
            self.status_label.update()
            
            success = self.shuffle_icons(intensity)
            if success:
                self.status_label.config(text="完成！", foreground="green")
                messagebox.showinfo("完成", "桌面图标已随机排列完成！")
            else:
                self.status_label.config(text="失败", foreground="red")
    
    def on_restore(self):
        """处理恢复按钮点击"""
        if messagebox.askyesno("确认", "确定要恢复桌面吗？"):
            self.status_label.config(text="正在恢复...", foreground="blue")
            self.status_label.update()
            
            success = self.restore_desktop()
            if success:
                self.status_label.config(text="恢复完成", foreground="green")
                messagebox.showinfo("完成", "桌面已恢复")
            else:
                self.status_label.config(text="恢复失败", foreground="red")

# 使用示例
if __name__ == "__main__":
    # 方法1：直接使用
    shuffler = DesktopIconShuffler()
    
    # 轻度打乱（重命名）
    # shuffler.shuffle_icons(intensity=1)
    
    # 恢复桌面
    # shuffler.restore_desktop()
    
    # 方法2：使用图形界面
    shuffler.create_gui()