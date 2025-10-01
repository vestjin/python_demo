#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: vestjin

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from faker import Faker
import pandas as pd
import json
from datetime import datetime
import threading

class FakerDataGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("虚假数据生成器 - Faker Data Generator")
        self.root.geometry("900x700")
        
        # 初始化Faker，支持中文
        self.fake_zh = Faker('zh_CN')
        self.fake_en = Faker('en_US')
        
        # 数据类型选项
        self.data_types = {
            "姓名": "name",
            "地址": "address",
            "邮箱": "email",
            "电话": "phone_number",
            "公司": "company",
            "职位": "job",
            "身份证号": "ssn",
            "信用卡号": "credit_card_number",
            "银行账号": "iban",
            "日期": "date",
            "时间": "time",
            "日期时间": "date_time",
            "URL": "url",
            "IPv4地址": "ipv4",
            "用户名": "user_name",
            "密码": "password",
            "文本": "text",
            "段落": "paragraph",
            "邮编": "postcode",
            "城市": "city",
            "省份": "province",
            "国家": "country"
        }
        
        self.selected_fields = {}
        self.create_widgets()
        
    def create_widgets(self):
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 语言选择
        lang_frame = ttk.LabelFrame(main_frame, text="语言设置", padding="5")
        lang_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        self.language_var = tk.StringVar(value="zh_CN")
        ttk.Radiobutton(lang_frame, text="中文", variable=self.language_var, 
                       value="zh_CN").pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(lang_frame, text="English", variable=self.language_var, 
                       value="en_US").pack(side=tk.LEFT, padx=10)
        
        # 字段选择区域
        field_frame = ttk.LabelFrame(main_frame, text="选择数据字段", padding="5")
        field_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        # 创建滚动区域
        canvas = tk.Canvas(field_frame, height=250)
        scrollbar = ttk.Scrollbar(field_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # 添加字段复选框
        self.field_vars = {}
        row = 0
        col = 0
        for display_name, field_type in self.data_types.items():
            var = tk.BooleanVar()
            self.field_vars[field_type] = {"var": var, "display": display_name}
            ttk.Checkbutton(scrollable_frame, text=display_name, 
                          variable=var).grid(row=row, column=col, sticky=tk.W, padx=5, pady=2)
            col += 1
            if col > 3:
                col = 0
                row += 1
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # 生成数量设置
        count_frame = ttk.LabelFrame(main_frame, text="生成设置", padding="5")
        count_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N), pady=5, padx=5)
        
        ttk.Label(count_frame, text="生成数量:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.count_var = tk.StringVar(value="100")
        count_entry = ttk.Entry(count_frame, textvariable=self.count_var, width=15)
        count_entry.grid(row=0, column=1, pady=5)
        
        ttk.Label(count_frame, text="导出格式:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.format_var = tk.StringVar(value="csv")
        formats = ["csv", "excel", "json", "html"]
        format_combo = ttk.Combobox(count_frame, textvariable=self.format_var, 
                                   values=formats, state="readonly", width=12)
        format_combo.grid(row=1, column=1, pady=5)
        
        # 按钮区域
        button_frame = ttk.Frame(count_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="生成数据", 
                  command=self.generate_data).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="导出文件", 
                  command=self.export_data).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="清空", 
                  command=self.clear_data).pack(side=tk.LEFT, padx=5)
        
        # 进度条
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # 预览区域
        preview_frame = ttk.LabelFrame(main_frame, text="数据预览", padding="5")
        preview_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        # 创建表格
        self.tree = ttk.Treeview(preview_frame, show='headings', height=15)
        vsb = ttk.Scrollbar(preview_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(preview_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        vsb.grid(row=0, column=1, sticky=(tk.N, tk.S))
        hsb.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        preview_frame.columnconfigure(0, weight=1)
        preview_frame.rowconfigure(0, weight=1)
        
        # 状态栏
        self.status_var = tk.StringVar(value="就绪")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, 
                              relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # 配置权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=3)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
        self.generated_data = None
        
    def generate_data(self):
        try:
            count = int(self.count_var.get())
            if count <= 0 or count > 100000:
                messagebox.showerror("错误", "请输入1-100000之间的数量")
                return
        except ValueError:
            messagebox.showerror("错误", "请输入有效的数字")
            return
        
        # 获取选中的字段
        selected = [field for field, data in self.field_vars.items() if data["var"].get()]
        
        if not selected:
            messagebox.showwarning("警告", "请至少选择一个字段")
            return
        
        # 在新线程中生成数据
        thread = threading.Thread(target=self._generate_data_thread, args=(count, selected))
        thread.daemon = True
        thread.start()
        
    def _generate_data_thread(self, count, selected):
        self.progress.start()
        self.status_var.set(f"正在生成 {count} 条数据...")
        
        # 选择语言
        fake = self.fake_zh if self.language_var.get() == "zh_CN" else self.fake_en
        
        data = []
        for _ in range(count):
            row = {}
            for field in selected:
                try:
                    display_name = self.field_vars[field]["display"]
                    if field == "name":
                        row[display_name] = fake.name()
                    elif field == "address":
                        row[display_name] = fake.address()
                    elif field == "email":
                        row[display_name] = fake.email()
                    elif field == "phone_number":
                        row[display_name] = fake.phone_number()
                    elif field == "company":
                        row[display_name] = fake.company()
                    elif field == "job":
                        row[display_name] = fake.job()
                    elif field == "ssn":
                        row[display_name] = fake.ssn()
                    elif field == "credit_card_number":
                        row[display_name] = fake.credit_card_number()
                    elif field == "iban":
                        row[display_name] = fake.iban()
                    elif field == "date":
                        row[display_name] = str(fake.date())
                    elif field == "time":
                        row[display_name] = str(fake.time())
                    elif field == "date_time":
                        row[display_name] = str(fake.date_time())
                    elif field == "url":
                        row[display_name] = fake.url()
                    elif field == "ipv4":
                        row[display_name] = fake.ipv4()
                    elif field == "user_name":
                        row[display_name] = fake.user_name()
                    elif field == "password":
                        row[display_name] = fake.password()
                    elif field == "text":
                        row[display_name] = fake.text(max_nb_chars=50)
                    elif field == "paragraph":
                        row[display_name] = fake.paragraph()
                    elif field == "postcode":
                        row[display_name] = fake.postcode()
                    elif field == "city":
                        row[display_name] = fake.city()
                    elif field == "province":
                        row[display_name] = fake.province() if hasattr(fake, 'province') else fake.state()
                    elif field == "country":
                        row[display_name] = fake.country()
                except Exception as e:
                    row[display_name] = "N/A"
            data.append(row)
        
        self.generated_data = pd.DataFrame(data)
        
        # 更新UI（在主线程中）
        self.root.after(0, self._update_preview)
        self.progress.stop()
        self.status_var.set(f"成功生成 {count} 条数据")
        
    def _update_preview(self):
        # 清空现有数据
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        if self.generated_data is not None:
            # 设置列
            self.tree['columns'] = list(self.generated_data.columns)
            
            for col in self.generated_data.columns:
                self.tree.heading(col, text=col)
                self.tree.column(col, width=150)
            
            # 插入数据（只显示前100行）
            for idx, row in self.generated_data.head(100).iterrows():
                values = [str(val)[:50] for val in row.values]  # 限制显示长度
                self.tree.insert('', 'end', values=values)
    
    def export_data(self):
        if self.generated_data is None:
            messagebox.showwarning("警告", "请先生成数据")
            return
        
        file_format = self.format_var.get()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if file_format == "csv":
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                initialfile=f"fake_data_{timestamp}.csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
            )
            if filename:
                self.generated_data.to_csv(filename, index=False, encoding='utf-8-sig')
                messagebox.showinfo("成功", f"已导出到: {filename}")
                
        elif file_format == "excel":
            filename = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                initialfile=f"fake_data_{timestamp}.xlsx",
                filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
            )
            if filename:
                self.generated_data.to_excel(filename, index=False, engine='openpyxl')
                messagebox.showinfo("成功", f"已导出到: {filename}")
                
        elif file_format == "json":
            filename = filedialog.asksaveasfilename(
                defaultextension=".json",
                initialfile=f"fake_data_{timestamp}.json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            if filename:
                self.generated_data.to_json(filename, orient='records', 
                                           force_ascii=False, indent=2)
                messagebox.showinfo("成功", f"已导出到: {filename}")
                
        elif file_format == "html":
            filename = filedialog.asksaveasfilename(
                defaultextension=".html",
                initialfile=f"fake_data_{timestamp}.html",
                filetypes=[("HTML files", "*.html"), ("All files", "*.*")]
            )
            if filename:
                self.generated_data.to_html(filename, index=False)
                messagebox.showinfo("成功", f"已导出到: {filename}")
    
    def clear_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.generated_data = None
        self.status_var.set("已清空数据")

if __name__ == "__main__":
    root = tk.Tk()
    app = FakerDataGenerator(root)
    root.mainloop()