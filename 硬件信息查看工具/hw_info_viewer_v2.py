import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import platform
import psutil
import subprocess
import threading
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import io
from PIL import Image as PILImage

class HardwareInfoViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("硬件信息查看工具 Pro")
        self.root.geometry("1000x700")
        self.root.resizable(True, True)
        
        # 数据存储
        self.hardware_data = {}
        
        # 设置样式
        style = ttk.Style()
        style.theme_use('clam')
        
        # 主容器
        main_container = ttk.Frame(root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 左侧面板 - 选项
        left_panel = ttk.LabelFrame(main_container, text="📋 选择查看内容", padding="10")
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 10))
        
        # 标题
        title = ttk.Label(left_panel, text="硬件信息查看工具", 
                         font=('Arial', 14, 'bold'))
        title.pack(pady=(0, 15))
        
        # 复选框变量
        self.check_vars = {
            'cpu': tk.BooleanVar(value=True),
            'memory': tk.BooleanVar(value=True),
            'disk': tk.BooleanVar(value=True),
            'network': tk.BooleanVar(value=True),
            'gpu': tk.BooleanVar(value=True),
            'motherboard': tk.BooleanVar(value=True),
            'system': tk.BooleanVar(value=True)
        }
        
        # 复选框列表
        checks = [
            ('cpu', '🖥️  CPU 信息'),
            ('memory', '🧠 内存信息'),
            ('disk', '💾 硬盘信息'),
            ('network', '🌐 网卡信息'),
            ('gpu', '🎮 GPU 信息'),
            ('motherboard', '🔧 主板信息'),
            ('system', '⚙️  系统信息')
        ]
        
        for key, text in checks:
            cb = ttk.Checkbutton(left_panel, text=text, 
                                variable=self.check_vars[key],
                                style='Custom.TCheckbutton')
            cb.pack(anchor=tk.W, pady=5)
        
        # 全选/取消全选按钮
        select_frame = ttk.Frame(left_panel)
        select_frame.pack(pady=10)
        
        ttk.Button(select_frame, text="全选", 
                  command=self.select_all, width=10).pack(side=tk.LEFT, padx=2)
        ttk.Button(select_frame, text="取消", 
                  command=self.deselect_all, width=10).pack(side=tk.LEFT, padx=2)
        
        # 操作按钮
        ttk.Separator(left_panel, orient='horizontal').pack(fill=tk.X, pady=15)
        
        self.scan_btn = ttk.Button(left_panel, text="🔍 一键查看", 
                                   command=self.start_scan, width=20)
        self.scan_btn.pack(pady=5)
        
        self.export_btn = ttk.Button(left_panel, text="📄 导出PDF报告", 
                                     command=self.export_pdf, width=20,
                                     state='disabled')
        self.export_btn.pack(pady=5)
        
        ttk.Button(left_panel, text="🗑️ 清空内容", 
                  command=self.clear_info, width=20).pack(pady=5)
        
        # 右侧面板 - 信息显示
        right_panel = ttk.Frame(main_container)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # 进度条
        self.progress = ttk.Progressbar(right_panel, mode='indeterminate')
        self.progress.pack(fill=tk.X, pady=(0, 10))
        
        # 信息显示区域
        self.info_text = scrolledtext.ScrolledText(right_panel, 
                                                   width=70, height=35,
                                                   font=('Consolas', 10),
                                                   wrap=tk.WORD)
        self.info_text.pack(fill=tk.BOTH, expand=True)
        
        # 配置文本标签
        self.info_text.tag_config('title', foreground='#2196F3', font=('Arial', 13, 'bold'))
        self.info_text.tag_config('key', foreground='#4CAF50', font=('Consolas', 10, 'bold'))
        self.info_text.tag_config('value', foreground='#333333')
        self.info_text.tag_config('separator', foreground='#999999')
        
        # 状态栏
        self.status_var = tk.StringVar(value="就绪")
        status_bar = ttk.Label(root, textvariable=self.status_var, 
                              relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def select_all(self):
        """全选"""
        for var in self.check_vars.values():
            var.set(True)

    def deselect_all(self):
        """取消全选"""
        for var in self.check_vars.values():
            var.set(False)

    def start_scan(self):
        """开始扫描硬件信息"""
        self.scan_btn.config(state='disabled')
        self.export_btn.config(state='disabled')
        self.progress.start(10)
        self.clear_info()
        self.hardware_data = {}
        
        thread = threading.Thread(target=self.scan_hardware)
        thread.daemon = True
        thread.start()

    def scan_hardware(self):
        """扫描硬件信息"""
        try:
            self.update_status("正在扫描硬件信息...")
            self.append_info("🔍 正在扫描选定的硬件信息...\n\n", 'title')
            
            if self.check_vars['cpu'].get():
                self.get_cpu_info()
            
            if self.check_vars['memory'].get():
                self.get_memory_info()
            
            if self.check_vars['disk'].get():
                self.get_disk_info()
            
            if self.check_vars['network'].get():
                self.get_network_info()
            
            if self.check_vars['gpu'].get():
                self.get_gpu_info()
            
            if self.check_vars['motherboard'].get():
                self.get_motherboard_info()
            
            if self.check_vars['system'].get():
                self.get_system_info()
            
            self.append_info("\n✅ 扫描完成！可以导出PDF报告。\n", 'title')
            self.update_status("扫描完成")
            self.root.after(0, lambda: self.export_btn.config(state='normal'))
            
        except Exception as e:
            self.append_info(f"\n❌ 扫描出错: {str(e)}\n", 'title')
            self.update_status(f"错误: {str(e)}")
        
        finally:
            self.root.after(0, self.progress.stop)
            self.root.after(0, lambda: self.scan_btn.config(state='normal'))

    def get_cpu_info(self):
        """获取CPU信息"""
        self.append_info("=" * 80 + "\n", 'separator')
        self.append_info("🖥️  CPU 信息\n", 'title')
        self.append_info("=" * 80 + "\n", 'separator')
        
        cpu_percent = psutil.cpu_percent(interval=1)
        freq = psutil.cpu_freq()
        
        self.hardware_data['cpu'] = {
            '处理器': platform.processor(),
            '架构': platform.machine(),
            '物理核心数': psutil.cpu_count(logical=False),
            '逻辑核心数': psutil.cpu_count(logical=True),
            '当前频率': f"{freq.current:.2f} MHz",
            '最大频率': f"{freq.max:.2f} MHz",
            'CPU使用率': f"{cpu_percent}%",
            '使用率数值': cpu_percent
        }
        
        for key, value in self.hardware_data['cpu'].items():
            if key != '使用率数值':
                self.append_kv(key, value)
        self.append_info("\n")

    def get_memory_info(self):
        """获取内存信息"""
        self.append_info("=" * 80 + "\n", 'separator')
        self.append_info("🧠 内存信息\n", 'title')
        self.append_info("=" * 80 + "\n", 'separator')
        
        mem = psutil.virtual_memory()
        
        self.hardware_data['memory'] = {
            '总内存': self.format_bytes(mem.total),
            '可用内存': self.format_bytes(mem.available),
            '已用内存': self.format_bytes(mem.used),
            '使用率': f"{mem.percent}%",
            '总内存数值': mem.total,
            '已用数值': mem.used,
            '可用数值': mem.available,
            '使用率数值': mem.percent
        }
        
        self.append_kv("总内存", self.hardware_data['memory']['总内存'])
        self.append_kv("可用内存", self.hardware_data['memory']['可用内存'])
        self.append_kv("已用内存", self.hardware_data['memory']['已用内存'])
        self.append_kv("使用率", self.hardware_data['memory']['使用率'])
        self.append_info("\n")

    def get_disk_info(self):
        """获取硬盘信息"""
        self.append_info("=" * 80 + "\n", 'separator')
        self.append_info("💾 硬盘信息\n", 'title')
        self.append_info("=" * 80 + "\n", 'separator')
        
        self.hardware_data['disk'] = []
        
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                disk_info = {
                    '设备': partition.device,
                    '挂载点': partition.mountpoint,
                    '文件系统': partition.fstype,
                    '总容量': self.format_bytes(usage.total),
                    '已使用': self.format_bytes(usage.used),
                    '可用空间': self.format_bytes(usage.free),
                    '使用率': f"{usage.percent}%",
                    '总容量数值': usage.total,
                    '已用数值': usage.used,
                    '可用数值': usage.free,
                    '使用率数值': usage.percent
                }
                
                self.hardware_data['disk'].append(disk_info)
                
                self.append_info(f"  📁 {partition.device}\n", 'key')
                self.append_kv("    挂载点", partition.mountpoint)
                self.append_kv("    文件系统", partition.fstype)
                self.append_kv("    总容量", disk_info['总容量'])
                self.append_kv("    已使用", disk_info['已使用'])
                self.append_kv("    可用空间", disk_info['可用空间'])
                self.append_kv("    使用率", disk_info['使用率'])
                self.append_info("\n")
            except:
                continue

    def get_network_info(self):
        """获取网卡信息"""
        self.append_info("=" * 80 + "\n", 'separator')
        self.append_info("🌐 网卡信息\n", 'title')
        self.append_info("=" * 80 + "\n", 'separator')
        
        self.hardware_data['network'] = []
        
        addrs = psutil.net_if_addrs()
        stats = psutil.net_if_stats()
        
        for interface_name, interface_addrs in addrs.items():
            net_info = {'接口名': interface_name, 'IPv4': '', 'IPv6': '', 'MAC': '', '状态': '', '速度': ''}
            
            self.append_info(f"  🔌 {interface_name}\n", 'key')
            
            if interface_name in stats:
                stat = stats[interface_name]
                status = "启用" if stat.isup else "禁用"
                speed = f"{stat.speed} Mbps" if stat.speed > 0 else "N/A"
                net_info['状态'] = status
                net_info['速度'] = speed
                self.append_kv("    状态", status)
                self.append_kv("    速度", speed)
            
            for addr in interface_addrs:
                if addr.family == 2:  # IPv4
                    net_info['IPv4'] = addr.address
                    self.append_kv("    IPv4地址", addr.address)
                elif addr.family == 23:  # IPv6
                    net_info['IPv6'] = addr.address[:20] + "..."
                    self.append_kv("    IPv6地址", addr.address)
                elif addr.family == -1 or addr.family == 17:  # MAC
                    net_info['MAC'] = addr.address
                    self.append_kv("    MAC地址", addr.address)
            
            self.hardware_data['network'].append(net_info)
            self.append_info("\n")

    def get_gpu_info(self):
        """获取GPU信息"""
        self.append_info("=" * 80 + "\n", 'separator')
        self.append_info("🎮 GPU 信息\n", 'title')
        self.append_info("=" * 80 + "\n", 'separator')
        
        system = platform.system()
        gpu_info = "未检测到GPU信息"
        
        try:
            if system == "Windows":
                result = subprocess.run(['wmic', 'path', 'win32_VideoController', 'get', 
                                       'name,driverversion,adapterram'], 
                                      capture_output=True, text=True, timeout=5)
                lines = [line.strip() for line in result.stdout.split('\n') if line.strip()]
                if len(lines) > 1:
                    gpu_info = lines[1] if lines[1] else "未检测到独立显卡"
                    self.append_info(f"  🎨 {gpu_info}\n", 'value')
            elif system == "Linux":
                result = subprocess.run(['lspci'], capture_output=True, text=True, timeout=5)
                gpu_lines = [line for line in result.stdout.split('\n') if 'VGA' in line or 'Display' in line]
                if gpu_lines:
                    gpu_info = gpu_lines[0].split(':', 1)[1].strip() if ':' in gpu_lines[0] else gpu_lines[0]
                    self.append_info(f"  🎨 {gpu_info}\n", 'value')
            else:
                gpu_info = "macOS系统GPU信息获取需要特殊权限"
                self.append_info(f"  {gpu_info}\n", 'value')
        except:
            self.append_info("  无法获取GPU信息\n", 'value')
        
        self.hardware_data['gpu'] = {'GPU信息': gpu_info}
        self.append_info("\n")

    def get_motherboard_info(self):
        """获取主板信息"""
        self.append_info("=" * 80 + "\n", 'separator')
        self.append_info("🔧 主板信息\n", 'title')
        self.append_info("=" * 80 + "\n", 'separator')
        
        system = platform.system()
        mb_info = "未检测到主板信息"
        
        try:
            if system == "Windows":
                result = subprocess.run(['wmic', 'baseboard', 'get', 
                                       'manufacturer,product,version'], 
                                      capture_output=True, text=True, timeout=5)
                lines = [line.strip() for line in result.stdout.split('\n') if line.strip()]
                if len(lines) > 1:
                    mb_info = lines[1]
                    self.append_info(f"  {mb_info}\n", 'value')
            elif system == "Linux":
                try:
                    with open('/sys/class/dmi/id/board_vendor', 'r') as f:
                        vendor = f.read().strip()
                    with open('/sys/class/dmi/id/board_name', 'r') as f:
                        name = f.read().strip()
                    mb_info = f"{vendor} {name}"
                    self.append_info(f"  制造商: {vendor}\n  型号: {name}\n", 'value')
                except:
                    self.append_info("  无法获取主板信息\n", 'value')
            else:
                mb_info = "macOS系统主板信息获取受限"
                self.append_info(f"  {mb_info}\n", 'value')
        except:
            self.append_info("  无法获取主板信息\n", 'value')
        
        self.hardware_data['motherboard'] = {'主板信息': mb_info}
        self.append_info("\n")

    def get_system_info(self):
        """获取系统信息"""
        self.append_info("=" * 80 + "\n", 'separator')
        self.append_info("⚙️  系统信息\n", 'title')
        self.append_info("=" * 80 + "\n", 'separator')
        
        boot_time = datetime.fromtimestamp(psutil.boot_time())
        
        self.hardware_data['system'] = {
            '操作系统': f"{platform.system()} {platform.release()}",
            '版本': platform.version(),
            '计算机名': platform.node(),
            '启动时间': boot_time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        for key, value in self.hardware_data['system'].items():
            self.append_kv(key, value)
        self.append_info("\n")

    def export_pdf(self):
        """导出PDF报告"""
        if not self.hardware_data:
            messagebox.showwarning("警告", "请先扫描硬件信息！")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF文件", "*.pdf")],
            initialfile=f"硬件信息报告_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        )
        
        if not filename:
            return
        
        self.update_status("正在生成PDF报告...")
        self.export_btn.config(state='disabled')
        
        thread = threading.Thread(target=self.generate_pdf, args=(filename,))
        thread.daemon = True
        thread.start()

    def generate_pdf(self, filename):
        """生成PDF报告"""
        try:
            # 注册中文字体（使用系统自带字体）
            import sys
            if sys.platform == 'win32':
                # Windows系统
                font_path = 'C:/Windows/Fonts/msyh.ttc'  # 微软雅黑
                try:
                    pdfmetrics.registerFont(TTFont('ChineseFont', font_path))
                except:
                    font_path = 'C:/Windows/Fonts/simsun.ttc'  # 宋体
                    try:
                        pdfmetrics.registerFont(TTFont('ChineseFont', font_path))
                    except:
                        # 如果都失败，使用Helvetica
                        pass
            elif sys.platform == 'darwin':
                # macOS系统
                font_path = '/System/Library/Fonts/PingFang.ttc'
                try:
                    pdfmetrics.registerFont(TTFont('ChineseFont', font_path))
                except:
                    pass
            else:
                # Linux系统
                font_path = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
                try:
                    pdfmetrics.registerFont(TTFont('ChineseFont', font_path))
                except:
                    pass
            
            doc = SimpleDocTemplate(filename, pagesize=A4)
            story = []
            styles = getSampleStyleSheet()
            
            # 自定义中文样式
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontName='ChineseFont',
                fontSize=24,
                textColor=colors.HexColor('#2196F3'),
                spaceAfter=30,
                alignment=TA_CENTER
            )
            
            heading2_style = ParagraphStyle(
                'ChineseHeading2',
                parent=styles['Heading2'],
                fontName='ChineseFont',
                fontSize=16,
                textColor=colors.HexColor('#1976D2'),
                spaceAfter=12,
                spaceBefore=12
            )
            
            normal_style = ParagraphStyle(
                'ChineseNormal',
                parent=styles['Normal'],
                fontName='ChineseFont',
                fontSize=10,
                leading=14
            )
            
            story.append(Paragraph("硬件信息分析报告", title_style))
            story.append(Paragraph(f"报告生成时间：{datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}", 
                                 normal_style))
            story.append(Spacer(1, 0.3*inch))
            
            # CPU信息和图表
            if 'cpu' in self.hardware_data:
                story.append(Paragraph("CPU 信息", heading2_style))
                
                cpu_data = [['项目', '详情']]
                for k, v in self.hardware_data['cpu'].items():
                    if k != '使用率数值':
                        cpu_data.append([k, str(v)])
                
                cpu_table = Table(cpu_data, colWidths=[2.5*inch, 3.5*inch])
                cpu_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2196F3')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, -1), 'ChineseFont'),
                    ('FONTSIZE', (0, 0), (-1, 0), 12),
                    ('FONTSIZE', (0, 1), (-1, -1), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.lightblue),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.lightblue, colors.white])
                ]))
                story.append(cpu_table)
                story.append(Spacer(1, 0.2*inch))
                
                # CPU使用率饼图
                if '使用率数值' in self.hardware_data['cpu']:
                    usage = self.hardware_data['cpu']['使用率数值']
                    
                    # 添加中文标题（使用Paragraph代替String）
                    story.append(Paragraph("CPU使用率分布图", normal_style))
                    story.append(Spacer(1, 0.1*inch))
                    
                    drawing = Drawing(400, 180)
                    pie = Pie()
                    pie.x = 150
                    pie.y = 40
                    pie.width = 100
                    pie.height = 100
                    pie.data = [usage, 100-usage]
                    # 使用英文标签避免图表内乱码
                    pie.labels = [f'{usage:.1f}%', f'{100-usage:.1f}%']
                    pie.slices[0].fillColor = colors.HexColor('#FF5252')
                    pie.slices[1].fillColor = colors.HexColor('#4CAF50')
                    drawing.add(pie)
                    
                    # 添加图例说明
                    from reportlab.graphics.shapes import Rect, String
                    # 已使用图例
                    legend1_rect = Rect(50, 150, 15, 15, fillColor=colors.HexColor('#FF5252'))
                    drawing.add(legend1_rect)
                    legend1_text = String(70, 155, 'Used', fontSize=10)
                    drawing.add(legend1_text)
                    # 空闲图例
                    legend2_rect = Rect(120, 150, 15, 15, fillColor=colors.HexColor('#4CAF50'))
                    drawing.add(legend2_rect)
                    legend2_text = String(140, 155, 'Free', fontSize=10)
                    drawing.add(legend2_text)
                    
                    story.append(drawing)
                    story.append(Spacer(1, 0.2*inch))
            
            # 内存信息和图表
            if 'memory' in self.hardware_data:
                story.append(Paragraph("内存信息", heading2_style))
                
                mem_display_data = [['项目', '详情'],
                                   ['总内存', self.hardware_data['memory']['总内存']],
                                   ['可用内存', self.hardware_data['memory']['可用内存']],
                                   ['已用内存', self.hardware_data['memory']['已用内存']],
                                   ['使用率', self.hardware_data['memory']['使用率']]]
                
                mem_table = Table(mem_display_data, colWidths=[2.5*inch, 3.5*inch])
                mem_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4CAF50')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, -1), 'ChineseFont'),
                    ('FONTSIZE', (0, 0), (-1, 0), 12),
                    ('FONTSIZE', (0, 1), (-1, -1), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.lightgreen),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.lightgreen, colors.white])
                ]))
                story.append(mem_table)
                story.append(Spacer(1, 0.2*inch))
                
                # 内存使用饼图
                story.append(Paragraph("内存使用分布图", normal_style))
                story.append(Spacer(1, 0.1*inch))
                
                drawing = Drawing(400, 180)
                pie = Pie()
                pie.x = 150
                pie.y = 40
                pie.width = 100
                pie.height = 100
                used = self.hardware_data['memory']['已用数值']
                available = self.hardware_data['memory']['可用数值']
                used_gb = used / (1024**3)
                available_gb = available / (1024**3)
                pie.data = [used, available]
                # 使用英文标签和数值
                pie.labels = [f'{used_gb:.1f}GB', f'{available_gb:.1f}GB']
                pie.slices[0].fillColor = colors.HexColor('#2196F3')
                pie.slices[1].fillColor = colors.HexColor('#4CAF50')
                drawing.add(pie)
                
                from reportlab.graphics.shapes import Rect, String
                # 已使用图例
                legend1_rect = Rect(50, 150, 15, 15, fillColor=colors.HexColor('#2196F3'))
                drawing.add(legend1_rect)
                legend1_text = String(70, 155, 'Used', fontSize=10)
                drawing.add(legend1_text)
                # 可用图例
                legend2_rect = Rect(120, 150, 15, 15, fillColor=colors.HexColor('#4CAF50'))
                drawing.add(legend2_rect)
                legend2_text = String(140, 155, 'Available', fontSize=10)
                drawing.add(legend2_text)
                
                story.append(drawing)
                story.append(Spacer(1, 0.2*inch))
            
            # 硬盘信息
            if 'disk' in self.hardware_data and self.hardware_data['disk']:
                story.append(PageBreak())
                story.append(Paragraph("硬盘信息", heading2_style))
                
                for idx, disk in enumerate(self.hardware_data['disk'], 1):
                    story.append(Paragraph(f"磁盘 {idx}", normal_style))
                    story.append(Spacer(1, 0.1*inch))
                    
                    disk_data = [
                        ['项目', '详情'],
                        ['设备', disk['设备']],
                        ['挂载点', disk['挂载点']],
                        ['文件系统', disk['文件系统']],
                        ['总容量', disk['总容量']],
                        ['已使用', disk['已使用']],
                        ['可用空间', disk['可用空间']],
                        ['使用率', disk['使用率']]
                    ]
                    
                    disk_table = Table(disk_data, colWidths=[2*inch, 4*inch])
                    disk_table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#FF9800')),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                        ('FONTNAME', (0, 0), (-1, -1), 'ChineseFont'),
                        ('FONTSIZE', (0, 0), (-1, 0), 11),
                        ('FONTSIZE', (0, 1), (-1, -1), 9),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.Color(1, 0.95, 0.8)),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black),
                        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.Color(1, 0.95, 0.8), colors.white])
                    ]))
                    story.append(disk_table)
                    story.append(Spacer(1, 0.15*inch))
                    
                    # 硬盘使用率条形图
                    story.append(Paragraph(f"磁盘 {idx} 空间使用情况", normal_style))
                    story.append(Spacer(1, 0.1*inch))
                    
                    drawing = Drawing(400, 180)
                    bar = VerticalBarChart()
                    bar.x = 100
                    bar.y = 40
                    bar.height = 120
                    bar.width = 200
                    bar.data = [[disk['使用率数值'], 100-disk['使用率数值']]]
                    bar.categoryAxis.categoryNames = ['Used', 'Free']
                    bar.categoryAxis.labels.fontSize = 10
                    bar.valueAxis.valueMin = 0
                    bar.valueAxis.valueMax = 100
                    bar.valueAxis.labels.fontSize = 9
                    bar.bars[0].fillColor = colors.HexColor('#FF9800')
                    bar.bars[1].fillColor = colors.HexColor('#4CAF50')
                    drawing.add(bar)
                    
                    # 添加百分比标注
                    from reportlab.graphics.shapes import String
                    used_label = String(150, 165, f'{disk["使用率数值"]:.1f}%', 
                                      fontSize=11, textAnchor='middle', fontName='Helvetica-Bold')
                    drawing.add(used_label)
                    
                    story.append(drawing)
                    story.append(Spacer(1, 0.2*inch))
            
            # 网卡信息
            if 'network' in self.hardware_data and self.hardware_data['network']:
                story.append(PageBreak())
                story.append(Paragraph("网卡信息", heading2_style))
                
                net_data = [['网卡名称', 'IPv4地址', 'MAC地址', '状态', '速度']]
                for net in self.hardware_data['network']:
                    net_data.append([
                        net['接口名'],
                        net['IPv4'] if net['IPv4'] else '-',
                        net['MAC'] if net['MAC'] else '-',
                        net['状态'],
                        net['速度']
                    ])
                
                net_table = Table(net_data, colWidths=[1.5*inch, 1.5*inch, 1.5*inch, 0.8*inch, 0.8*inch])
                net_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#9C27B0')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, -1), 'ChineseFont'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('FONTSIZE', (0, 1), (-1, -1), 8),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.lavender),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.lavender, colors.white])
                ]))
                story.append(net_table)
                story.append(Spacer(1, 0.3*inch))
            
            # GPU信息
            if 'gpu' in self.hardware_data:
                story.append(Paragraph("GPU 信息", heading2_style))
                story.append(Paragraph(self.hardware_data['gpu']['GPU信息'], normal_style))
                story.append(Spacer(1, 0.3*inch))
            
            # 主板信息
            if 'motherboard' in self.hardware_data:
                story.append(Paragraph("主板信息", heading2_style))
                story.append(Paragraph(self.hardware_data['motherboard']['主板信息'], normal_style))
                story.append(Spacer(1, 0.3*inch))
            
            # 系统信息
            if 'system' in self.hardware_data:
                story.append(Paragraph("系统信息", heading2_style))
                
                sys_data = [['项目', '详情']]
                for k, v in self.hardware_data['system'].items():
                    sys_data.append([k, str(v)])
                    
                sys_table = Table(sys_data, colWidths=[2.5*inch, 3.5*inch])
                sys_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#607D8B')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, -1), 'ChineseFont'),
                    ('FONTSIZE', (0, 0), (-1, 0), 12),
                    ('FONTSIZE', (0, 1), (-1, -1), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.lightgrey, colors.white])
                ]))
                story.append(sys_table)
            
            # 生成PDF
            doc.build(story)
            
            self.root.after(0, lambda: messagebox.showinfo("成功", f"PDF报告已导出到:\n{filename}"))
            self.update_status("PDF报告生成成功")
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("错误", f"生成PDF失败:\n{str(e)}"))
            self.update_status(f"PDF生成失败: {str(e)}")
        
        finally:
            self.root.after(0, lambda: self.export_btn.config(state='normal'))

    def append_info(self, text, tag=None):
        """添加信息到文本框"""
        def _append():
            self.info_text.insert(tk.END, text, tag)
            self.info_text.see(tk.END)
        self.root.after(0, _append)

    def append_kv(self, key, value):
        """添加键值对"""
        self.append_info(f"  {key}: ", 'key')
        self.append_info(f"{value}\n", 'value')

    def clear_info(self):
        """清空信息"""
        self.info_text.delete(1.0, tk.END)
        self.hardware_data = {}
        self.export_btn.config(state='disabled')
        self.update_status("就绪")

    def update_status(self, message):
        """更新状态栏"""
        self.root.after(0, lambda: self.status_var.set(message))

    @staticmethod
    def format_bytes(bytes):
        """格式化字节大小"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes < 1024.0:
                return f"{bytes:.2f} {unit}"
            bytes /= 1024.0
        return f"{bytes:.2f} PB"

def main():
    root = tk.Tk()
    app = HardwareInfoViewer(root)
    root.mainloop()

if __name__ == "__main__":
    main()