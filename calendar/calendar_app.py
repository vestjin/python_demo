
import tkinter as tk
from tkinter import ttk, messagebox
import calendar
from datetime import datetime, timedelta
import json
import os

class CalendarApp:
    def __init__(self, root):
        self.root = root
        self.root.title("智能日历助手")
        self.root.geometry("1200x800")
        self.root.configure(bg="#f5f5f5")
        self.root.minsize(900, 600)
        
        # 数据存储
        self.events_file = "calendar_events.json"
        self.events = self.load_events()
        
        # 当前日期
        self.current_date = datetime.now()
        self.selected_date = None
        
        # 样式配置
        self.setup_styles()
        
        # 创建UI
        self.create_widgets()
        self.update_calendar()
        
    def setup_styles(self):
        """设置样式"""
        self.colors = {
            'primary': '#2563EB',
            'primary_dark': '#1D4ED8',
            'primary_light': '#DBEAFE',
            'accent': '#F59E0B',
            'success': '#10B981',
            'warning': '#F59E0B',
            'danger': '#EF4444',
            'light': '#FFFFFF',
            'dark': '#1F2937',
            'grey': '#6B7280',
            'grey_light': '#F3F4F6',
            'background': '#F9FAFB',
            'border': '#E5E7EB'
        }
        
    def load_events(self):
        """加载事件数据"""
        if os.path.exists(self.events_file):
            try:
                with open(self.events_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_events(self):
        """保存事件数据"""
        with open(self.events_file, 'w', encoding='utf-8') as f:
            json.dump(self.events, f, ensure_ascii=False, indent=2)
    
    def create_widgets(self):
        """创建界面组件"""
        # ==================== 顶部区域 ====================
        self.create_header()
        
        # ==================== 导航栏 ====================
        self.create_navigation()
        
        # ==================== 主内容区域 ====================
        main_container = tk.Frame(self.root, bg=self.colors['background'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # 左侧：日历视图 (70%)
        self.create_calendar_view(main_container)
        
        # 右侧：事件面板 (30%)
        self.create_event_panel(main_container)
    
    def create_header(self):
        """创建顶部标题栏"""
        header = tk.Frame(self.root, bg=self.colors['primary'], height=70)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        # 内容容器
        content = tk.Frame(header, bg=self.colors['primary'])
        content.pack(fill=tk.BOTH, expand=True, padx=30, pady=15)
        
        # 左侧：标题
        left_frame = tk.Frame(content, bg=self.colors['primary'])
        left_frame.pack(side=tk.LEFT)
        
        tk.Label(left_frame, text="📅", font=("Arial", 32), 
                bg=self.colors['primary']).pack(side=tk.LEFT, padx=(0, 12))
        
        title_container = tk.Frame(left_frame, bg=self.colors['primary'])
        title_container.pack(side=tk.LEFT)
        
        tk.Label(title_container, text="智能日历", 
                font=("Arial", 20, "bold"),
                bg=self.colors['primary'], fg="white").pack(anchor=tk.W)
        
        tk.Label(title_container, text="高效管理您的时间", 
                font=("Arial", 10),
                bg=self.colors['primary'], fg="#BFDBFE").pack(anchor=tk.W)
        
        # 右侧：实时时间
        right_frame = tk.Frame(content, bg=self.colors['primary'])
        right_frame.pack(side=tk.RIGHT)
        
        self.time_label = tk.Label(right_frame, text="", 
                                   font=("Arial", 13, "bold"),
                                   bg=self.colors['primary'], fg="white")
        self.time_label.pack(anchor=tk.E)
        
        self.date_label = tk.Label(right_frame, text="", 
                                   font=("Arial", 10),
                                   bg=self.colors['primary'], fg="#BFDBFE")
        self.date_label.pack(anchor=tk.E)
        
        self.update_time()
    
    def create_navigation(self):
        """创建导航栏"""
        nav_frame = tk.Frame(self.root, bg=self.colors['light'], height=70)
        nav_frame.pack(fill=tk.X, pady=(0, 20))
        nav_frame.pack_propagate(False)
        
        # 添加底部边框
        tk.Frame(nav_frame, bg=self.colors['border'], height=1).pack(
            side=tk.BOTTOM, fill=tk.X)
        
        content = tk.Frame(nav_frame, bg=self.colors['light'])
        content.pack(fill=tk.BOTH, expand=True, padx=30, pady=12)
        
        # 左侧：导航按钮
        left_nav = tk.Frame(content, bg=self.colors['light'])
        left_nav.pack(side=tk.LEFT)
        
        nav_style = {
            'font': ("Arial", 11, "bold"),
            'relief': tk.FLAT,
            'cursor': "hand2",
            'padx': 15,
            'pady': 8,
            'fg': "white"
        }
        
        btn_prev_year = tk.Button(left_nav, text="◀◀", 
                                  bg=self.colors['grey'],
                                  command=self.prev_year, **nav_style)
        btn_prev_year.pack(side=tk.LEFT, padx=(0, 5))
        self.add_hover_effect(btn_prev_year, self.colors['grey'], 
                            self.colors['dark'])
        
        btn_prev_month = tk.Button(left_nav, text="◀", 
                                   bg=self.colors['primary'],
                                   command=self.prev_month, **nav_style)
        btn_prev_month.pack(side=tk.LEFT, padx=(0, 15))
        self.add_hover_effect(btn_prev_month, self.colors['primary'], 
                            self.colors['primary_dark'])
        
        # 中间：月份显示
        self.month_label = tk.Label(content, text="", 
                                    bg=self.colors['light'], 
                                    fg=self.colors['dark'],
                                    font=("Arial", 20, "bold"))
        self.month_label.pack(side=tk.LEFT, expand=True)
        
        # 右侧：导航和功能按钮
        right_nav = tk.Frame(content, bg=self.colors['light'])
        right_nav.pack(side=tk.RIGHT)
        
        btn_today = tk.Button(right_nav, text="今天", 
                             bg=self.colors['success'],
                             command=self.go_to_today, **nav_style)
        btn_today.pack(side=tk.LEFT, padx=(0, 15))
        self.add_hover_effect(btn_today, self.colors['success'], "#059669")
        
        btn_next_month = tk.Button(right_nav, text="▶", 
                                   bg=self.colors['primary'],
                                   command=self.next_month, **nav_style)
        btn_next_month.pack(side=tk.LEFT, padx=(0, 5))
        self.add_hover_effect(btn_next_month, self.colors['primary'], 
                            self.colors['primary_dark'])
        
        btn_next_year = tk.Button(right_nav, text="▶▶", 
                                  bg=self.colors['grey'],
                                  command=self.next_year, **nav_style)
        btn_next_year.pack(side=tk.LEFT)
        self.add_hover_effect(btn_next_year, self.colors['grey'], 
                            self.colors['dark'])
    
    def create_calendar_view(self, parent):
        """创建日历视图"""
        calendar_container = tk.Frame(parent, bg=self.colors['light'])
        calendar_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, 
                               padx=(0, 15))
        
        # 圆角效果（通过边框模拟）
        calendar_container.configure(relief=tk.SOLID, bd=1, 
                                    highlightbackground=self.colors['border'],
                                    highlightthickness=1)
        
        # 星期标题
        days_header = tk.Frame(calendar_container, bg=self.colors['light'], 
                              height=50)
        days_header.pack(fill=tk.X)
        days_header.pack_propagate(False)
        
        tk.Frame(days_header, bg=self.colors['border'], height=1).pack(
            side=tk.BOTTOM, fill=tk.X)
        
        days = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
        for i, day in enumerate(days):
            color = self.colors['danger'] if i >= 5 else self.colors['dark']
            lbl = tk.Label(days_header, text=day, bg=self.colors['light'], 
                          fg=color, font=("Arial", 12, "bold"))
            lbl.pack(side=tk.LEFT, expand=True)
        
        # 日历网格容器
        grid_container = tk.Frame(calendar_container, bg=self.colors['light'])
        grid_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        self.calendar_frame = grid_container
    
    def create_event_panel(self, parent):
        """创建事件面板"""
        panel_width = 360
        panel = tk.Frame(parent, bg=self.colors['light'], width=panel_width)
        panel.pack(side=tk.RIGHT, fill=tk.BOTH)
        panel.pack_propagate(False)
        
        panel.configure(relief=tk.SOLID, bd=1, 
                       highlightbackground=self.colors['border'],
                       highlightthickness=1)
        
        # 面板标题
        header = tk.Frame(panel, bg=self.colors['primary_light'], height=50)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(header, text="事件管理", 
                bg=self.colors['primary_light'],
                fg=self.colors['primary'], 
                font=("Arial", 15, "bold")).pack(pady=12)
        
        # 滚动容器
        canvas = tk.Canvas(panel, bg=self.colors['light'], 
                          highlightthickness=0)
        scrollbar = ttk.Scrollbar(panel, orient="vertical", 
                                 command=canvas.yview)
        scrollable = tk.Frame(canvas, bg=self.colors['light'])
        
        scrollable.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable, anchor="nw", 
                            width=panel_width-20)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 绑定鼠标滚轮
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # ========== 选中日期显示 ==========
        date_card = tk.Frame(scrollable, bg=self.colors['primary_light'])
        date_card.pack(fill=tk.X, padx=15, pady=15)
        
        self.selected_date_label = tk.Label(
            date_card, text="👆 请点击选择日期", 
            bg=self.colors['primary_light'], fg=self.colors['primary'],
            font=("Arial", 12, "bold"), pady=15)
        self.selected_date_label.pack()
        
        # ========== 快速跳转 ==========
        self.create_quick_jump_section(scrollable)
        
        # ========== 添加事件 ==========
        self.create_add_event_section(scrollable)
        
        # ========== 事件列表 ==========
        self.create_event_list_section(scrollable)
        
        # ========== 统计信息 ==========
        self.create_stats_section(scrollable)
    
    def create_quick_jump_section(self, parent):
        """创建快速跳转区域"""
        section = tk.LabelFrame(parent, text="⚡ 快速跳转", 
                               bg=self.colors['light'],
                               font=("Arial", 11, "bold"), 
                               fg=self.colors['dark'],
                               bd=0)
        section.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        btn_frame = tk.Frame(section, bg=self.colors['light'])
        btn_frame.pack(pady=10, padx=10)
        
        quick_btns = [
            ("昨天", -1), ("今天", 0), ("明天", 1),
            ("下周", 7), ("下月", 30)
        ]
        
        for i, (text, days) in enumerate(quick_btns):
            btn = tk.Button(btn_frame, text=text, 
                          command=lambda d=days: self.quick_jump(d),
                          bg=self.colors['grey_light'], 
                          fg=self.colors['dark'],
                          font=("Arial", 10), relief=tk.FLAT,
                          padx=10, pady=6, cursor="hand2",
                          activebackground=self.colors['primary_light'])
            btn.grid(row=i//3, column=i%3, padx=3, pady=3, sticky="ew")
            self.add_hover_effect(btn, self.colors['grey_light'], 
                                self.colors['primary_light'])
        
        for i in range(3):
            btn_frame.grid_columnconfigure(i, weight=1)
    
    def create_add_event_section(self, parent):
        """创建添加事件区域"""
        section = tk.LabelFrame(parent, text="➕ 添加新事件", 
                               bg=self.colors['light'],
                               font=("Arial", 11, "bold"), 
                               fg=self.colors['dark'],
                               bd=0)
        section.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        inner = tk.Frame(section, bg=self.colors['light'])
        inner.pack(fill=tk.X, padx=10, pady=10)
        
        # 标题输入
        tk.Label(inner, text="标题", bg=self.colors['light'],
                fg=self.colors['grey'], font=("Arial", 9)).pack(
                    anchor=tk.W, pady=(0, 4))
        
        self.event_title_entry = tk.Entry(inner, font=("Arial", 11),
                                         relief=tk.FLAT, 
                                         bg=self.colors['grey_light'],
                                         fg=self.colors['dark'])
        self.event_title_entry.pack(fill=tk.X, ipady=8, pady=(0, 12))
        
        # 描述输入
        tk.Label(inner, text="描述", bg=self.colors['light'],
                fg=self.colors['grey'], font=("Arial", 9)).pack(
                    anchor=tk.W, pady=(0, 4))
        
        self.event_desc_entry = tk.Text(inner, height=3, 
                                        font=("Arial", 10),
                                        relief=tk.FLAT, 
                                        bg=self.colors['grey_light'],
                                        fg=self.colors['dark'],
                                        padx=8, pady=8)
        self.event_desc_entry.pack(fill=tk.X, pady=(0, 12))
        
        # 优先级选择
        priority_frame = tk.Frame(inner, bg=self.colors['light'])
        priority_frame.pack(fill=tk.X, pady=(0, 12))
        
        tk.Label(priority_frame, text="优先级", bg=self.colors['light'],
                fg=self.colors['grey'], font=("Arial", 9)).pack(
                    side=tk.LEFT, padx=(0, 10))
        
        self.priority_var = tk.StringVar(value="普通")
        priorities = [("🔴 高", "高"), ("🟡 普通", "普通"), ("🟢 低", "低")]
        
        for text, value in priorities:
            tk.Radiobutton(priority_frame, text=text, 
                          variable=self.priority_var,
                          value=value, bg=self.colors['light'], 
                          font=("Arial", 10),
                          activebackground=self.colors['light'],
                          selectcolor=self.colors['primary_light']).pack(
                              side=tk.LEFT, padx=5)
        
        # 添加按钮
        add_btn = tk.Button(inner, text="✅ 添加事件", 
                           command=self.add_event,
                           bg=self.colors['success'], fg="white", 
                           font=("Arial", 11, "bold"),
                           relief=tk.FLAT, cursor="hand2", 
                           pady=10, activebackground="#059669")
        add_btn.pack(fill=tk.X)
        self.add_hover_effect(add_btn, self.colors['success'], "#059669")
    
    def create_event_list_section(self, parent):
        """创建事件列表区域"""
        section = tk.LabelFrame(parent, text="📋 当日事件", 
                               bg=self.colors['light'],
                               font=("Arial", 11, "bold"), 
                               fg=self.colors['dark'],
                               bd=0)
        section.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        self.event_list_frame = tk.Frame(section, bg=self.colors['light'])
        self.event_list_frame.pack(fill=tk.BOTH, expand=True, 
                                   padx=10, pady=10)
    
    def create_stats_section(self, parent):
        """创建统计信息区域"""
        section = tk.Frame(parent, bg="#FEF3C7")
        section.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        tk.Label(section, text="📊 统计信息", bg="#FEF3C7",
                fg=self.colors['dark'], font=("Arial", 10, "bold")).pack(
                    anchor=tk.W, padx=12, pady=(10, 5))
        
        self.stats_label = tk.Label(section, text="", bg="#FEF3C7",
                                    fg=self.colors['grey'], 
                                    font=("Arial", 9),
                                    justify=tk.LEFT)
        self.stats_label.pack(anchor=tk.W, padx=12, pady=(0, 10))
        
        self.update_stats()
    
    def add_hover_effect(self, button, normal_color, hover_color):
        """添加悬停效果"""
        button.bind("<Enter>", lambda e: button.config(bg=hover_color))
        button.bind("<Leave>", lambda e: button.config(bg=normal_color))
    
    def update_time(self):
        """更新实时时间"""
        now = datetime.now()
        time_str = now.strftime("%H:%M:%S")
        date_str = now.strftime("%Y年%m月%d日")
        weekday = ["一", "二", "三", "四", "五", "六", "日"][now.weekday()]
        
        self.time_label.config(text=time_str)
        self.date_label.config(text=f"{date_str} 星期{weekday}")
        self.root.after(1000, self.update_time)
    
    def update_calendar(self):
        """更新日历显示"""
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()
        
        year = self.current_date.year
        month = self.current_date.month
        self.month_label.config(text=f"{year}年 {month}月")
        
        cal = calendar.monthcalendar(year, month)
        today = datetime.now().date()
        
        for week_num, week in enumerate(cal):
            for day_num, day in enumerate(week):
                if day == 0:
                    # 空白单元格
                    tk.Frame(self.calendar_frame, 
                            bg=self.colors['light']).grid(
                        row=week_num, column=day_num, sticky="nsew", 
                        padx=2, pady=2)
                else:
                    self.create_date_cell(week_num, day_num, day, 
                                         year, month, today)
        
        # 配置网格权重
        for i in range(6):
            self.calendar_frame.grid_rowconfigure(i, weight=1, minsize=80)
        for i in range(7):
            self.calendar_frame.grid_columnconfigure(i, weight=1, minsize=80)
    
    def create_date_cell(self, row, col, day, year, month, today):
        """创建日期单元格"""
        date_obj = datetime(year, month, day).date()
        date_str = date_obj.strftime("%Y-%m-%d")
        
        is_today = (date_obj == today)
        is_selected = (self.selected_date == date_obj)
        is_weekend = (col >= 5)
        has_event = date_str in self.events
        is_past = (date_obj < today)
        
        # 确定样式
        if is_today:
            bg_color = self.colors['primary']
            fg_color = "white"
            font_weight = "bold"
        elif is_selected:
            bg_color = self.colors['primary_light']
            fg_color = self.colors['primary']
            font_weight = "bold"
        elif has_event:
            bg_color = "#FEF3C7"
            fg_color = self.colors['dark']
            font_weight = "normal"
        elif is_weekend:
            bg_color = "#FEE2E2"
            fg_color = self.colors['danger']
            font_weight = "normal"
        elif is_past:
            bg_color = self.colors['grey_light']
            fg_color = self.colors['grey']
            font_weight = "normal"
        else:
            bg_color = self.colors['light']
            fg_color = self.colors['dark']
            font_weight = "normal"
        
        # 创建按钮
        btn = tk.Button(self.calendar_frame, text=str(day),
                       bg=bg_color, fg=fg_color,
                       font=("Arial", 16, font_weight),
                       relief=tk.FLAT, bd=0,
                       cursor="hand2",
                       activebackground=bg_color,
                       command=lambda d=date_obj: self.select_date(d))
        btn.grid(row=row, column=col, sticky="nsew", padx=2, pady=2)
        
        # 事件标记
        if has_event:
            event_count = len(self.events[date_str])
            indicator = tk.Label(btn, text=f"●{event_count}", 
                               bg=bg_color, fg=self.colors['accent'],
                               font=("Arial", 9, "bold"))
            indicator.place(relx=0.82, rely=0.1)
        
        # 悬停效果
        if not is_today:
            hover_bg = self.get_hover_color(bg_color)
            self.add_hover_effect(btn, bg_color, hover_bg)
    
    def get_hover_color(self, color):
        """获取悬停颜色"""
        color_map = {
            self.colors['light']: "#F3F4F6",
            self.colors['grey_light']: "#E5E7EB",
            "#FEE2E2": "#FECACA",
            "#FEF3C7": "#FDE68A",
            self.colors['primary_light']: "#BFDBFE"
        }
        return color_map.get(color, "#E5E7EB")
    
    def select_date(self, date_obj):
        """选择日期"""
        self.selected_date = date_obj
        date_str = date_obj.strftime("%Y年%m月%d日")
        weekday = ["一", "二", "三", "四", "五", "六", "日"][date_obj.weekday()]
        
        today = datetime.now().date()
        if date_obj == today:
            prefix = "📍"
        elif date_obj > today:
            prefix = "➡️"
        else:
            prefix = "⬅️"
        
        self.selected_date_label.config(
            text=f"{prefix} {date_str} 星期{weekday}")
        self.update_calendar()
        self.update_event_list()
    
    def update_event_list(self):
        """更新事件列表"""
        for widget in self.event_list_frame.winfo_children():
            widget.destroy()
        
        if not self.selected_date:
            tk.Label(self.event_list_frame, text="未选择日期", 
                    bg=self.colors['light'], fg=self.colors['grey'],
                    font=("Arial", 11), pady=30).pack()
            return
        
        date_key = self.selected_date.strftime("%Y-%m-%d")
        if date_key not in self.events or not self.events[date_key]:
            tk.Label(self.event_list_frame, text="📭 暂无事件", 
                    bg=self.colors['light'], fg=self.colors['grey'],
                    font=("Arial", 11), pady=30).pack()
            return
        
        for i, event in enumerate(self.events[date_key]):
            self.create_event_card(event, i, date_key)
    
    def create_event_card(self, event, index, date_key):
        """创建事件卡片"""
        # 兼容旧版本字符串格式
        if isinstance(event, str):
            event = {"title": event, "description": "", "priority": "普通"}
        
        card = tk.Frame(self.event_list_frame, bg=self.colors['grey_light'])
        card.pack(fill=tk.X, pady=5)
        
        # 优先级颜色条
        priority_colors = {"高": "#FCA5A5", "普通": "#FCD34D", "低": "#86EFAC"}
        priority = event.get("priority", "普通")
        
        tk.Frame(card, bg=priority_colors.get(priority, "#FCD34D"), 
                width=4).pack(side=tk.LEFT, fill=tk.Y)
        
        # 内容区域
        content = tk.Frame(card, bg=self.colors['grey_light'])
        content.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, 
                    padx=10, pady=10)
        
        # 标题行
        title_frame = tk.Frame(content, bg=self.colors['grey_light'])
        title_frame.pack(fill=tk.X)
        
        priority_emoji = {"高": "🔴", "普通": "🟡", "低": "🟢"}
        tk.Label(title_frame, text=priority_emoji.get(priority, "🟡"),
                bg=self.colors['grey_light'], 
                font=("Arial", 11)).pack(side=tk.LEFT)
        
        title = event.get("title", "未命名事件")
        tk.Label(title_frame, text=title, bg=self.colors['grey_light'],
                font=("Arial", 11, "bold"), fg=self.colors['dark'],
                anchor=tk.W).pack(side=tk.LEFT, fill=tk.X, expand=True, 
                                 padx=8)
        
        # 描述
        desc = event.get("description", "")
        if desc:
            tk.Label(content, text=desc, bg=self.colors['grey_light'],
                    font=("Arial", 10), fg=self.colors['grey'],
                    anchor=tk.W, wraplength=240, 
                    justify=tk.LEFT).pack(fill=tk.X, pady=(8, 0))
        
        # 删除按钮
        del_btn = tk.Button(card, text="🗑️", 
                           bg=self.colors['grey_light'], 
                           fg=self.colors['danger'],
                           font=("Arial", 12), relief=tk.FLAT,
                           cursor="hand2", padx=10,
                           activebackground="#FEE2E2",
                           command=lambda: self.delete_event(date_key, index))
        del_btn.pack(side=tk.RIGHT, padx=5)
        self.add_hover_effect(del_btn, self.colors['grey_light'], "#FEE2E2")
    
    def add_event(self):
        """添加事件"""
        if not self.selected_date:
            messagebox.showwarning("提示", "请先选择日期！")
            return
        
        title = self.event_title_entry.get().strip()
        desc = self.event_desc_entry.get("1.0", tk.END).strip()
        
        if not title:
            messagebox.showwarning("提示", "请输入事件标题！")
            return
        
        date_key = self.selected_date.strftime("%Y-%m-%d")
        if date_key not in self.events:
            self.events[date_key] = []
        
        event_data = {
            "title": title,
            "description": desc,
            "priority": self.priority_var.get(),
            "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        self.events[date_key].append(event_data)
        self.save_events()
        
        self.event_title_entry.delete(0, tk.END)
        self.event_desc_entry.delete("1.0", tk.END)
        self.priority_var.set("普通")
        
        self.update_calendar()
        self.update_event_list()
        self.update_stats()
        messagebox.showinfo("成功", f"事件「{title}」已添加！")
    
    def delete_event(self, date_key, index):
        """删除事件"""
        if messagebox.askyesno("确认删除", "确定要删除这个事件吗？"):
            title = self.events[date_key][index].get("title", "未命名")
            del self.events[date_key][index]
            
            if not self.events[date_key]:
                del self.events[date_key]
            
            self.save_events()
            self.update_calendar()
            self.update_event_list()
            self.update_stats()
            messagebox.showinfo("成功", f"事件「{title}」已删除！")
    
    def update_stats(self):
        """更新统计信息"""
        total_events = sum(len(events) for events in self.events.values())
        total_days = len(self.events)
        
        high_priority = 0
        for events in self.events.values():
            for event in events:
                # 兼容旧版本字符串格式和新版本字典格式
                if isinstance(event, dict) and event.get("priority") == "高":
                    high_priority += 1
        
        stats_text = f"📊 统计信息\n"
        stats_text += f"总事件数: {total_events}\n"
        stats_text += f"有事件天数: {total_days}\n"
        stats_text += f"高优先级: {high_priority}"
        
        self.stats_label.config(text=stats_text)
    
    def quick_jump(self, days):
        """快速跳转"""
        target_date = datetime.now().date() + timedelta(days=days)
        self.current_date = datetime(target_date.year, target_date.month, 
                                     target_date.day)
        self.select_date(target_date)
        self.update_calendar()
    
    def prev_month(self):
        """上一月"""
        self.current_date = self.current_date.replace(day=1) - timedelta(days=1)
        self.update_calendar()
    
    def next_month(self):
        """下一月"""
        self.current_date = (self.current_date.replace(day=28) + 
                            timedelta(days=4)).replace(day=1)
        self.update_calendar()
    
    def prev_year(self):
        """上一年"""
        self.current_date = self.current_date.replace(
            year=self.current_date.year - 1)
        self.update_calendar()
    
    def next_year(self):
        """下一年"""
        self.current_date = self.current_date.replace(
            year=self.current_date.year + 1)
        self.update_calendar()
    
    def go_to_today(self):
        """回到今天"""
        today = datetime.now()
        self.current_date = today
        self.select_date(today.date())
        self.update_calendar()

if __name__ == "__main__":
    root = tk.Tk()
    app = CalendarApp(root)
    root.mainloop()
