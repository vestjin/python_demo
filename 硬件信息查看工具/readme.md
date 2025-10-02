# 💻 硬件信息查看工具 Pro

<div align="center">

![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)

一款简洁、轻量、功能强大的硬件信息查看工具

[功能特性](#-功能特性) • [安装说明](#-安装说明) • [使用方法](#-使用方法) • [截图展示](#-截图展示) • [常见问题](#-常见问题)

</div>

---

## 📋 目录

- [功能特性](#-功能特性)
- [系统要求](#-系统要求)
- [安装说明](#-安装说明)
- [使用方法](#-使用方法)
- [功能详解](#-功能详解)
- [PDF报告说明](#-pdf报告说明)
- [截图展示](#-截图展示)
- [常见问题](#-常见问题)
- [更新日志](#-更新日志)
- [许可证](#-许可证)

---

## ✨ 功能特性

### 🎯 核心功能

- **一键查看** - 快速扫描并显示所有硬件信息
- **选择性查看** - 自由选择需要查看的硬件类型
- **PDF导出** - 生成专业的硬件信息分析报告
- **图形分析** - 内置饼图、条形图等可视化图表
- **跨平台支持** - 支持 Windows、Linux、macOS

### 🖥️ 硬件信息覆盖

| 硬件类型 | 信息内容 |
|---------|---------|
| 🖥️ **CPU** | 处理器型号、架构、核心数、频率、使用率 |
| 🧠 **内存** | 总容量、可用容量、已用容量、使用率 |
| 💾 **硬盘** | 设备名称、文件系统、容量、使用情况 |
| 🌐 **网卡** | 网卡名称、IP地址、MAC地址、连接状态、速度 |
| 🎮 **GPU** | 显卡型号、驱动版本、显存信息 |
| 🔧 **主板** | 制造商、型号、版本信息 |
| ⚙️ **系统** | 操作系统、版本、计算机名、启动时间 |

### 📊 可视化图表

- **CPU使用率饼图** - 直观显示CPU占用情况
- **内存使用饼图** - 清晰展示内存分配状态
- **硬盘空间条形图** - 对比各磁盘使用率
- **彩色分类表格** - 不同硬件类型使用不同主题色

---

## 💻 系统要求

### 支持的操作系统

- ✅ Windows 7/8/10/11
- ✅ macOS 10.12+
- ✅ Linux (Ubuntu, Debian, CentOS, Fedora 等)

### Python 版本

- Python 3.7 或更高版本

### 依赖库

- `psutil` - 系统和进程工具库
- `reportlab` - PDF生成库
- `pillow` - 图像处理库
- `tkinter` - GUI界面库（Python自带）

---

## 📦 安装说明

### 方法一：使用 pip 安装依赖

```bash
# 克隆或下载项目
git clone https://github.com/vestjin/python_demo.git
cd python_demo\硬件信息查看工具

# 安装依赖
pip install -r requirements.txt
```

**requirements.txt 内容：**
```
psutil>=5.9.0
reportlab>=3.6.0
pillow>=9.0.0
```

### 方法二：手动安装依赖

```bash
pip install psutil reportlab pillow
```

### 验证安装

```bash
python --version  # 确认Python版本
python -c "import psutil, reportlab, PIL; print('依赖安装成功！')"
```

---

## 🚀 使用方法

### 快速开始

1. **启动程序**
   ```bash
   python hw_info_viewer.py
   ```

2. **选择要查看的硬件**
   - 在左侧面板勾选需要查看的硬件类型
   - 支持全选/取消全选操作

3. **一键扫描**
   - 点击 **"🔍 一键查看"** 按钮
   - 等待扫描完成（通常1-3秒）

4. **查看结果**
   - 右侧面板实时显示硬件信息
   - 支持滚动查看详细内容

5. **导出PDF报告**
   - 点击 **"📄 导出PDF报告"** 按钮
   - 选择保存路径和文件名
   - 等待生成完成

### 界面布局

```
┌─────────────────────────────────────────────────────────┐
│  硬件信息查看工具 Pro                                      │
├──────────────┬──────────────────────────────────────────┤
│ 📋 选择内容   │  ═══════ 进度条 ═══════                   │
│              │                                          │
│ ☑ CPU 信息   │  ┌────────────────────────────────────┐ │
│ ☑ 内存信息   │  │                                    │ │
│ ☑ 硬盘信息   │  │   硬件信息显示区域                  │ │
│ ☑ 网卡信息   │  │                                    │ │
│ ☑ GPU 信息   │  │   支持滚动查看                      │ │
│ ☑ 主板信息   │  │                                    │ │
│ ☑ 系统信息   │  │                                    │ │
│              │  └────────────────────────────────────┘ │
│ [全选][取消] │                                          │
│              │                                          │
│ 🔍 一键查看   │                                          │
│ 📄 导出PDF    │                                          │
│ 🗑️ 清空内容   │                                          │
└──────────────┴──────────────────────────────────────────┤
│ 状态栏: 就绪                                              │
└─────────────────────────────────────────────────────────┘
```

---

## 🔧 功能详解

### 1. 选择性查看

#### 全选 / 取消全选
- 快速勾选或取消所有硬件类型
- 适合快速切换查看模式

#### 自定义选择
- 只查看特定硬件信息
- 提升扫描速度
- 减少不必要的系统调用

**使用场景：**
- 只想查看CPU和内存 → 仅勾选这两项
- 需要完整报告 → 点击"全选"
- 快速检测硬盘 → 仅勾选"硬盘信息"

### 2. 实时扫描

#### 扫描过程
1. 点击"一键查看"按钮
2. 进度条开始滚动（表示正在扫描）
3. 信息逐条显示在右侧面板
4. 扫描完成后显示 ✅ 提示

#### 扫描性能
- **速度快**：通常1-3秒完成全部扫描
- **准确性高**：直接调用系统API
- **资源占用低**：轻量级设计

### 3. PDF报告生成

#### 报告内容

**封面**
- 报告标题：硬件信息分析报告
- 生成时间：精确到秒
- 专业排版

**详细信息页**

每个硬件类型包含：
- 📋 **数据表格** - 清晰的键值对展示
- 📊 **可视化图表** - 饼图、条形图
- 🎨 **彩色分类** - 不同硬件使用不同颜色主题

**图表说明**

| 图表类型 | 用途 | 颜色方案 |
|---------|------|---------|
| CPU饼图 | 使用率分布 | 红色(已用) + 绿色(空闲) |
| 内存饼图 | 容量分配 | 蓝色(已用) + 绿色(可用) |
| 硬盘条形图 | 空间对比 | 橙色(已用) + 绿色(可用) |

#### 报告特色

✨ **专业排版**
- 自动分页，避免内容截断
- 统一的字体和样式
- 清晰的层次结构

🎨 **彩色主题**
- CPU：蓝色主题
- 内存：绿色主题
- 硬盘：橙色主题
- 网卡：紫色主题
- 系统：灰色主题

📊 **数据可视化**
- 饼图显示百分比
- 条形图对比数据
- 表格展示详细信息

🌍 **中文支持**
- 自动检测系统字体
- Windows使用微软雅黑或宋体
- macOS使用苹方字体
- Linux使用文泉驿正黑

---

## 📄 PDF报告说明

### 报告结构

```
📄 硬件信息分析报告.pdf
│
├─ 📑 封面
│  ├─ 报告标题
│  └─ 生成时间
│
├─ 🖥️ CPU信息
│  ├─ 详细参数表格
│  └─ 使用率饼图
│
├─ 🧠 内存信息
│  ├─ 容量信息表格
│  └─ 使用分布饼图
│
├─ 💾 硬盘信息（分页）
│  ├─ 磁盘1信息 + 使用率条形图
│  ├─ 磁盘2信息 + 使用率条形图
│  └─ ...
│
├─ 🌐 网卡信息
│  └─ 网卡列表表格
│
├─ 🎮 GPU信息
│  └─ 显卡详情
│
├─ 🔧 主板信息
│  └─ 主板型号
│
└─ ⚙️ 系统信息
   └─ 系统详情表格
```

### 字体支持

**Windows系统**
- 优先使用：微软雅黑 (`C:/Windows/Fonts/msyh.ttc`)
- 备用字体：宋体 (`C:/Windows/Fonts/simsun.ttc`)

**macOS系统**
- 使用：苹方字体 (`/System/Library/Fonts/PingFang.ttc`)

**Linux系统**
- 使用：文泉驿正黑 (`/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc`)
- 需要安装：`sudo apt-get install fonts-wqy-zenhei`

### 图表说明

**图例含义**
- 🟥 红色：CPU已使用
- 🟩 绿色：CPU/内存/硬盘空闲
- 🟦 蓝色：内存已使用
- 🟧 橙色：硬盘已使用

**数值标注**
- 饼图：显示百分比或容量（GB）
- 条形图：显示使用率百分比
- 表格：显示完整的详细信息

---

## 📸 截图展示

### 主界面
```
┌──────────────────────────────────────────────────┐
│  💻 硬件信息查看工具 Pro                          │
├──────────────┬───────────────────────────────────┤
│ 选择内容     │  显示区域                          │
│              │                                   │
│ [√] CPU      │  ═══════════════════              │
│ [√] 内存     │                                   │
│ [√] 硬盘     │  🖥️ CPU 信息                      │
│ [√] 网卡     │  处理器: Intel Core i7-10700K     │
│ [√] GPU      │  物理核心: 8                      │
│ [√] 主板     │  逻辑核心: 16                     │
│ [√] 系统     │  CPU使用率: 25.3%                 │
│              │                                   │
│ [全选][取消] │  🧠 内存信息                      │
│              │  总内存: 16.00 GB                 │
│ 🔍 一键查看  │  可用内存: 8.52 GB                │
│ 📄 导出PDF   │  使用率: 46.8%                    │
│ 🗑️ 清空     │                                   │
└──────────────┴───────────────────────────────────┘
```

### PDF报告示例

**第1页 - 封面**
```
╔════════════════════════════════════════╗
║                                        ║
║      硬件信息分析报告                   ║
║                                        ║
║   报告生成时间：2025年10月01日 14:30   ║
║                                        ║
╚════════════════════════════════════════╝
```

**第2页 - CPU信息**
```
┌─────────────────────────────────────┐
│ CPU 信息                            │
├──────────────┬──────────────────────┤
│ 处理器       │ Intel Core i7-10700K │
│ 架构         │ AMD64                │
│ 物理核心数   │ 8                    │
│ 逻辑核心数   │ 16                   │
│ CPU使用率    │ 25.3%                │
└──────────────┴──────────────────────┘

      CPU使用率分布图
     ┌──────────────┐
     │   ●●●●●      │  🟥 Used  25.3%
     │ ●●    ●●●    │  🟩 Free  74.7%
     │●        ●●   │
     │●          ●  │
     │ ●●●●●●●●●    │
     └──────────────┘
```

---

## ❓ 常见问题

### Q1: 程序无法启动？

**A:** 请检查：
1. Python版本是否 ≥ 3.7
   ```bash
   python --version
   ```
2. 依赖是否正确安装
   ```bash
   pip list | grep psutil
   pip list | grep reportlab
   ```
3. 是否有tkinter支持
   ```bash
   python -c "import tkinter"
   ```

**Ubuntu/Debian用户安装tkinter：**
```bash
sudo apt-get install python3-tk
```

### Q2: 扫描时卡住不动？

**A:** 可能原因：
- 系统权限不足
- 某些硬件信息获取超时

**解决方法：**
- Windows：以管理员身份运行
- Linux/macOS：使用 `sudo python hardware_info_viewer.py`
- 取消勾选导致问题的硬件类型

### Q3: PDF导出失败？

**A:** 检查项目：

1. **中文字体缺失**
   - Windows：确认系统有微软雅黑或宋体
   - Linux：安装中文字体
     ```bash
     sudo apt-get install fonts-wqy-zenhei
     ```

2. **权限问题**
   - 确保保存路径有写入权限
   - 尝试保存到桌面或文档文件夹

3. **磁盘空间不足**
   - 确保至少有10MB可用空间

### Q4: 图表中文显示为方块？

**A:** 已修复！最新版本：
- 图表标题使用Paragraph组件（支持中文）
- 图表内使用英文标签 + 数值
- 添加彩色图例说明

### Q5: GPU信息显示"未检测到"？

**A:** 可能原因：
- 使用集成显卡（正常现象）
- 缺少驱动或系统工具
  - Windows：需要WMIC
  - Linux：需要lspci
    ```bash
    sudo apt-get install pciutils
    ```

### Q6: 网卡信息不完整？

**A:** 某些虚拟网卡或禁用的网卡可能显示不完整，这是正常现象。程序会跳过无效的网络接口。

### Q7: 硬盘使用率不准确？

**A:** 
- Windows：某些系统分区可能无法访问
- Linux：需要挂载的分区才会显示
- macOS：系统保护的分区可能无法读取

### Q8: 如何只查看某一项硬件？

**A:** 
1. 点击"取消"按钮取消全选
2. 勾选需要的硬件类型
3. 点击"一键查看"

### Q9: 可以定时自动扫描吗？

**A:** 当前版本不支持自动扫描，需要手动点击按钮。如有需求可以自行修改代码添加定时器功能。

### Q10: 支持命令行模式吗？

**A:** 当前版本只有GUI界面。如需命令行版本，可以基于代码进行二次开发。

---

## 📊 性能指标

| 指标 | 数值 |
|-----|------|
| 启动时间 | < 2秒 |
| 扫描时间（全部） | 1-3秒 |
| 内存占用 | 30-50MB |
| CPU占用（扫描时） | < 5% |
| PDF生成时间 | 2-5秒 |
| PDF文件大小 | 100-500KB |

---

## 🔄 更新日志

### v1.2.0 (2025-10-01)
- ✨ 新增PDF导出功能
- 📊 添加可视化图表（饼图、条形图）
- 🎨 优化PDF报告样式和排版
- 🐛 修复图表中文乱码问题
- 🌍 完善中文字体支持

### v1.1.0 (2025-09-25)
- ✨ 新增选择性查看功能
- 🎨 优化界面布局（左右分栏）
- 📌 添加状态栏显示
- 🔧 改进错误处理机制

### v1.0.0 (2025-09-20)
- 🎉 首次发布
- 💻 支持CPU、内存、硬盘、网卡信息查看
- 🖥️ 基础GUI界面
- 🌐 跨平台支持

---

## 🛠️ 技术栈

- **GUI框架**: Tkinter
- **系统信息**: psutil
- **PDF生成**: ReportLab
- **图像处理**: Pillow
- **编程语言**: Python 3.7+

---

## 📝 开发说明

### 项目结构

```
hardware-info-viewer/
├── hardware_info_viewer.py    # 主程序
├── requirements.txt           # 依赖列表
├── README.md                  # 说明文档
└── LICENSE                    # 许可证文件
```

### 代码架构

```python
HardwareInfoViewer (主类)
│
├── __init__()           # 初始化界面
├── start_scan()         # 开始扫描
├── scan_hardware()      # 扫描线程
│
├── get_cpu_info()       # 获取CPU信息
├── get_memory_info()    # 获取内存信息
├── get_disk_info()      # 获取硬盘信息
├── get_network_info()   # 获取网卡信息
├── get_gpu_info()       # 获取GPU信息
├── get_motherboard_info() # 获取主板信息
├── get_system_info()    # 获取系统信息
│
├── export_pdf()         # 导出PDF
└── generate_pdf()       # 生成PDF报告
```

### 二次开发

欢迎贡献代码！可以添加的功能：
- [ ] 定时自动扫描
- [ ] 历史记录对比
- [ ] 导出Excel格式
- [ ] 多语言支持
- [ ] 性能监控曲线
- [ ] 系统健康评分

---

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

1. Fork 本仓库
2. 创建新分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启Pull Request

---

## 📧 联系方式

- 作者：vestjin
- 邮箱：17633088571@163.com
- 项目主页：https://github.com/vestjin/python_demo

---

## 📜 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

```
MIT License

Copyright (c) 2025 Your Name

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## ⭐ Star History

如果这个项目对你有帮助，请给我们一个 Star ⭐！

---

## 🙏 致谢

感谢以下开源项目：
- [psutil](https://github.com/giampaolo/psutil) - 跨平台系统和进程工具库
- [ReportLab](https://www.reportlab.com/) - 强大的PDF生成库
- [Pillow](https://python-pillow.org/) - 图像处理库

---

<div align="center">

**Made with ❤️ by Python**

[⬆ 回到顶部](#-硬件信息查看工具-pro)

</div>