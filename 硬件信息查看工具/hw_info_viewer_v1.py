import tkinter as tk
from tkinter import ttk, scrolledtext
import platform
import psutil
import subprocess
import threading

class HardwareInfoViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("硬件信息查看工具")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # 设置样式
        style = ttk.Style()
        style.theme_use('clam')
        
        # 主框架
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 标题
        title = ttk.Label(main_frame, text="💻 硬件信息查看工具", 
                         font=('Arial', 16, 'bold'))
        title.grid(row=0, column=0, pady=(0, 10))
        
        # 按钮框架
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=1, column=0, pady=(0, 10))
        
        # 一键查看按钮
        self.scan_btn = ttk.Button(btn_frame, text="🔍 一键查看硬件信息", 
                                   command=self.start_scan, width=25)
        self.scan_btn.grid(row=0, column=0, padx=5)
        
        # 清空按钮
        clear_btn = ttk.Button(btn_frame, text="🗑️ 清空", 
                              command=self.clear_info, width=15)
        clear_btn.grid(row=0, column=1, padx=5)
        
        # 进度条
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # 信息显示区域
        self.info_text = scrolledtext.ScrolledText(main_frame, 
                                                   width=90, height=30,
                                                   font=('Consolas', 10),
                                                   wrap=tk.WORD)
        self.info_text.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置网格权重
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
        # 配置文本标签
        self.info_text.tag_config('title', foreground='#2196F3', font=('Arial', 12, 'bold'))
        self.info_text.tag_config('key', foreground='#4CAF50', font=('Consolas', 10, 'bold'))
        self.info_text.tag_config('value', foreground='#333333')
        self.info_text.tag_config('separator', foreground='#999999')

    def start_scan(self):
        """开始扫描硬件信息"""
        self.scan_btn.config(state='disabled')
        self.progress.start(10)
        self.clear_info()
        
        # 在新线程中执行扫描
        thread = threading.Thread(target=self.scan_hardware)
        thread.daemon = True
        thread.start()

    def scan_hardware(self):
        """扫描硬件信息"""
        try:
            self.append_info("正在扫描硬件信息...\n\n", 'title')
            
            # CPU信息
            self.get_cpu_info()
            
            # 内存信息
            self.get_memory_info()
            
            # 硬盘信息
            self.get_disk_info()
            
            # 网卡信息
            self.get_network_info()
            
            # GPU信息
            self.get_gpu_info()
            
            # 主板信息
            self.get_motherboard_info()
            
            # 系统信息
            self.get_system_info()
            
            self.append_info("\n✅ 扫描完成！\n", 'title')
            
        except Exception as e:
            self.append_info(f"\n❌ 扫描出错: {str(e)}\n", 'title')
        
        finally:
            self.root.after(0, self.progress.stop)
            self.root.after(0, lambda: self.scan_btn.config(state='normal'))

    def get_cpu_info(self):
        """获取CPU信息"""
        self.append_info("=" * 80 + "\n", 'separator')
        self.append_info("🖥️  CPU 信息\n", 'title')
        self.append_info("=" * 80 + "\n", 'separator')
        
        self.append_kv("处理器", platform.processor())
        self.append_kv("架构", platform.machine())
        self.append_kv("物理核心数", psutil.cpu_count(logical=False))
        self.append_kv("逻辑核心数", psutil.cpu_count(logical=True))
        self.append_kv("当前频率", f"{psutil.cpu_freq().current:.2f} MHz")
        self.append_kv("最大频率", f"{psutil.cpu_freq().max:.2f} MHz")
        self.append_kv("CPU使用率", f"{psutil.cpu_percent(interval=1)}%")
        self.append_info("\n")

    def get_memory_info(self):
        """获取内存信息"""
        self.append_info("=" * 80 + "\n", 'separator')
        self.append_info("🧠 内存信息\n", 'title')
        self.append_info("=" * 80 + "\n", 'separator')
        
        mem = psutil.virtual_memory()
        self.append_kv("总内存", self.format_bytes(mem.total))
        self.append_kv("可用内存", self.format_bytes(mem.available))
        self.append_kv("已用内存", self.format_bytes(mem.used))
        self.append_kv("使用率", f"{mem.percent}%")
        self.append_info("\n")

    def get_disk_info(self):
        """获取硬盘信息"""
        self.append_info("=" * 80 + "\n", 'separator')
        self.append_info("💾 硬盘信息\n", 'title')
        self.append_info("=" * 80 + "\n", 'separator')
        
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                self.append_info(f"  📁 {partition.device}\n", 'key')
                self.append_kv("    挂载点", partition.mountpoint)
                self.append_kv("    文件系统", partition.fstype)
                self.append_kv("    总容量", self.format_bytes(usage.total))
                self.append_kv("    已使用", self.format_bytes(usage.used))
                self.append_kv("    可用空间", self.format_bytes(usage.free))
                self.append_kv("    使用率", f"{usage.percent}%")
                self.append_info("\n")
            except:
                continue

    def get_network_info(self):
        """获取网卡信息"""
        self.append_info("=" * 80 + "\n", 'separator')
        self.append_info("🌐 网卡信息\n", 'title')
        self.append_info("=" * 80 + "\n", 'separator')
        
        addrs = psutil.net_if_addrs()
        stats = psutil.net_if_stats()
        
        for interface_name, interface_addrs in addrs.items():
            self.append_info(f"  🔌 {interface_name}\n", 'key')
            
            if interface_name in stats:
                stat = stats[interface_name]
                self.append_kv("    状态", "启用" if stat.isup else "禁用")
                self.append_kv("    速度", f"{stat.speed} Mbps" if stat.speed > 0 else "N/A")
            
            for addr in interface_addrs:
                if addr.family == 2:  # IPv4
                    self.append_kv("    IPv4地址", addr.address)
                    self.append_kv("    子网掩码", addr.netmask)
                elif addr.family == 23:  # IPv6
                    self.append_kv("    IPv6地址", addr.address)
                elif addr.family == -1 or addr.family == 17:  # MAC
                    self.append_kv("    MAC地址", addr.address)
            
            self.append_info("\n")

    def get_gpu_info(self):
        """获取GPU信息"""
        self.append_info("=" * 80 + "\n", 'separator')
        self.append_info("🎮 GPU 信息\n", 'title')
        self.append_info("=" * 80 + "\n", 'separator')
        
        system = platform.system()
        
        try:
            if system == "Windows":
                result = subprocess.run(['wmic', 'path', 'win32_VideoController', 'get', 
                                       'name,driverversion,adapterram'], 
                                      capture_output=True, text=True, timeout=5)
                lines = [line.strip() for line in result.stdout.split('\n') if line.strip()]
                if len(lines) > 1:
                    for line in lines[1:]:
                        if line:
                            self.append_info(f"  🎨 {line}\n", 'value')
                else:
                    self.append_info("  未检测到独立显卡\n", 'value')
            elif system == "Linux":
                result = subprocess.run(['lspci'], capture_output=True, text=True, timeout=5)
                gpu_lines = [line for line in result.stdout.split('\n') if 'VGA' in line or 'Display' in line]
                if gpu_lines:
                    for line in gpu_lines:
                        self.append_info(f"  🎨 {line.split(':', 1)[1].strip() if ':' in line else line}\n", 'value')
                else:
                    self.append_info("  未检测到显卡信息\n", 'value')
            else:
                self.append_info("  macOS系统GPU信息获取需要特殊权限\n", 'value')
        except:
            self.append_info("  无法获取GPU信息\n", 'value')
        
        self.append_info("\n")

    def get_motherboard_info(self):
        """获取主板信息"""
        self.append_info("=" * 80 + "\n", 'separator')
        self.append_info("🔧 主板信息\n", 'title')
        self.append_info("=" * 80 + "\n", 'separator')
        
        system = platform.system()
        
        try:
            if system == "Windows":
                result = subprocess.run(['wmic', 'baseboard', 'get', 
                                       'manufacturer,product,version'], 
                                      capture_output=True, text=True, timeout=5)
                lines = [line.strip() for line in result.stdout.split('\n') if line.strip()]
                if len(lines) > 1:
                    self.append_info(f"  {lines[1]}\n", 'value')
                else:
                    self.append_info("  无法获取主板信息\n", 'value')
            elif system == "Linux":
                try:
                    with open('/sys/class/dmi/id/board_vendor', 'r') as f:
                        vendor = f.read().strip()
                    with open('/sys/class/dmi/id/board_name', 'r') as f:
                        name = f.read().strip()
                    self.append_info(f"  制造商: {vendor}\n  型号: {name}\n", 'value')
                except:
                    self.append_info("  无法获取主板信息\n", 'value')
            else:
                self.append_info("  macOS系统主板信息获取受限\n", 'value')
        except:
            self.append_info("  无法获取主板信息\n", 'value')
        
        self.append_info("\n")

    def get_system_info(self):
        """获取系统信息"""
        self.append_info("=" * 80 + "\n", 'separator')
        self.append_info("⚙️  系统信息\n", 'title')
        self.append_info("=" * 80 + "\n", 'separator')
        
        self.append_kv("操作系统", f"{platform.system()} {platform.release()}")
        self.append_kv("版本", platform.version())
        self.append_kv("计算机名", platform.node())
        
        import datetime
        boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
        self.append_kv("启动时间", boot_time.strftime("%Y-%m-%d %H:%M:%S"))
        self.append_info("\n")

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
