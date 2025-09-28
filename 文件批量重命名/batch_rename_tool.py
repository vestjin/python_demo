#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: vestjin
"""
批量文件重命名工具
支持拖拽、预览、冲突检测、筛选等功能
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import re
import sys
from pathlib import Path
import string
from collections import Counter

class FileRenameApp:
    def __init__(self, root):
        self.root = root
        self.root.title("批量文件重命名工具 v1.0")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)
        
        # 数据存储
        self.files_data = []  # 存储文件信息
        self.filtered_data = []  # 筛选后的数据
        
        # 创建界面
        self.setup_ui()
        
        # 绑定拖拽事件
        self.setup_drag_drop()
        
    def setup_ui(self):
        """设置用户界面"""
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # 1. 文件选择区域
        file_frame = ttk.LabelFrame(main_frame, text="文件选择", padding="5")
        file_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 5))
        file_frame.columnconfigure(1, weight=1)
        
        ttk.Button(file_frame, text="选择文件", command=self.select_files).grid(row=0, column=0, padx=(0, 5))
        ttk.Button(file_frame, text="选择文件夹", command=self.select_folder).grid(row=0, column=1, padx=5)
        ttk.Button(file_frame, text="清空列表", command=self.clear_files).grid(row=0, column=2, padx=(5, 0))
        ttk.Button(file_frame, text="📖 使用说明", command=self.show_help).grid(row=0, column=3, padx=(5, 0))
        
        # 拖拽提示
        drag_label = ttk.Label(file_frame, text="💡 提示：可直接拖拽文件或文件夹到窗口中", foreground="blue")
        drag_label.grid(row=1, column=0, columnspan=3, pady=(5, 0))
        
        # 2. 筛选区域
        filter_frame = ttk.LabelFrame(main_frame, text="筛选选项", padding="5")
        filter_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # 扩展名筛选
        ttk.Label(filter_frame, text="扩展名:").grid(row=0, column=0, sticky=tk.W)
        self.ext_filter = ttk.Combobox(filter_frame, width=15)
        self.ext_filter.grid(row=0, column=1, padx=(5, 10), sticky=tk.W)
        self.ext_filter.bind('<<ComboboxSelected>>', self.apply_filter)
        
        # 文件类型筛选
        ttk.Label(filter_frame, text="类型:").grid(row=0, column=2, sticky=tk.W)
        self.type_filter = ttk.Combobox(filter_frame, values=["全部", "文件", "文件夹"], width=10)
        self.type_filter.set("全部")
        self.type_filter.grid(row=0, column=3, padx=(5, 10), sticky=tk.W)
        self.type_filter.bind('<<ComboboxSelected>>', self.apply_filter)
        
        ttk.Button(filter_frame, text="重置筛选", command=self.reset_filter).grid(row=0, column=4, padx=5)
        
        # 3. 重命名规则区域
        rename_frame = ttk.LabelFrame(main_frame, text="重命名规则", padding="5")
        rename_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        rename_frame.rowconfigure(4, weight=1)
        
        # 重命名模式选择
        self.rename_mode = tk.StringVar(value="replace")
        ttk.Radiobutton(rename_frame, text="查找替换", variable=self.rename_mode, 
                       value="replace", command=self.update_preview).grid(row=0, column=0, sticky=tk.W)
        ttk.Radiobutton(rename_frame, text="添加前缀", variable=self.rename_mode, 
                       value="prefix", command=self.update_preview).grid(row=1, column=0, sticky=tk.W)
        ttk.Radiobutton(rename_frame, text="添加后缀", variable=self.rename_mode, 
                       value="suffix", command=self.update_preview).grid(row=2, column=0, sticky=tk.W)
        ttk.Radiobutton(rename_frame, text="序号重命名", variable=self.rename_mode, 
                       value="number", command=self.update_preview).grid(row=3, column=0, sticky=tk.W)
        
        # 参数输入区域
        params_frame = ttk.Frame(rename_frame)
        params_frame.grid(row=4, column=0, sticky=(tk.W, tk.E, tk.N), pady=(10, 0))
        params_frame.columnconfigure(1, weight=1)
        
        # 查找文本
        ttk.Label(params_frame, text="查找:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.find_text = ttk.Entry(params_frame)
        self.find_text.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(5, 0), pady=2)
        self.find_text.bind('<KeyRelease>', self.update_preview)
        
        # 替换文本
        ttk.Label(params_frame, text="替换:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.replace_text = ttk.Entry(params_frame)
        self.replace_text.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(5, 0), pady=2)
        self.replace_text.bind('<KeyRelease>', self.update_preview)
        
        # 前缀/后缀文本
        ttk.Label(params_frame, text="文本:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.prefix_suffix_text = ttk.Entry(params_frame)
        self.prefix_suffix_text.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=(5, 0), pady=2)
        self.prefix_suffix_text.bind('<KeyRelease>', self.update_preview)
        
        # 序号设置
        number_frame = ttk.Frame(params_frame)
        number_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=2)
        number_frame.columnconfigure(1, weight=1)
        
        ttk.Label(number_frame, text="基础名:").grid(row=0, column=0, sticky=tk.W)
        self.base_name = ttk.Entry(number_frame, width=15)
        self.base_name.insert(0,"文件")
        self.base_name.grid(row=0, column=1, sticky=tk.W, padx=(5, 10))
        self.base_name.bind('<KeyRelease>', self.update_preview)
        
        ttk.Label(number_frame, text="起始序号:").grid(row=0, column=2, sticky=tk.W)
        self.start_number = ttk.Spinbox(number_frame, from_=1, to=999, width=8, value=1)
        self.start_number.grid(row=0, column=3, sticky=tk.W, padx=(5, 10))
        self.start_number.bind('<KeyRelease>', self.update_preview)
        
        ttk.Label(number_frame, text="位数:").grid(row=0, column=4, sticky=tk.W)
        self.number_digits = ttk.Spinbox(number_frame, from_=1, to=6, width=5, value=3)
        self.number_digits.grid(row=0, column=5, sticky=tk.W, padx=(5, 0))
        self.number_digits.bind('<KeyRelease>', self.update_preview)
        
        # 执行按钮
        ttk.Button(rename_frame, text="🔄 预览更改", command=self.update_preview).grid(row=5, column=0, pady=(10, 5))
        self.execute_btn = ttk.Button(rename_frame, text="✅ 执行重命名", command=self.execute_rename)
        self.execute_btn.grid(row=6, column=0, pady=5)
        self.execute_btn.state(['disabled'])
        
        # 4. 文件列表区域
        list_frame = ttk.LabelFrame(main_frame, text="文件列表", padding="5")
        list_frame.grid(row=2, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        # 创建Treeview
        columns = ("原名称", "新名称", "状态")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="tree headings", height=15)
        
        # 配置列
        self.tree.heading("#0", text="类型")
        self.tree.column("#0", width=50, minwidth=50)
        
        for col in columns:
            self.tree.heading(col, text=col)
            if col == "状态":
                self.tree.column(col, width=80, minwidth=80)
            else:
                self.tree.column(col, width=200, minwidth=150)
        
        # 添加滚动条
        v_scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(list_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # 网格布局
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        v_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        h_scrollbar.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # 配置标签颜色
        self.tree.tag_configure("conflict", background="#ffcccc")  # 冲突 - 红色
        self.tree.tag_configure("invalid", background="#ffcc99")   # 无效 - 橙色
        self.tree.tag_configure("valid", background="#ccffcc")     # 有效 - 绿色
        self.tree.tag_configure("unchanged", background="#f0f0f0") # 未更改 - 灰色
        
    def setup_drag_drop(self):
        """设置拖拽功能"""
        def drop(event):
            files = self.root.tk.splitlist(event.data)
            self.add_files(files)
            
        def drag_enter(event):
            event.widget.focus_force()
            return event.action
            
        try:
            from tkinter import dnd
            # 注册拖拽事件
            self.root.drop_target_register(dnd.DND_FILES)
            self.root.dnd_bind('<<Drop>>', drop)
            self.root.dnd_bind('<<DragEnter>>', drag_enter)
        except:
            # 如果没有dnd支持，使用替代方法
            self.root.bind('<Button-1>', self.on_click)
    
    def on_click(self, event):
        """处理点击事件（拖拽替代）"""
        pass
    
    def select_files(self):
        """选择文件"""
        files = filedialog.askopenfilenames(title="选择要重命名的文件")
        if files:
            self.add_files(files)
    
    def select_folder(self):
        """选择文件夹"""
        folder = filedialog.askdirectory(title="选择包含要重命名文件的文件夹")
        if folder:
            files = []
            for item in os.listdir(folder):
                files.append(os.path.join(folder, item))
            self.add_files(files)
    
    def add_files(self, file_paths):
        """添加文件到列表"""
        new_files = 0
        for file_path in file_paths:
            path_obj = Path(file_path)
            if path_obj.exists():
                # 检查是否已存在
                if not any(item['path'] == str(path_obj) for item in self.files_data):
                    file_info = {
                        'path': str(path_obj),
                        'name': path_obj.name,
                        'is_dir': path_obj.is_dir(),
                        'extension': path_obj.suffix.lower() if not path_obj.is_dir() else '',
                        'new_name': path_obj.name,
                        'status': '未更改'
                    }
                    self.files_data.append(file_info)
                    new_files += 1
        
        if new_files > 0:
            self.update_filter_options()
            self.apply_filter()
            messagebox.showinfo("添加完成", f"成功添加 {new_files} 个项目")
        else:
            messagebox.showwarning("提示", "没有找到新的有效文件")
    
    def clear_files(self):
        """清空文件列表"""
        self.files_data.clear()
        self.filtered_data.clear()
        self.tree.delete(*self.tree.get_children())
        self.ext_filter['values'] = []
        self.ext_filter.set('')
        self.execute_btn.state(['disabled'])
    
    def update_filter_options(self):
        """更新筛选选项"""
        extensions = set()
        for item in self.files_data:
            if item['extension']:
                extensions.add(item['extension'])
        
        ext_list = ['全部'] + sorted(list(extensions))
        self.ext_filter['values'] = ext_list
        if not self.ext_filter.get():
            self.ext_filter.set('全部')
    
    def apply_filter(self, event=None):
        """应用筛选"""
        ext_filter = self.ext_filter.get()
        type_filter = self.type_filter.get()
        
        self.filtered_data = []
        for item in self.files_data:
            # 扩展名筛选
            if ext_filter and ext_filter != '全部':
                if item['extension'] != ext_filter:
                    continue
            
            # 类型筛选
            if type_filter == '文件' and item['is_dir']:
                continue
            elif type_filter == '文件夹' and not item['is_dir']:
                continue
            
            self.filtered_data.append(item)
        
        self.update_tree_display()
        self.update_preview()
    
    def reset_filter(self):
        """重置筛选"""
        self.ext_filter.set('全部')
        self.type_filter.set('全部')
        self.apply_filter()
    
    def update_preview(self, event=None):
        """更新预览"""
        if not self.filtered_data:
            return
        
        mode = self.rename_mode.get()
        
        # 生成新名称
        for item in self.filtered_data:
            original_name = item['name']
            name_without_ext = Path(original_name).stem
            extension = Path(original_name).suffix
            
            if mode == "replace":
                find_text = self.find_text.get()
                replace_text = self.replace_text.get()
                if find_text:
                    new_name_without_ext = name_without_ext.replace(find_text, replace_text)
                    item['new_name'] = new_name_without_ext + extension
                else:
                    item['new_name'] = original_name
            
            elif mode == "prefix":
                prefix = self.prefix_suffix_text.get()
                item['new_name'] = prefix + original_name
            
            elif mode == "suffix":
                suffix = self.prefix_suffix_text.get()
                item['new_name'] = name_without_ext + suffix + extension
            
            elif mode == "number":
                base_name = self.base_name.get()
                start_num = int(self.start_number.get())
                digits = int(self.number_digits.get())
                index = self.filtered_data.index(item)
                number = str(start_num + index).zfill(digits)
                item['new_name'] = f"{base_name}{number}{extension}"
        
        # 检查冲突和有效性
        self.check_conflicts_and_validity()
        self.update_tree_display()
        
        # 检查是否可以执行
        can_execute = any(item['status'] == '有效' for item in self.filtered_data)
        if can_execute:
            self.execute_btn.state(['!disabled'])
        else:
            self.execute_btn.state(['disabled'])
    
    def check_conflicts_and_validity(self):
        """检查冲突和有效性"""
        # 收集所有新名称
        new_names = [item['new_name'] for item in self.filtered_data]
        name_counts = Counter(new_names)
        
        # 获取目录中已存在的文件
        existing_files = set()
        if self.filtered_data:
            parent_dir = Path(self.filtered_data[0]['path']).parent
            try:
                existing_files = set(os.listdir(parent_dir))
            except:
                pass
        
        for item in self.filtered_data:
            new_name = item['new_name']
            original_name = item['name']
            
            # 检查是否有更改
            if new_name == original_name:
                item['status'] = '未更改'
                continue
            
            # 检查非法字符
            invalid_chars = '<>:"/\\|?*'
            if any(char in new_name for char in invalid_chars):
                item['status'] = '非法字符'
                continue
            
            # 检查空名称
            if not new_name.strip():
                item['status'] = '名称为空'
                continue
            
            # 检查重复
            if name_counts[new_name] > 1:
                item['status'] = '名称冲突'
                continue
            
            # 检查与现有文件冲突（排除自身）
            if new_name in existing_files and new_name != original_name:
                item['status'] = '文件已存在'
                continue
            
            # 有效
            item['status'] = '有效'
    
    def update_tree_display(self):
        """更新树形显示"""
        # 清空现有内容
        self.tree.delete(*self.tree.get_children())
        
        # 添加筛选后的数据
        for item in self.filtered_data:
            # 确定图标和标签
            icon = "📁" if item['is_dir'] else "📄"
            
            # 确定标签（用于颜色）
            tag = ""
            if item['status'] == '有效':
                tag = "valid"
            elif item['status'] == '未更改':
                tag = "unchanged"
            elif item['status'] in ['名称冲突', '文件已存在']:
                tag = "conflict"
            elif item['status'] in ['非法字符', '名称为空']:
                tag = "invalid"
            
            # 插入项目
            self.tree.insert("", "end", 
                           text=icon,
                           values=(item['name'], item['new_name'], item['status']),
                           tags=(tag,))
    
    def execute_rename(self):
        """执行重命名"""
        valid_items = [item for item in self.filtered_data if item['status'] == '有效']
        
        if not valid_items:
            messagebox.showwarning("警告", "没有可以重命名的文件")
            return
        
        # 确认对话框
        result = messagebox.askyesno("确认重命名", 
                                   f"确定要重命名 {len(valid_items)} 个项目吗？\n"
                                   f"此操作不可撤销！")
        if not result:
            return
        
        # 执行重命名
        success_count = 0
        error_count = 0
        error_messages = []
        
        for item in valid_items:
            try:
                old_path = Path(item['path'])
                new_path = old_path.parent / item['new_name']
                old_path.rename(new_path)
                
                # 更新数据
                item['path'] = str(new_path)
                item['name'] = item['new_name']
                item['status'] = '已重命名'
                success_count += 1
                
            except Exception as e:
                error_count += 1
                error_messages.append(f"{item['name']}: {str(e)}")
        
        # 显示结果
        if success_count > 0:
            self.update_tree_display()
        
        if error_count == 0:
            messagebox.showinfo("重命名完成", f"成功重命名 {success_count} 个项目")
        else:
            error_text = "\n".join(error_messages[:5])  # 只显示前5个错误
            if len(error_messages) > 5:
                error_text += f"\n... 还有 {len(error_messages)-5} 个错误"
            
            messagebox.showerror("重命名完成", 
                               f"成功: {success_count} 个\n"
                               f"失败: {error_count} 个\n\n"
                               f"错误详情:\n{error_text}")
        
        # 刷新数据
        self.refresh_data()
    
    def refresh_data(self):
        """刷新数据"""
        # 重新检查文件是否存在，更新路径等
        valid_items = []
        for item in self.files_data:
            path_obj = Path(item['path'])
            if path_obj.exists():
                item['name'] = path_obj.name
                valid_items.append(item)
        
        self.files_data = valid_items
        self.apply_filter()

    def show_help(self):
        """显示使用说明"""
        help_text = """
🎯 批量文件重命名工具 - 使用说明

📁 添加文件/文件夹：
  • 点击"选择文件"按钮选择多个文件
  • 点击"选择文件夹"按钮选择整个文件夹
  • 直接拖拽文件或文件夹到窗口中
  • 点击"清空列表"清除所有文件

🔍 筛选功能：
  • 扩展名筛选：只显示特定扩展名的文件（如 .txt, .jpg）
  • 类型筛选：选择只处理"文件"或"文件夹"
  • 点击"重置筛选"恢复显示所有文件

✏️ 重命名模式：
  1️⃣ 查找替换：在文件名中查找指定文本并替换
     - 查找：要查找的文本
     - 替换：要替换成的文本
  
  2️⃣ 添加前缀：在文件名前面添加文本
     - 文本：要添加的前缀内容
  
  3️⃣ 添加后缀：在文件名后面（扩展名前）添加文本
     - 文本：要添加的后缀内容
  
  4️⃣ 序号重命名：使用"基础名+序号"格式重命名
     - 基础名：新文件名的基础部分
     - 起始序号：序号从几开始
     - 位数：序号补零到几位数

🎨 状态颜色说明：
  🟢 绿色背景：可以安全重命名
  🔴 红色背景：名称冲突或文件已存在
  🟠 橙色背景：包含非法字符或名称为空
  ⚪ 灰色背景：名称未更改

⚠️ 注意事项：
  • 重命名操作不可撤销，请谨慎操作
  • 文件名不能包含 < > : " / \\ | ? * 字符
  • 确保有足够的磁盘权限进行重命名
  • 建议先备份重要文件

🚀 操作步骤：
  1. 添加要重命名的文件
  2. 设置筛选条件（可选）
  3. 选择重命名模式并填写参数
  4. 点击"预览更改"查看效果
  5. 确认无误后点击"执行重命名"
        """
        
        # 创建帮助窗口
        help_window = tk.Toplevel(self.root)
        help_window.title("使用说明")
        help_window.geometry("600x700")
        help_window.resizable(True, True)
        
        # 创建滚动文本框
        frame = ttk.Frame(help_window, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)
        
        text_widget = tk.Text(frame, wrap=tk.WORD, font=("Microsoft YaHei", 10))
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 插入帮助文本
        text_widget.insert("1.0", help_text)
        text_widget.config(state=tk.DISABLED)  # 设置为只读
        
        # 关闭按钮
        btn_frame = ttk.Frame(help_window)
        btn_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        ttk.Button(btn_frame, text="关闭", command=help_window.destroy).pack(side=tk.RIGHT)

def main():
    """主函数"""
    root = tk.Tk()
    
    # 设置窗口图标（如果有的话）
    try:
        # root.iconbitmap('icon.ico')  # 如果有图标文件
        pass
    except:
        pass
    
    app = FileRenameApp(root)
    
    # 运行应用
    try:
        root.mainloop()
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
