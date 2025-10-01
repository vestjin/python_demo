#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: vestjin

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
from faker import Faker
import pandas as pd
import json
import yaml
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import threading
import random
import re
import pickle
import gzip
from collections import Counter
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class FakerDataGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("虚假数据生成器 Pro Max - Faker Data Generator Pro Max")
        self.root.geometry("1200x800")
        
        # 初始化Faker
        self.fake_zh = Faker('zh_CN')
        self.fake_en = Faker('en_US')
        
        # 数据类型选项
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
        
        # 自定义字段规则
        self.custom_rules = {}
        
        # 数据关联配置
        self.enable_data_correlation = tk.BooleanVar(value=True)
        
        self.selected_fields = {}
        self.generated_data = None
        self.current_filter = None
        
        self.create_widgets()
        
    def create_widgets(self):
        # 创建菜单栏
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # 文件菜单
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="文件", menu=file_menu)
        file_menu.add_command(label="保存配置模板", command=self.save_template)
        file_menu.add_command(label="加载配置模板", command=self.load_template)
        file_menu.add_separator()
        file_menu.add_command(label="退出", command=self.root.quit)
        
        # 数据菜单
        data_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="数据", menu=data_menu)
        data_menu.add_command(label="增量生成（追加）", command=self.incremental_generate)
        data_menu.add_command(label="批量生成多组数据", command=self.batch_generate)
        data_menu.add_command(label="数据验证", command=self.validate_data)
        data_menu.add_separator()
        data_menu.add_command(label="数据统计分析", command=self.show_statistics)
        
        # 工具菜单
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="工具", menu=tools_menu)
        tools_menu.add_command(label="自定义字段规则", command=self.custom_field_rules)
        tools_menu.add_command(label="数据库连接设置", command=self.database_settings)

        # 帮助菜单
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="帮助",menu=help_menu)
        help_menu.add_command(label="使用说明", command=self.show_help)
        help_menu.add_command(label="快速入门", command=self.quick_start_guide)
        help_menu.add_separator()
        help_menu.add_command(label="关于", command=self.show_about)
        
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
        
        # 数据关联选项
        correlation_frame = ttk.LabelFrame(top_frame, text="高级选项", padding="5")
        correlation_frame.pack(side=tk.LEFT, padx=5)
        ttk.Checkbutton(correlation_frame, text="启用数据关联性", 
                       variable=self.enable_data_correlation).pack(side=tk.LEFT, padx=5)
        
        # 快捷选择
        quick_frame = ttk.LabelFrame(top_frame, text="快捷选择", padding="5")
        quick_frame.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(quick_frame, text="全选", width=8,
                  command=self.select_all).pack(side=tk.LEFT, padx=2)
        ttk.Button(quick_frame, text="取消", width=8,
                  command=self.deselect_all).pack(side=tk.LEFT, padx=2)
        ttk.Button(quick_frame, text="反选", width=8,
                  command=self.invert_selection).pack(side=tk.LEFT, padx=2)
        
        # 字段选择区域
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
            
            canvas = tk.Canvas(tab, height=200)
            scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
            scrollable_frame = ttk.Frame(canvas)
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
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
        formats = ["csv", "excel", "json", "html", "sql", "xml", "yaml", "parquet"]
        format_combo = ttk.Combobox(settings_frame, textvariable=self.format_var, 
                                   values=formats, state="readonly", width=12)
        format_combo.grid(row=1, column=1, pady=5, padx=5)
        
        # 唯一性选项
        self.unique_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(settings_frame, text="确保邮箱唯一", 
                       variable=self.unique_var).grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        # 压缩导出
        self.compress_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(settings_frame, text="压缩导出(gzip)", 
                       variable=self.compress_var).grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        # 自定义前缀
        ttk.Label(settings_frame, text="ID前缀:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.prefix_var = tk.StringVar(value="USER")
        ttk.Entry(settings_frame, textvariable=self.prefix_var, width=15).grid(row=4, column=1, pady=5, padx=5)
        
        # SQL表名
        ttk.Label(settings_frame, text="SQL表名:").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.table_name_var = tk.StringVar(value="fake_data")
        ttk.Entry(settings_frame, textvariable=self.table_name_var, width=15).grid(row=5, column=1, pady=5, padx=5)
        
        # 按钮区域
        button_frame = ttk.Frame(settings_frame)
        button_frame.grid(row=6, column=0, columnspan=2, pady=15)
        
        ttk.Button(button_frame, text="生成数据", width=12,
                  command=self.generate_data).pack(pady=3)
        ttk.Button(button_frame, text="导出文件", width=12,
                  command=self.export_data).pack(pady=3)
        ttk.Button(button_frame, text="导出到数据库", width=12,
                  command=self.export_to_database).pack(pady=3)
        ttk.Button(button_frame, text="清空数据", width=12,
                  command=self.clear_data).pack(pady=3)
        
        # 统计信息
        stats_frame = ttk.LabelFrame(settings_frame, text="统计信息", padding="5")
        stats_frame.grid(row=7, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        self.stats_var = tk.StringVar(value="字段: 0 | 数据: 0")
        ttk.Label(stats_frame, textvariable=self.stats_var, font=('Arial', 9)).pack()
        
        # 进度条
        self.progress = ttk.Progressbar(main_frame, mode='determinate')
        self.progress.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # 预览和编辑区域
        preview_frame = ttk.LabelFrame(main_frame, text="数据预览与编辑", padding="5")
        preview_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        # 搜索和过滤工具栏
        toolbar_frame = ttk.Frame(preview_frame)
        toolbar_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(toolbar_frame, text="搜索:").pack(side=tk.LEFT, padx=5)
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(toolbar_frame, textvariable=self.search_var, width=20)
        search_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar_frame, text="搜索", command=self.search_data).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar_frame, text="重置", command=self.reset_filter).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar_frame, text="编辑选中", command=self.edit_selected).pack(side=tk.LEFT, padx=10)
        ttk.Button(toolbar_frame, text="删除选中", command=self.delete_selected).pack(side=tk.LEFT, padx=2)
        
        # 创建表格
        table_frame = ttk.Frame(preview_frame)
        table_frame.pack(fill="both", expand=True)
        
        self.tree = ttk.Treeview(table_frame, show='headings', height=10)
        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        vsb.grid(row=0, column=1, sticky=(tk.N, tk.S))
        hsb.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)
        
        # 绑定排序事件
        self.tree.bind('<Button-1>', self.on_header_click)
        
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
        main_frame.rowconfigure(3, weight=2)
        
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
        
        selected = [field for field, data in self.field_vars.items() if data["var"].get()]
        
        if not selected:
            messagebox.showwarning("警告", "请至少选择一个字段")
            return
        
        thread = threading.Thread(target=self._generate_data_thread, args=(count, selected, False))
        thread.daemon = True
        thread.start()
        
    def incremental_generate(self):
        """增量生成（追加到现有数据）"""
        if self.generated_data is None:
            messagebox.showinfo("提示", "当前没有数据，将执行普通生成")
            self.generate_data()
            return
            
        try:
            count = int(self.count_var.get())
            if count <= 0 or count > 100000:
                messagebox.showerror("错误", "请输入1-100000之间的数量")
                return
        except ValueError:
            messagebox.showerror("错误", "请输入有效的数字")
            return
        
        selected = [field for field, data in self.field_vars.items() if data["var"].get()]
        
        if not selected:
            messagebox.showwarning("警告", "请至少选择一个字段")
            return
        
        thread = threading.Thread(target=self._generate_data_thread, args=(count, selected, True))
        thread.daemon = True
        thread.start()
        
    def _generate_data_thread(self, count, selected, append_mode=False):
        self.progress['mode'] = 'determinate'
        self.progress['maximum'] = count
        self.progress['value'] = 0
        self.status_var.set(f"正在生成 {count} 条数据...")
        
        fake = self.fake_zh if self.language_var.get() == "zh_CN" else self.fake_en
        used_emails = set()
        
        # 如果是追加模式，保留现有邮箱
        if append_mode and self.generated_data is not None and "邮箱" in self.generated_data.columns:
            used_emails = set(self.generated_data["邮箱"].values)
        
        data = []
        enable_correlation = self.enable_data_correlation.get()
        
        for i in range(count):
            row = self._generate_single_row(fake, selected, used_emails, enable_correlation, i)
            data.append(row)
            
            # 更新进度
            if i % 10 == 0:
                self.progress['value'] = i + 1
                self.root.update_idletasks()
        
        new_data = pd.DataFrame(data)
        
        # 追加或替换数据
        if append_mode and self.generated_data is not None:
            self.generated_data = pd.concat([self.generated_data, new_data], ignore_index=True)
        else:
            self.generated_data = new_data
        
        self.root.after(0, self._update_preview)
        self.root.after(0, self.update_stats)
        self.progress['value'] = count
        mode_text = "追加" if append_mode else "生成"
        self.status_var.set(f"✓ 成功{mode_text} {count} 条数据，总计 {len(self.generated_data)} 条")
        
    def _generate_single_row(self, fake, selected, used_emails, enable_correlation, index):
        """生成单行数据，支持数据关联"""
        row = {}
        
        # 如果启用关联，先生成关键字段
        age = None
        gender = None
        province = None
        city = None
        
        if enable_correlation:
            if "age" in selected:
                age = random.randint(18, 65)
            if "gender" in selected:
                gender = random.choice(["男", "女"]) if self.language_var.get() == "zh_CN" else random.choice(["Male", "Female"])
            if "province" in selected:
                province = fake.province() if hasattr(fake, 'province') else fake.state()
            if "city" in selected and province:
                # 城市应该在省份内（简化处理）
                city = fake.city()
        
        for field in selected:
            display_name = self.field_vars[field]["display"]
            
            # 检查是否有自定义规则
            if field in self.custom_rules:
                row[display_name] = self._apply_custom_rule(field, fake)
                continue
            
            try:
                # 个人信息 - 支持关联
                if field == "name":
                    if enable_correlation and gender:
                        if gender in ["男", "Male"]:
                            row[display_name] = fake.name_male() if hasattr(fake, 'name_male') else fake.name()
                        else:
                            row[display_name] = fake.name_female() if hasattr(fake, 'name_female') else fake.name()
                    else:
                        row[display_name] = fake.name()
                        
                elif field == "gender":
                    row[display_name] = gender if gender else (random.choice(["男", "女"]) if self.language_var.get() == "zh_CN" else random.choice(["Male", "Female"]))
                    
                elif field == "age":
                    row[display_name] = age if age else random.randint(18, 65)
                    
                elif field == "date_of_birth":
                    if enable_correlation and age:
                        # 根据年龄计算生日
                        birth_year = datetime.now().year - age
                        row[display_name] = str(fake.date_of_birth(minimum_age=age, maximum_age=age))
                    else:
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
                
                # 地址信息 - 支持关联
                elif field == "address":
                    row[display_name] = fake.address()
                elif field == "country":
                    row[display_name] = fake.country()
                elif field == "province":
                    row[display_name] = province if province else (fake.province() if hasattr(fake, 'province') else fake.state())
                elif field == "city":
                    row[display_name] = city if city else fake.city()
                elif field == "district":
                    row[display_name] = fake.city_suffix()
                elif field == "street_address":
                    row[display_name] = fake.street_address()
                elif field == "postcode":
                    row[display_name] = fake.postcode()
                elif field == "coordinates":
                    row[display_name] = f"{fake.latitude()}, {fake.longitude()}"
                
                # 公司职业 - 支持关联
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
                    row[display_name] = f"{self.prefix_var.get()}{index+1:06d}"
                elif field == "work_years":
                    if enable_correlation and age:
                        # 工作年限不应超过 年龄-18
                        max_work_years = min(age - 18, 30)
                        row[display_name] = random.randint(0, max(1, max_work_years))
                    else:
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
                
                # 教育信息 - 支持关联
                elif field == "school_name":
                    row[display_name] = fake.company() + ("大学" if self.language_var.get() == "zh_CN" else " University")
                elif field == "major":
                    majors = ["计算机科学", "工商管理", "机械工程", "英语", "数学"] if self.language_var.get() == "zh_CN" else ["Computer Science", "Business", "Engineering", "English", "Mathematics"]
                    row[display_name] = random.choice(majors)
                elif field == "education_level":
                    if enable_correlation and age:
                        # 根据年龄分配学历
                        if age < 22:
                            levels = ["本科"] if self.language_var.get() == "zh_CN" else ["Bachelor"]
                        elif age < 25:
                            levels = ["本科", "硕士"] if self.language_var.get() == "zh_CN" else ["Bachelor", "Master"]
                        else:
                            levels = ["本科", "硕士", "博士"] if self.language_var.get() == "zh_CN" else ["Bachelor", "Master", "PhD"]
                        row[display_name] = random.choice(levels)
                    else:
                        levels = ["本科", "硕士", "博士"] if self.language_var.get() == "zh_CN" else ["Bachelor", "Master", "PhD"]
                        row[display_name] = random.choice(levels)
                elif field == "graduation_year":
                    if enable_correlation and age:
                        # 根据年龄计算合理的毕业年份
                        grad_year = datetime.now().year - (age - 22)
                        row[display_name] = max(2000, grad_year)
                    else:
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
        
        return row
    
    def _apply_custom_rule(self, field, fake):
        """应用自定义字段规则"""
        rule = self.custom_rules[field]
        rule_type = rule.get('type', 'regex')
        
        if rule_type == 'regex':
            pattern = rule.get('pattern', '.*')
            try:
                return fake.regex(pattern)
            except:
                return "Invalid Pattern"
        elif rule_type == 'range':
            min_val = rule.get('min', 0)
            max_val = rule.get('max', 100)
            return random.randint(min_val, max_val)
        elif rule_type == 'choices':
            choices = rule.get('choices', [])
            weights = rule.get('weights', None)
            if weights:
                return random.choices(choices, weights=weights)[0]
            return random.choice(choices) if choices else "N/A"
        
        return "N/A"
        
    def _update_preview(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        if self.generated_data is not None:
            self.tree['columns'] = list(self.generated_data.columns)
            
            for col in self.generated_data.columns:
                self.tree.heading(col, text=col)
                self.tree.column(col, width=120)
            
            # 显示过滤后的数据或全部数据
            display_data = self.current_filter if self.current_filter is not None else self.generated_data
            
            for idx, row in display_data.head(100).iterrows():
                values = [str(val)[:50] for val in row.values]
                self.tree.insert('', 'end', values=values, tags=(idx,))
    
    def search_data(self):
        """搜索数据"""
        if self.generated_data is None:
            messagebox.showwarning("警告", "请先生成数据")
            return
        
        search_term = self.search_var.get().strip()
        if not search_term:
            messagebox.showinfo("提示", "请输入搜索内容")
            return
        
        # 在所有列中搜索
        mask = self.generated_data.apply(lambda row: row.astype(str).str.contains(search_term, case=False, na=False).any(), axis=1)
        self.current_filter = self.generated_data[mask]
        
        self._update_preview()
        self.status_var.set(f"搜索到 {len(self.current_filter)} 条匹配数据")
    
    def reset_filter(self):
        """重置过滤"""
        self.current_filter = None
        self.search_var.set("")
        self._update_preview()
        self.status_var.set("已重置过滤")
    
    def on_header_click(self, event):
        """处理表头点击事件，实现排序"""
        if self.generated_data is None:
            return
        
        region = self.tree.identify("region", event.x, event.y)
        if region == "heading":
            column = self.tree.identify_column(event.x)
            col_index = int(column.replace('#', '')) - 1
            
            if col_index >= 0 and col_index < len(self.tree['columns']):
                col_name = self.tree['columns'][col_index]
                
                # 排序
                self.generated_data = self.generated_data.sort_values(by=col_name)
                self._update_preview()
                self.status_var.set(f"已按 {col_name} 排序")
    
    def edit_selected(self):
        """编辑选中的行"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("警告", "请先选择要编辑的行")
            return
        
        item = selection[0]
        item_tags = self.tree.item(item, 'tags')
        if not item_tags:
            return
        
        row_index = int(item_tags[0])
        
        # 创建编辑对话框
        edit_window = tk.Toplevel(self.root)
        edit_window.title("编辑数据")
        edit_window.geometry("400x500")
        
        canvas = tk.Canvas(edit_window)
        scrollbar = ttk.Scrollbar(edit_window, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        entry_vars = {}
        row_num = 0
        
        for col in self.generated_data.columns:
            ttk.Label(scrollable_frame, text=f"{col}:").grid(row=row_num, column=0, sticky=tk.W, padx=5, pady=5)
            var = tk.StringVar(value=str(self.generated_data.at[row_index, col]))
            entry = ttk.Entry(scrollable_frame, textvariable=var, width=30)
            entry.grid(row=row_num, column=1, padx=5, pady=5)
            entry_vars[col] = var
            row_num += 1
        
        def save_changes():
            for col, var in entry_vars.items():
                self.generated_data.at[row_index, col] = var.get()
            self._update_preview()
            edit_window.destroy()
            self.status_var.set("数据已更新")
        
        button_frame = ttk.Frame(scrollable_frame)
        button_frame.grid(row=row_num, column=0, columnspan=2, pady=10)
        ttk.Button(button_frame, text="保存", command=save_changes).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="取消", command=edit_window.destroy).pack(side=tk.LEFT, padx=5)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def delete_selected(self):
        """删除选中的行"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("警告", "请先选择要删除的行")
            return
        
        result = messagebox.askyesno("确认", f"确定要删除选中的 {len(selection)} 行吗？")
        if not result:
            return
        
        indices_to_delete = []
        for item in selection:
            item_tags = self.tree.item(item, 'tags')
            if item_tags:
                indices_to_delete.append(int(item_tags[0]))
        
        self.generated_data = self.generated_data.drop(indices_to_delete).reset_index(drop=True)
        self._update_preview()
        self.update_stats()
        self.status_var.set(f"已删除 {len(indices_to_delete)} 行")
    
    def validate_data(self):
        """数据验证"""
        if self.generated_data is None:
            messagebox.showwarning("警告", "请先生成数据")
            return
        
        issues = []
        
        # 检查邮箱格式
        if "邮箱" in self.generated_data.columns:
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
            invalid_emails = self.generated_data[~self.generated_data["邮箱"].str.match(email_pattern, na=False)]
            if not invalid_emails.empty:
                issues.append(f"发现 {len(invalid_emails)} 个无效邮箱格式")
        
        # 检查电话号码格式
        if "手机号" in self.generated_data.columns:
            invalid_phones = self.generated_data[self.generated_data["手机号"].isna()]
            if not invalid_phones.empty:
                issues.append(f"发现 {len(invalid_phones)} 个空手机号")
        
        # 检查年龄范围
        if "年龄" in self.generated_data.columns:
            invalid_ages = self.generated_data[(self.generated_data["年龄"] < 0) | (self.generated_data["年龄"] > 120)]
            if not invalid_ages.empty:
                issues.append(f"发现 {len(invalid_ages)} 个异常年龄")
        
        # 检查重复邮箱
        if "邮箱" in self.generated_data.columns:
            duplicates = self.generated_data[self.generated_data["邮箱"].duplicated()]
            if not duplicates.empty:
                issues.append(f"发现 {len(duplicates)} 个重复邮箱")
        
        if issues:
            messagebox.showwarning("数据验证结果", "\n".join(issues))
        else:
            messagebox.showinfo("数据验证结果", "✓ 所有数据验证通过！")
    
    def show_statistics(self):
        """显示数据统计分析"""
        if self.generated_data is None:
            messagebox.showwarning("警告", "请先生成数据")
            return
        
        stats_window = tk.Toplevel(self.root)
        stats_window.title("数据统计分析")
        stats_window.geometry("800x600")
        
        notebook = ttk.Notebook(stats_window)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # 基础统计
        basic_frame = ttk.Frame(notebook)
        notebook.add(basic_frame, text="基础统计")
        
        text_widget = tk.Text(basic_frame, wrap=tk.WORD, width=80, height=30)
        text_widget.pack(fill="both", expand=True, padx=10, pady=10)
        
        stats_text = f"数据集基本信息\n{'='*50}\n\n"
        stats_text += f"总行数: {len(self.generated_data)}\n"
        stats_text += f"总列数: {len(self.generated_data.columns)}\n"
        stats_text += f"内存占用: {self.generated_data.memory_usage(deep=True).sum() / 1024:.2f} KB\n\n"
        
        stats_text += f"各列统计\n{'-'*50}\n"
        for col in self.generated_data.columns:
            stats_text += f"\n【{col}】\n"
            stats_text += f"  非空值: {self.generated_data[col].count()}\n"
            stats_text += f"  空值数: {self.generated_data[col].isna().sum()}\n"
            stats_text += f"  唯一值: {self.generated_data[col].nunique()}\n"
            
            # 如果是数值类型
            if pd.api.types.is_numeric_dtype(self.generated_data[col]):
                stats_text += f"  最小值: {self.generated_data[col].min()}\n"
                stats_text += f"  最大值: {self.generated_data[col].max()}\n"
                stats_text += f"  平均值: {self.generated_data[col].mean():.2f}\n"
        
        text_widget.insert('1.0', stats_text)
        text_widget.config(state='disabled')
        
        # 图表分析
        chart_frame = ttk.Frame(notebook)
        notebook.add(chart_frame, text="图表分析")
        
        fig = Figure(figsize=(10, 6))
        
        # 选择一些字段进行可视化
        numeric_cols = self.generated_data.select_dtypes(include=['int64', 'float64']).columns
        if len(numeric_cols) > 0:
            ax1 = fig.add_subplot(2, 2, 1)
            col = numeric_cols[0]
            self.generated_data[col].hist(ax=ax1, bins=20)
            ax1.set_title(f'{col} 分布')
            ax1.set_xlabel(col)
            ax1.set_ylabel('频数')
        
        # 分类字段分析
        categorical_cols = self.generated_data.select_dtypes(include=['object']).columns
        if len(categorical_cols) > 0:
            for i, col in enumerate(categorical_cols[:3]):
                if self.generated_data[col].nunique() < 20:
                    ax = fig.add_subplot(2, 2, i+2)
                    value_counts = self.generated_data[col].value_counts().head(10)
                    value_counts.plot(kind='bar', ax=ax)
                    ax.set_title(f'{col} 前10分布')
                    ax.set_xlabel(col)
                    ax.set_ylabel('数量')
                    ax.tick_params(axis='x', rotation=45)
        
        fig.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, master=chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
    
    def custom_field_rules(self):
        """自定义字段规则对话框"""
        rule_window = tk.Toplevel(self.root)
        rule_window.title("自定义字段规则")
        rule_window.geometry("600x400")
        
        ttk.Label(rule_window, text="选择字段:").grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        
        field_var = tk.StringVar()
        all_fields = [data["display"] for data in self.field_vars.values()]
        field_combo = ttk.Combobox(rule_window, textvariable=field_var, values=all_fields, width=30)
        field_combo.grid(row=0, column=1, padx=10, pady=10)
        
        ttk.Label(rule_window, text="规则类型:").grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        
        rule_type_var = tk.StringVar(value="choices")
        ttk.Radiobutton(rule_window, text="选项列表(带权重)", variable=rule_type_var, value="choices").grid(row=1, column=1, sticky=tk.W)
        ttk.Radiobutton(rule_window, text="数值范围", variable=rule_type_var, value="range").grid(row=2, column=1, sticky=tk.W)
        ttk.Radiobutton(rule_window, text="正则表达式", variable=rule_type_var, value="regex").grid(row=3, column=1, sticky=tk.W)
        
        # 选项列表配置
        ttk.Label(rule_window, text="选项(逗号分隔):").grid(row=4, column=0, padx=10, pady=10, sticky=tk.W)
        choices_var = tk.StringVar()
        ttk.Entry(rule_window, textvariable=choices_var, width=40).grid(row=4, column=1, padx=10, pady=10)
        
        ttk.Label(rule_window, text="权重(逗号分隔):").grid(row=5, column=0, padx=10, pady=10, sticky=tk.W)
        weights_var = tk.StringVar()
        ttk.Entry(rule_window, textvariable=weights_var, width=40).grid(row=5, column=1, padx=10, pady=10)
        
        # 数值范围配置
        ttk.Label(rule_window, text="最小值:").grid(row=6, column=0, padx=10, pady=10, sticky=tk.W)
        min_var = tk.StringVar(value="0")
        ttk.Entry(rule_window, textvariable=min_var, width=20).grid(row=6, column=1, padx=10, pady=10, sticky=tk.W)
        
        ttk.Label(rule_window, text="最大值:").grid(row=7, column=0, padx=10, pady=10, sticky=tk.W)
        max_var = tk.StringVar(value="100")
        ttk.Entry(rule_window, textvariable=max_var, width=20).grid(row=7, column=1, padx=10, pady=10, sticky=tk.W)
        
        # 正则表达式配置
        ttk.Label(rule_window, text="正则表达式:").grid(row=8, column=0, padx=10, pady=10, sticky=tk.W)
        regex_var = tk.StringVar()
        ttk.Entry(rule_window, textvariable=regex_var, width=40).grid(row=8, column=1, padx=10, pady=10)
        
        def save_rule():
            field_name = field_var.get()
            if not field_name:
                messagebox.showwarning("警告", "请选择字段")
                return
            
            # 找到字段的内部名称
            field_key = None
            for key, data in self.field_vars.items():
                if data["display"] == field_name:
                    field_key = key
                    break
            
            if not field_key:
                return
            
            rule_type = rule_type_var.get()
            rule = {'type': rule_type}
            
            if rule_type == 'choices':
                choices = [c.strip() for c in choices_var.get().split(',') if c.strip()]
                if not choices:
                    messagebox.showwarning("警告", "请输入选项")
                    return
                rule['choices'] = choices
                
                weights_str = weights_var.get().strip()
                if weights_str:
                    try:
                        weights = [float(w.strip()) for w in weights_str.split(',')]
                        if len(weights) == len(choices):
                            rule['weights'] = weights
                    except:
                        pass
                        
            elif rule_type == 'range':
                try:
                    rule['min'] = int(min_var.get())
                    rule['max'] = int(max_var.get())
                except:
                    messagebox.showwarning("警告", "请输入有效的数值")
                    return
                    
            elif rule_type == 'regex':
                pattern = regex_var.get().strip()
                if not pattern:
                    messagebox.showwarning("警告", "请输入正则表达式")
                    return
                rule['pattern'] = pattern
            
            self.custom_rules[field_key] = rule
            messagebox.showinfo("成功", f"已为 {field_name} 设置自定义规则")
            rule_window.destroy()
        
        ttk.Button(rule_window, text="保存规则", command=save_rule).grid(row=9, column=0, columnspan=2, pady=20)
    
    def database_settings(self):
        """数据库连接设置"""
        db_window = tk.Toplevel(self.root)
        db_window.title("数据库连接设置")
        db_window.geometry("500x400")
        
        ttk.Label(db_window, text="数据库类型:").grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        db_type_var = tk.StringVar(value="mysql")
        ttk.Combobox(db_window, textvariable=db_type_var, values=["mysql", "postgresql", "sqlite"], 
                     state="readonly", width=30).grid(row=0, column=1, padx=10, pady=10)
        
        ttk.Label(db_window, text="主机:").grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        host_var = tk.StringVar(value="localhost")
        ttk.Entry(db_window, textvariable=host_var, width=32).grid(row=1, column=1, padx=10, pady=10)
        
        ttk.Label(db_window, text="端口:").grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)
        port_var = tk.StringVar(value="3306")
        ttk.Entry(db_window, textvariable=port_var, width=32).grid(row=2, column=1, padx=10, pady=10)
        
        ttk.Label(db_window, text="数据库名:").grid(row=3, column=0, padx=10, pady=10, sticky=tk.W)
        database_var = tk.StringVar(value="test_db")
        ttk.Entry(db_window, textvariable=database_var, width=32).grid(row=3, column=1, padx=10, pady=10)
        
        ttk.Label(db_window, text="用户名:").grid(row=4, column=0, padx=10, pady=10, sticky=tk.W)
        username_var = tk.StringVar(value="root")
        ttk.Entry(db_window, textvariable=username_var, width=32).grid(row=4, column=1, padx=10, pady=10)
        
        ttk.Label(db_window, text="密码:").grid(row=5, column=0, padx=10, pady=10, sticky=tk.W)
        password_var = tk.StringVar()
        ttk.Entry(db_window, textvariable=password_var, show="*", width=32).grid(row=5, column=1, padx=10, pady=10)
        
        def test_connection():
            messagebox.showinfo("提示", "数据库连接测试功能需要安装对应的数据库驱动\n(pymysql, psycopg2, sqlite3)")
        
        def save_settings():
            self.db_config = {
                'type': db_type_var.get(),
                'host': host_var.get(),
                'port': port_var.get(),
                'database': database_var.get(),
                'username': username_var.get(),
                'password': password_var.get()
            }
            messagebox.showinfo("成功", "数据库配置已保存")
            db_window.destroy()
        
        button_frame = ttk.Frame(db_window)
        button_frame.grid(row=6, column=0, columnspan=2, pady=20)
        ttk.Button(button_frame, text="测试连接", command=test_connection).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="保存", command=save_settings).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="取消", command=db_window.destroy).pack(side=tk.LEFT, padx=5)
    
    def export_to_database(self):
        """导出到数据库"""
        if self.generated_data is None:
            messagebox.showwarning("警告", "请先生成数据")
            return
        
        if not hasattr(self, 'db_config'):
            result = messagebox.askyesno("提示", "尚未配置数据库连接，是否现在配置？")
            if result:
                self.database_settings()
            return
        
        messagebox.showinfo("提示", "数据库导出功能需要安装对应的数据库驱动\n示例: pip install pymysql sqlalchemy")
    
    def batch_generate(self):
        """批量生成多组数据"""
        dialog = simpledialog.askinteger("批量生成", "请输入要生成的批次数量:", minvalue=1, maxvalue=100)
        if not dialog:
            return
        
        batch_count = dialog
        count_per_batch = int(self.count_var.get())
        
        result = messagebox.askyesno("确认", f"将生成 {batch_count} 个文件，每个包含 {count_per_batch} 条数据。\n是否继续？")
        if not result:
            return
        
        directory = filedialog.askdirectory(title="选择保存目录")
        if not directory:
            return
        
        selected = [field for field, data in self.field_vars.items() if data["var"].get()]
        if not selected:
            messagebox.showwarning("警告", "请至少选择一个字段")
            return
        
        # 在新线程中批量生成
        thread = threading.Thread(target=self._batch_generate_thread, 
                                 args=(batch_count, count_per_batch, selected, directory))
        thread.daemon = True
        thread.start()
    
    def _batch_generate_thread(self, batch_count, count_per_batch, selected, directory):
        """批量生成线程"""
        self.progress['mode'] = 'determinate'
        self.progress['maximum'] = batch_count
        self.progress['value'] = 0
        
        fake = self.fake_zh if self.language_var.get() == "zh_CN" else self.fake_en
        file_format = self.format_var.get()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        for batch in range(batch_count):
            self.status_var.set(f"正在生成第 {batch + 1}/{batch_count} 批数据...")
            
            data = []
            used_emails = set()
            
            for i in range(count_per_batch):
                row = self._generate_single_row(fake, selected, used_emails, 
                                               self.enable_data_correlation.get(), i)
                data.append(row)
            
            df = pd.DataFrame(data)
            
            # 保存文件
            filename = f"{directory}/batch_{batch + 1}_{timestamp}.{file_format}"
            
            try:
                if file_format == "csv":
                    if self.compress_var.get():
                        filename += ".gz"
                        df.to_csv(filename, index=False, encoding='utf-8-sig', compression='gzip')
                    else:
                        df.to_csv(filename, index=False, encoding='utf-8-sig')
                elif file_format == "excel":
                    df.to_excel(filename, index=False, engine='openpyxl')
                elif file_format == "json":
                    df.to_json(filename, orient='records', force_ascii=False, indent=2)
                elif file_format == "parquet":
                    df.to_parquet(filename, index=False)
            except Exception as e:
                self.status_var.set(f"批次 {batch + 1} 保存失败: {str(e)}")
                continue
            
            self.progress['value'] = batch + 1
            self.root.update_idletasks()
        
        self.status_var.set(f"✓ 批量生成完成！共 {batch_count} 个文件已保存到: {directory}")
        messagebox.showinfo("完成", f"批量生成完成！\n共 {batch_count} 个文件\n保存位置: {directory}")
    
    def save_template(self):
        """保存配置模板"""
        if not any(data["var"].get() for data in self.field_vars.values()):
            messagebox.showwarning("警告", "请先选择字段")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".fdt",
            initialfile=f"template_{datetime.now().strftime('%Y%m%d_%H%M%S')}.fdt",
            filetypes=[("Faker Data Template", "*.fdt"), ("All files", "*.*")]
        )
        
        if not filename:
            return
        
        template = {
            'language': self.language_var.get(),
            'count': self.count_var.get(),
            'format': self.format_var.get(),
            'unique_email': self.unique_var.get(),
            'compress': self.compress_var.get(),
            'prefix': self.prefix_var.get(),
            'table_name': self.table_name_var.get(),
            'enable_correlation': self.enable_data_correlation.get(),
            'selected_fields': [field for field, data in self.field_vars.items() if data["var"].get()],
            'custom_rules': self.custom_rules
        }
        
        try:
            with open(filename, 'wb') as f:
                pickle.dump(template, f)
            messagebox.showinfo("成功", f"配置模板已保存到:\n{filename}")
        except Exception as e:
            messagebox.showerror("错误", f"保存失败: {str(e)}")
    
    def load_template(self):
        """加载配置模板"""
        filename = filedialog.askopenfilename(
            title="选择模板文件",
            filetypes=[("Faker Data Template", "*.fdt"), ("All files", "*.*")]
        )
        
        if not filename:
            return
        
        try:
            with open(filename, 'rb') as f:
                template = pickle.load(f)
            
            # 恢复配置
            self.language_var.set(template.get('language', 'zh_CN'))
            self.count_var.set(template.get('count', '100'))
            self.format_var.set(template.get('format', 'csv'))
            self.unique_var.set(template.get('unique_email', False))
            self.compress_var.set(template.get('compress', False))
            self.prefix_var.set(template.get('prefix', 'USER'))
            self.table_name_var.set(template.get('table_name', 'fake_data'))
            self.enable_data_correlation.set(template.get('enable_correlation', True))
            
            # 恢复字段选择
            for field, data in self.field_vars.items():
                data["var"].set(field in template.get('selected_fields', []))
            
            # 恢复自定义规则
            self.custom_rules = template.get('custom_rules', {})
            
            self.update_stats()
            messagebox.showinfo("成功", "配置模板加载成功！")
            
        except Exception as e:
            messagebox.showerror("错误", f"加载失败: {str(e)}")
    
    def export_data(self):
        if self.generated_data is None:
            messagebox.showwarning("警告", "请先生成数据")
            return
        
        file_format = self.format_var.get()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        try:
            if file_format == "csv":
                filename = filedialog.asksaveasfilename(
                    defaultextension=".csv" if not self.compress_var.get() else ".csv.gz",
                    initialfile=f"fake_data_{timestamp}.csv{'gz' if self.compress_var.get() else ''}",
                    filetypes=[("CSV files", "*.csv"), ("Compressed CSV", "*.csv.gz"), ("All files", "*.*")]
                )
                if filename:
                    if self.compress_var.get():
                        self.generated_data.to_csv(filename, index=False, encoding='utf-8-sig', compression='gzip')
                    else:
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
                    self._export_sql(filename)
                    messagebox.showinfo("成功", f"已导出 {len(self.generated_data)} 条数据到:\n{filename}")
            
            elif file_format == "xml":
                filename = filedialog.asksaveasfilename(
                    defaultextension=".xml",
                    initialfile=f"fake_data_{timestamp}.xml",
                    filetypes=[("XML files", "*.xml"), ("All files", "*.*")]
                )
                if filename:
                    self._export_xml(filename)
                    messagebox.showinfo("成功", f"已导出 {len(self.generated_data)} 条数据到:\n{filename}")
            
            elif file_format == "yaml":
                filename = filedialog.asksaveasfilename(
                    defaultextension=".yaml",
                    initialfile=f"fake_data_{timestamp}.yaml",
                    filetypes=[("YAML files", "*.yaml"), ("All files", "*.*")]
                )
                if filename:
                    data_dict = self.generated_data.to_dict(orient='records')
                    with open(filename, 'w', encoding='utf-8') as f:
                        yaml.dump(data_dict, f, allow_unicode=True, default_flow_style=False)
                    messagebox.showinfo("成功", f"已导出 {len(self.generated_data)} 条数据到:\n{filename}")
            
            elif file_format == "parquet":
                filename = filedialog.asksaveasfilename(
                    defaultextension=".parquet",
                    initialfile=f"fake_data_{timestamp}.parquet",
                    filetypes=[("Parquet files", "*.parquet"), ("All files", "*.*")]
                )
                if filename:
                    self.generated_data.to_parquet(filename, index=False)
                    messagebox.showinfo("成功", f"已导出 {len(self.generated_data)} 条数据到:\n{filename}")
        
        except Exception as e:
            messagebox.showerror("错误", f"导出失败: {str(e)}")
    
    def _export_sql(self, filename):
        """导出为SQL文件"""
        table_name = self.table_name_var.get()
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"-- Generated on {datetime.now()}\n")
            f.write(f"-- Total records: {len(self.generated_data)}\n\n")
            f.write(f"DROP TABLE IF EXISTS `{table_name}`;\n\n")
            f.write(f"CREATE TABLE `{table_name}` (\n")
            f.write("    `id` INT PRIMARY KEY AUTO_INCREMENT,\n")
            
            for col in self.generated_data.columns:
                col_type = "VARCHAR(500)"
                if pd.api.types.is_integer_dtype(self.generated_data[col]):
                    col_type = "INT"
                elif pd.api.types.is_float_dtype(self.generated_data[col]):
                    col_type = "DECIMAL(10, 2)"
                f.write(f"    `{col}` {col_type},\n")
            
            f.write("    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP\n")
            f.write(") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;\n\n")
            
            # 分批插入（每100条一个INSERT语句）
            batch_size = 100
            for start_idx in range(0, len(self.generated_data), batch_size):
                end_idx = min(start_idx + batch_size, len(self.generated_data))
                batch = self.generated_data.iloc[start_idx:end_idx]
                
                f.write(f"INSERT INTO `{table_name}` (")
                f.write("`, `".join(self.generated_data.columns))
                f.write("`) VALUES\n")
                
                for idx, (_, row) in enumerate(batch.iterrows()):
                    values = []
                    for val in row.values:
                        if pd.isna(val):
                            values.append("NULL")
                        else:
                            escaped_val = str(val).replace("'", "''").replace("\\", "\\\\")
                            values.append(f"'{escaped_val}'")
                    
                    f.write(f"    ({', '.join(values)})")
                    if idx < len(batch) - 1:
                        f.write(",\n")
                    else:
                        f.write(";\n\n")
    
    def _export_xml(self, filename):
        """导出为XML文件"""
        root = ET.Element("data")
        root.set("generated", str(datetime.now()))
        root.set("count", str(len(self.generated_data)))
        
        for _, row in self.generated_data.iterrows():
            record = ET.SubElement(root, "record")
            for col, val in row.items():
                field = ET.SubElement(record, "field")
                field.set("name", col)
                field.text = str(val) if not pd.isna(val) else ""
        
        tree = ET.ElementTree(root)
        ET.indent(tree, space="  ")
        tree.write(filename, encoding='utf-8', xml_declaration=True)
    
    def clear_data(self):
        if self.generated_data is not None:
            result = messagebox.askyesno("确认", "确定要清空所有数据吗？")
            if result:
                for item in self.tree.get_children():
                    self.tree.delete(item)
                self.generated_data = None
                self.current_filter = None
                self.update_stats()
                self.status_var.set("已清空数据")
        else:
            self.status_var.set("没有数据需要清空")

    def show_help(self):
        """显示详细使用说明"""
        help_window = tk.Toplevel(self.root)
        help_window.title("使用说明")
        help_window.geometry("800x600")
        
        # 创建Notebook
        notebook = ttk.Notebook(help_window)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # 基础使用
        basic_frame = ttk.Frame(notebook)
        notebook.add(basic_frame, text="基础使用")
        
        basic_text = tk.Text(basic_frame, wrap=tk.WORD, padx=10, pady=10)
        basic_scroll = ttk.Scrollbar(basic_frame, command=basic_text.yview)
        basic_text.configure(yscrollcommand=basic_scroll.set)
        
        basic_content = """
    【基础使用】

    1. 选择字段
    • 在左侧标签页中选择需要的数据字段
    • 使用"全选"/"取消"/"反选"快速操作
    • 支持跨类别多选

    2. 设置参数
    • 生成数量：1-100000条（推荐≤10000）
    • 导出格式：CSV、Excel、JSON、SQL等8种
    • 语言设置：中文/English
    • ID前缀：自定义编号前缀（如：USER、EMP）

    3. 生成数据
    • 点击"生成数据"按钮
    • 查看进度条和状态提示
    • 数据自动显示在预览区

    4. 导出文件
    • 点击"导出文件"按钮
    • 选择保存位置和文件名
    • 勾选"压缩导出"可减小文件体积

    【快捷键】
    - Ctrl+A：全选预览区数据
    - Ctrl+F：快速搜索
    - 点击表头：排序数据
        """
        
        basic_text.insert('1.0', basic_content)
        basic_text.configure(state='disabled')
        basic_text.pack(side="left", fill="both", expand=True)
        basic_scroll.pack(side="right", fill="y")
        
        # 高级功能
        advanced_frame = ttk.Frame(notebook)
        notebook.add(advanced_frame, text="高级功能")
        
        adv_text = tk.Text(advanced_frame, wrap=tk.WORD, padx=10, pady=10)
        adv_scroll = ttk.Scrollbar(advanced_frame, command=adv_text.yview)
        adv_text.configure(yscrollcommand=adv_scroll.set)
        
        adv_content = """
    【数据关联性】

    启用后，系统会自动关联相关字段，生成更真实的数据：

    - 年龄 ←→ 学历
    年龄<22只分配本科；年龄>25可分配硕士、博士

    - 年龄 ←→ 工作年限
    工作年限不会超过(年龄-18)

    - 年龄 ←→ 生日
    根据年龄自动生成匹配的出生日期

    - 性别 ←→ 姓名
    根据性别生成对应的男/女性姓名

    使用场景：生成用户画像、员工信息时建议启用
        """
        
        adv_text.insert('1.0', adv_content)
        adv_text.configure(state='disabled')
        adv_text.pack(side="left", fill="both", expand=True)
        adv_scroll.pack(side="right", fill="y")
        
        # 数据处理
        data_frame = ttk.Frame(notebook)
        notebook.add(data_frame, text="数据处理")
        
        data_text = tk.Text(data_frame, wrap=tk.WORD, padx=10, pady=10)
        data_scroll = ttk.Scrollbar(data_frame, command=data_text.yview)
        data_text.configure(yscrollcommand=data_scroll.set)
        
        data_content = """
    【搜索功能】

    1. 在搜索框输入关键词
    2. 点击"搜索"按钮
    3. 系统在所有列中查找匹配数据
    4. 点击"重置"恢复全部数据


    【排序功能】

    - 点击任意列的表头
    - 数据按该列排序
    - 支持数值、文本、日期排序
        """
        
        data_text.insert('1.0', data_content)
        data_text.configure(state='disabled')
        data_text.pack(side="left", fill="both", expand=True)
        data_scroll.pack(side="right", fill="y")

    def quick_start_guide(self):
        """快速入门"""
        guide_window = tk.Toplevel(self.root)
        guide_window.title("快速入门")
        guide_window.geometry("400x300")
        
        # 创建Notebook
        notebook = ttk.Notebook(guide_window)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # 步骤 1: 选择字段
        step1_frame = ttk.Frame(notebook)
        notebook.add(step1_frame, text="步骤 1: 选择字段")
        
        step1_text = tk.Text(step1_frame, wrap=tk.WORD, padx=10, pady=10)
        step1_text.insert('1.0', """
        选择您需要生成的数据字段。您可以在左侧面板中选择不同类别的字段，
        比如个人信息、联系方式、地址信息等。使用“全选”、“取消”或“反选”按钮快速选择。
        """)
        step1_text.configure(state='disabled')
        step1_text.pack(fill="both", expand=True)
        
        # 步骤 2: 配置生成参数
        step2_frame = ttk.Frame(notebook)
        notebook.add(step2_frame, text="步骤 2: 配置生成参数")
        
        step2_text = tk.Text(step2_frame, wrap=tk.WORD, padx=10, pady=10)
        step2_text.insert('1.0', """
        配置生成的数据数量、导出格式（CSV、Excel、JSON等），
        选择语言（中文或英文），以及是否启用数据关联性（如：年龄与学历关联）。
        在右侧面板中设置ID前缀等生成规则。
        """)
        step2_text.configure(state='disabled')
        step2_text.pack(fill="both", expand=True)
        
        # 步骤 3: 生成和导出数据
        step3_frame = ttk.Frame(notebook)
        notebook.add(step3_frame, text="步骤 3: 生成和导出数据")
        
        step3_text = tk.Text(step3_frame, wrap=tk.WORD, padx=10, pady=10)
        step3_text.insert('1.0', """
        点击“生成数据”按钮开始生成数据，生成进度将在底部显示。
        生成完成后，点击“导出文件”按钮选择导出格式和保存位置。
        您可以选择压缩导出以减小文件体积。
        """)
        step3_text.configure(state='disabled')
        step3_text.pack(fill="both", expand=True)

    def show_about(self):
        """关于"""
        about_window = tk.Toplevel(self.root)
        about_window.title("关于")
        about_window.geometry("400x300")
        
        # 内容
        about_text = tk.Text(about_window, wrap=tk.WORD, padx=10, pady=10)
        about_text.insert('1.0', """
        Faker Data Generator Pro Max
        版本: 1.0.0
        作者: Your Name
        版权所有 (c) 2025

        本工具用于生成虚假数据，适用于各种测试场景。
        使用Faker库提供的数据生成能力，您可以自定义字段、配置生成规则，并将数据导出为不同格式。

        特别感谢以下开源项目：
        - Faker (https://faker.readthedocs.io/)
        - Tkinter (https://wiki.python.org/moin/TkInter)

        联系我们：
        - 电子邮件: support@example.com
        """)
        about_text.configure(state='disabled')
        about_text.pack(fill="both", expand=True)



if __name__ == "__main__":
    root = tk.Tk()
    app = FakerDataGenerator(root)
    root.mainloop()