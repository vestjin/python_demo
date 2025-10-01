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
import random

class FakerDataGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("虚假数据生成器 Pro - Faker Data Generator Pro")
        self.root.geometry("1000x750")
        
        # 初始化Faker，支持多语言
        self.fake_zh = Faker('zh_CN')
        self.fake_en = Faker('en_US')
        
        # 扩展的数据类型选项 - 按类别组织
        self.data_categories = {
            "个人信息": {
                "姓名": "name",
                "性别": "gender",
                "年龄": "age",
                "生日": "date_of_birth",
                "身份证号": "ssn",
                "血型": "blood_type",
            },
            "联系方式": {
                "邮箱": "email",
                "手机号": "phone_number",
                "座机号": "landline",
                "QQ号": "qq_number",
                "微信号": "wechat_id",
            },
            "地址信息": {
                "完整地址": "address",
                "国家": "country",
                "省份": "province",
                "城市": "city",
                "区县": "district",
                "街道": "street_address",
                "邮编": "postcode",
                "经纬度": "coordinates",
            },
            "公司职业": {
                "公司名称": "company",
                "公司后缀": "company_suffix",
                "职位": "job",
                "部门": "department",
                "工号": "employee_id",
                "工作年限": "work_years",
            },
            "金融信息": {
                "信用卡号": "credit_card_number",
                "信用卡类型": "credit_card_provider",
                "信用卡过期日": "credit_card_expire",
                "CVV码": "credit_card_security_code",
                "银行账号": "iban",
                "货币代码": "currency_code",
                "金额": "random_amount",
            },
            "网络信息": {
                "用户名": "user_name",
                "密码": "password",
                "强密码": "strong_password",
                "URL网址": "url",
                "域名": "domain_name",
                "IPv4地址": "ipv4",
                "IPv6地址": "ipv6",
                "MAC地址": "mac_address",
                "User Agent": "user_agent",
            },
            "时间日期": {
                "日期": "date",
                "时间": "time",
                "日期时间": "date_time",
                "年份": "year",
                "月份": "month_name",
                "星期": "day_of_week",
                "时间戳": "unix_time",
            },
            "文本内容": {
                "短文本": "text",
                "段落": "paragraph",
                "句子": "sentence",
                "单词": "word",
                "标题": "catch_phrase",
                "描述": "bs",
            },
            "商品信息": {
                "商品名称": "product_name",
                "商品类别": "product_category",
                "商品价格": "product_price",
                "SKU编号": "sku",
                "条形码": "ean",
            },
            "教育信息": {
                "学校名称": "school_name",
                "专业": "major",
                "学历": "education_level",
                "毕业年份": "graduation_year",
                "GPA": "gpa",
            },
            "其他": {
                "颜色": "color",
                "车牌号": "license_plate",
                "ISBN": "isbn13",
                "UUID": "uuid4",
                "文件名": "file_name",
                "MIME类型": "mime_type",
            }
        }
        
        self.selected_fields = {}
        self.create_widgets()
        
    def create_widgets(self):
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 顶部控制区
        top_frame = ttk.Frame(main_frame)
        top_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # 语言选择
        lang_frame = ttk.LabelFrame(top_frame, text="语言设置", padding="5")
        lang_frame.pack(side=tk.LEFT, padx=5)
        
        self.language_var = tk.StringVar(value="zh_CN")
        ttk.Radiobutton(lang_frame, text="中文", variable=self.language_var, 
                       value="zh_CN").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(lang_frame, text="English", variable=self.language_var, 
                       value="en_US").pack(side=tk.LEFT, padx=5)
        
        # 快捷选择
        quick_frame = ttk.LabelFrame(top_frame, text="快捷选择", padding="5")
        quick_frame.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(quick_frame, text="全选", width=8,
                  command=self.select_all).pack(side=tk.LEFT, padx=2)
        ttk.Button(quick_frame, text="取消全选", width=8,
                  command=self.deselect_all).pack(side=tk.LEFT, padx=2)
        ttk.Button(quick_frame, text="反选", width=8,
                  command=self.invert_selection).pack(side=tk.LEFT, padx=2)
        
        # 字段选择区域（使用Notebook分类）
        field_frame = ttk.LabelFrame(main_frame, text="选择数据字段", padding="5")
        field_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        # 创建Notebook
        self.notebook = ttk.Notebook(field_frame)
        self.notebook.pack(fill="both", expand=True)
        
        # 为每个类别创建标签页
        self.field_vars = {}
        for category_name, fields in self.data_categories.items():
            tab = ttk.Frame(self.notebook)
            self.notebook.add(tab, text=category_name)
            
            # 创建滚动区域
            canvas = tk.Canvas(tab, height=250)
            scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
            scrollable_frame = ttk.Frame(canvas)
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            # 添加字段复选框
            row = 0
            col = 0
            for display_name, field_type in fields.items():
                var = tk.BooleanVar()
                self.field_vars[field_type] = {"var": var, "display": display_name, "category": category_name}
                ttk.Checkbutton(scrollable_frame, text=display_name, 
                              variable=var).grid(row=row, column=col, sticky=tk.W, padx=10, pady=3)
                col += 1
                if col > 3:
                    col = 0
                    row += 1
            
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
        
        # 右侧设置区域
        settings_frame = ttk.LabelFrame(main_frame, text="生成设置", padding="10")
        settings_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N), pady=5, padx=5)
        
        # 生成数量
        ttk.Label(settings_frame, text="生成数量:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.count_var = tk.StringVar(value="100")
        count_entry = ttk.Entry(settings_frame, textvariable=self.count_var, width=15)
        count_entry.grid(row=0, column=1, pady=5, padx=5)
        
        # 导出格式
        ttk.Label(settings_frame, text="导出格式:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.format_var = tk.StringVar(value="csv")
        formats = ["csv", "excel", "json", "html", "sql"]
        format_combo = ttk.Combobox(settings_frame, textvariable=self.format_var, 
                                   values=formats, state="readonly", width=12)
        format_combo.grid(row=1, column=1, pady=5, padx=5)
        
        # 唯一性选项
        self.unique_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(settings_frame, text="确保邮箱唯一", 
                       variable=self.unique_var).grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        # 自定义前缀
        ttk.Label(settings_frame, text="ID前缀:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.prefix_var = tk.StringVar(value="USER")
        ttk.Entry(settings_frame, textvariable=self.prefix_var, width=15).grid(row=3, column=1, pady=5, padx=5)
        
        # 按钮区域
        button_frame = ttk.Frame(settings_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=15)
        
        ttk.Button(button_frame, text="生成数据", width=12,
                  command=self.generate_data).pack(pady=3)
        ttk.Button(button_frame, text="导出文件", width=12,
                  command=self.export_data).pack(pady=3)
        ttk.Button(button_frame, text="清空数据", width=12,
                  command=self.clear_data).pack(pady=3)
        
        # 统计信息
        stats_frame = ttk.LabelFrame(settings_frame, text="统计信息", padding="5")
        stats_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        self.stats_var = tk.StringVar(value="字段: 0 | 数据: 0")
        ttk.Label(stats_frame, textvariable=self.stats_var, font=('Arial', 9)).pack()
        
        # 进度条
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # 预览区域
        preview_frame = ttk.LabelFrame(main_frame, text="数据预览 (最多显示100行)", padding="5")
        preview_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        # 创建表格
        self.tree = ttk.Treeview(preview_frame, show='headings', height=12)
        vsb = ttk.Scrollbar(preview_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(preview_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        vsb.grid(row=0, column=1, sticky=(tk.N, tk.S))
        hsb.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        preview_frame.columnconfigure(0, weight=1)
        preview_frame.rowconfigure(0, weight=1)
        
        # 状态栏
        self.status_var = tk.StringVar(value="就绪 - 请选择字段并生成数据")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, 
                              relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # 配置权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=3)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
        self.generated_data = None
        
    def select_all(self):
        for field_data in self.field_vars.values():
            field_data["var"].set(True)
        self.update_stats()
        
    def deselect_all(self):
        for field_data in self.field_vars.values():
            field_data["var"].set(False)
        self.update_stats()
        
    def invert_selection(self):
        for field_data in self.field_vars.values():
            field_data["var"].set(not field_data["var"].get())
        self.update_stats()
        
    def update_stats(self):
        selected_count = sum(1 for data in self.field_vars.values() if data["var"].get())
        data_count = len(self.generated_data) if self.generated_data is not None else 0
        self.stats_var.set(f"字段: {selected_count} | 数据: {data_count}")
        
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
        
        # 用于确保唯一性
        used_emails = set()
        
        data = []
        for i in range(count):
            row = {}
            for field in selected:
                try:
                    display_name = self.field_vars[field]["display"]
                    
                    # 基础字段
                    if field == "name":
                        row[display_name] = fake.name()
                    elif field == "gender":
                        row[display_name] = random.choice(["男", "女"]) if self.language_var.get() == "zh_CN" else random.choice(["Male", "Female"])
                    elif field == "age":
                        row[display_name] = random.randint(18, 65)
                    elif field == "date_of_birth":
                        row[display_name] = str(fake.date_of_birth(minimum_age=18, maximum_age=65))
                    elif field == "ssn":
                        row[display_name] = fake.ssn()
                    elif field == "blood_type":
                        row[display_name] = random.choice(["A", "B", "AB", "O"])
                    
                    # 联系方式
                    elif field == "email":
                        if self.unique_var.get():
                            email = fake.email()
                            while email in used_emails:
                                email = fake.email()
                            used_emails.add(email)
                            row[display_name] = email
                        else:
                            row[display_name] = fake.email()
                    elif field == "phone_number":
                        row[display_name] = fake.phone_number()
                    elif field == "landline":
                        row[display_name] = f"0{random.randint(10, 99)}-{random.randint(10000000, 99999999)}"
                    elif field == "qq_number":
                        row[display_name] = str(random.randint(100000, 9999999999))
                    elif field == "wechat_id":
                        row[display_name] = fake.user_name() + str(random.randint(100, 999))
                    
                    # 地址信息
                    elif field == "address":
                        row[display_name] = fake.address()
                    elif field == "country":
                        row[display_name] = fake.country()
                    elif field == "province":
                        row[display_name] = fake.province() if hasattr(fake, 'province') else fake.state()
                    elif field == "city":
                        row[display_name] = fake.city()
                    elif field == "district":
                        row[display_name] = fake.city_suffix()
                    elif field == "street_address":
                        row[display_name] = fake.street_address()
                    elif field == "postcode":
                        row[display_name] = fake.postcode()
                    elif field == "coordinates":
                        row[display_name] = f"{fake.latitude()}, {fake.longitude()}"
                    
                    # 公司职业
                    elif field == "company":
                        row[display_name] = fake.company()
                    elif field == "company_suffix":
                        row[display_name] = fake.company_suffix()
                    elif field == "job":
                        row[display_name] = fake.job()
                    elif field == "department":
                        departments = ["技术部", "市场部", "销售部", "人力资源部", "财务部"] if self.language_var.get() == "zh_CN" else ["Tech", "Marketing", "Sales", "HR", "Finance"]
                        row[display_name] = random.choice(departments)
                    elif field == "employee_id":
                        row[display_name] = f"{self.prefix_var.get()}{i+1:06d}"
                    elif field == "work_years":
                        row[display_name] = random.randint(0, 30)
                    
                    # 金融信息
                    elif field == "credit_card_number":
                        row[display_name] = fake.credit_card_number()
                    elif field == "credit_card_provider":
                        row[display_name] = fake.credit_card_provider()
                    elif field == "credit_card_expire":
                        row[display_name] = fake.credit_card_expire()
                    elif field == "credit_card_security_code":
                        row[display_name] = fake.credit_card_security_code()
                    elif field == "iban":
                        row[display_name] = fake.iban()
                    elif field == "currency_code":
                        row[display_name] = fake.currency_code()
                    elif field == "random_amount":
                        row[display_name] = f"{random.uniform(10, 10000):.2f}"
                    
                    # 网络信息
                    elif field == "user_name":
                        row[display_name] = fake.user_name()
                    elif field == "password":
                        row[display_name] = fake.password(length=10)
                    elif field == "strong_password":
                        row[display_name] = fake.password(length=16, special_chars=True, digits=True, upper_case=True, lower_case=True)
                    elif field == "url":
                        row[display_name] = fake.url()
                    elif field == "domain_name":
                        row[display_name] = fake.domain_name()
                    elif field == "ipv4":
                        row[display_name] = fake.ipv4()
                    elif field == "ipv6":
                        row[display_name] = fake.ipv6()
                    elif field == "mac_address":
                        row[display_name] = fake.mac_address()
                    elif field == "user_agent":
                        row[display_name] = fake.user_agent()
                    
                    # 时间日期
                    elif field == "date":
                        row[display_name] = str(fake.date())
                    elif field == "time":
                        row[display_name] = str(fake.time())
                    elif field == "date_time":
                        row[display_name] = str(fake.date_time())
                    elif field == "year":
                        row[display_name] = fake.year()
                    elif field == "month_name":
                        row[display_name] = fake.month_name()
                    elif field == "day_of_week":
                        row[display_name] = fake.day_of_week()
                    elif field == "unix_time":
                        row[display_name] = fake.unix_time()
                    
                    # 文本内容
                    elif field == "text":
                        row[display_name] = fake.text(max_nb_chars=50)
                    elif field == "paragraph":
                        row[display_name] = fake.paragraph()
                    elif field == "sentence":
                        row[display_name] = fake.sentence()
                    elif field == "word":
                        row[display_name] = fake.word()
                    elif field == "catch_phrase":
                        row[display_name] = fake.catch_phrase()
                    elif field == "bs":
                        row[display_name] = fake.bs()
                    
                    # 商品信息
                    elif field == "product_name":
                        row[display_name] = fake.catch_phrase()
                    elif field == "product_category":
                        categories = ["电子产品", "服装", "食品", "图书", "家居"] if self.language_var.get() == "zh_CN" else ["Electronics", "Clothing", "Food", "Books", "Home"]
                        row[display_name] = random.choice(categories)
                    elif field == "product_price":
                        row[display_name] = f"{random.uniform(10, 5000):.2f}"
                    elif field == "sku":
                        row[display_name] = f"SKU{random.randint(100000, 999999)}"
                    elif field == "ean":
                        row[display_name] = fake.ean13()
                    
                    # 教育信息
                    elif field == "school_name":
                        row[display_name] = fake.company() + ("大学" if self.language_var.get() == "zh_CN" else " University")
                    elif field == "major":
                        majors = ["计算机科学", "工商管理", "机械工程", "英语", "数学"] if self.language_var.get() == "zh_CN" else ["Computer Science", "Business", "Engineering", "English", "Mathematics"]
                        row[display_name] = random.choice(majors)
                    elif field == "education_level":
                        levels = ["本科", "硕士", "博士"] if self.language_var.get() == "zh_CN" else ["Bachelor", "Master", "PhD"]
                        row[display_name] = random.choice(levels)
                    elif field == "graduation_year":
                        row[display_name] = random.randint(2000, 2024)
                    elif field == "gpa":
                        row[display_name] = f"{random.uniform(2.5, 4.0):.2f}"
                    
                    # 其他
                    elif field == "color":
                        row[display_name] = fake.color_name()
                    elif field == "license_plate":
                        row[display_name] = fake.license_plate()
                    elif field == "isbn13":
                        row[display_name] = fake.isbn13()
                    elif field == "uuid4":
                        row[display_name] = str(fake.uuid4())
                    elif field == "file_name":
                        row[display_name] = fake.file_name()
                    elif field == "mime_type":
                        row[display_name] = fake.mime_type()
                    
                except Exception as e:
                    row[display_name] = "N/A"
            data.append(row)
        
        self.generated_data = pd.DataFrame(data)
        
        # 更新UI（在主线程中）
        self.root.after(0, self._update_preview)
        self.root.after(0, self.update_stats)
        self.progress.stop()
        self.status_var.set(f"✓ 成功生成 {count} 条数据，包含 {len(selected)} 个字段")
        
    def _update_preview(self):
        # 清空现有数据
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        if self.generated_data is not None:
            # 设置列
            self.tree['columns'] = list(self.generated_data.columns)
            
            for col in self.generated_data.columns:
                self.tree.heading(col, text=col)
                self.tree.column(col, width=120)
            
            # 插入数据（只显示前100行）
            for idx, row in self.generated_data.head(100).iterrows():
                values = [str(val)[:50] for val in row.values]
                self.tree.insert('', 'end', values=values)
    
    def export_data(self):
        if self.generated_data is None:
            messagebox.showwarning("警告", "请先生成数据")
            return
        
        file_format = self.format_var.get()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        try:
            if file_format == "csv":
                filename = filedialog.asksaveasfilename(
                    defaultextension=".csv",
                    initialfile=f"fake_data_{timestamp}.csv",
                    filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
                )
                if filename:
                    self.generated_data.to_csv(filename, index=False, encoding='utf-8-sig')
                    messagebox.showinfo("成功", f"已导出 {len(self.generated_data)} 条数据到:\n{filename}")
                    
            elif file_format == "excel":
                filename = filedialog.asksaveasfilename(
                    defaultextension=".xlsx",
                    initialfile=f"fake_data_{timestamp}.xlsx",
                    filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
                )
                if filename:
                    self.generated_data.to_excel(filename, index=False, engine='openpyxl')
                    messagebox.showinfo("成功", f"已导出 {len(self.generated_data)} 条数据到:\n{filename}")
                    
            elif file_format == "json":
                filename = filedialog.asksaveasfilename(
                    defaultextension=".json",
                    initialfile=f"fake_data_{timestamp}.json",
                    filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
                )
                if filename:
                    self.generated_data.to_json(filename, orient='records', 
                                               force_ascii=False, indent=2)
                    messagebox.showinfo("成功", f"已导出 {len(self.generated_data)} 条数据到:\n{filename}")
                    
            elif file_format == "html":
                filename = filedialog.asksaveasfilename(
                    defaultextension=".html",
                    initialfile=f"fake_data_{timestamp}.html",
                    filetypes=[("HTML files", "*.html"), ("All files", "*.*")]
                )
                if filename:
                    self.generated_data.to_html(filename, index=False)
                    messagebox.showinfo("成功", f"已导出 {len(self.generated_data)} 条数据到:\n{filename}")
                    
            elif file_format == "sql":
                filename = filedialog.asksaveasfilename(
                    defaultextension=".sql",
                    initialfile=f"fake_data_{timestamp}.sql",
                    filetypes=[("SQL files", "*.sql"), ("All files", "*.*")]
                )
                if filename:
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(f"-- Generated on {datetime.now()}\n")
                        f.write(f"-- Total records: {len(self.generated_data)}\n\n")
                        f.write("CREATE TABLE IF NOT EXISTS fake_data (\n")
                        f.write("    id INT PRIMARY KEY AUTO_INCREMENT,\n")
                        
                        for col in self.generated_data.columns:
                            f.write(f"    `{col}` VARCHAR(255),\n")
                        
                        f.write("    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP\n")
                        f.write(");\n\n")
                        
                        for idx, row in self.generated_data.iterrows():
                            values = []
                            for val in row.values:
                                if pd.isna(val):
                                    values.append("NULL")
                                else:
                                    # 转义单引号
                                    escaped_val = str(val).replace("'", "''")
                                    values.append(f"'{escaped_val}'")
                            
                            columns = "`, `".join(self.generated_data.columns)
                            values_str = ", ".join(values)
                            f.write(f"INSERT INTO fake_data (`{columns}`) VALUES ({values_str});\n")
                    
                    messagebox.showinfo("成功", f"已导出 {len(self.generated_data)} 条数据到:\n{filename}")
        
        except Exception as e:
            messagebox.showerror("错误", f"导出失败: {str(e)}")
    
    def clear_data(self):
        if self.generated_data is not None:
            result = messagebox.askyesno("确认", "确定要清空所有数据吗？")
            if result:
                for item in self.tree.get_children():
                    self.tree.delete(item)
                self.generated_data = None
                self.update_stats()
                self.status_var.set("已清空数据")
        else:
            self.status_var.set("没有数据需要清空")

if __name__ == "__main__":
    root = tk.Tk()
    app = FakerDataGenerator(root)
    root.mainloop()