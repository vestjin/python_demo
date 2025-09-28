# 📁 批量文件重命名工具

一个功能强大、易于使用的 Python GUI 批量文件重命名工具，支持多种重命名模式、实时预览、冲突检测和拖拽操作。

| [![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://python.org) | [![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)](https://example.com) | [![License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT) |
|:---:|:---:|:---:|


## ✨ 主要特性

### 🎯 多种重命名模式
- **查找替换**：在文件名中查找并替换指定文本
- **添加前缀**：在文件名前添加指定文本
- **添加后缀**：在文件名后（扩展名前）添加指定文本
- **序号重命名**：使用"基础名+序号"格式批量重命名

### 🔍 智能筛选系统
- **扩展名筛选**：只处理特定类型的文件（如 .txt, .jpg, .pdf 等）
- **文件类型筛选**：区分处理文件或文件夹
- **一键重置**：快速清除所有筛选条件

### 👀 实时预览功能
- **即时预览**：实时显示重命名前后的文件名对比
- **智能颜色标识**：
  - 🟢 **绿色**：可以安全重命名
  - 🔴 **红色**：名称冲突或文件已存在
  - 🟠 **橙色**：包含非法字符或名称为空
  - ⚪ **灰色**：名称未更改

### 🛡️ 安全保护机制
- **冲突检测**：自动检测重复文件名
- **合法性验证**：检查文件名是否包含非法字符
- **执行确认**：重命名前的二次确认对话框
- **详细报告**：显示执行结果和错误信息

### 🎨 用户友好界面
- **拖拽支持**：直接拖拽文件/文件夹到窗口
- **响应式布局**：支持窗口大小调整
- **内置帮助**：点击按钮查看详细使用说明
- **直观操作**：清晰的界面布局和操作流程

## 📋 系统要求

- **Python 版本**：3.7 或更高版本
- **操作系统**：Windows / macOS / Linux
- **依赖库**：仅使用 Python 标准库，无需额外安装

### 标准库依赖
```python
tkinter      # GUI 界面框架
pathlib      # 现代路径处理
os           # 系统操作接口  
re           # 正则表达式支持
collections  # 高级数据结构
string       # 字符串操作工具
sys          # 系统相关功能
```

## 🚀 安装与运行

### 方法一：直接运行源码
```bash
# 1. 下载源码
git clone https://github.com/vestjin/python_demo.git
cd batch-rename-tool

# 2. 运行程序
python batch_rename_tool.py
```

### 方法二：打包为独立执行文件(已打包)

#### 使用 PyInstaller（推荐）
```bash
# 安装 PyInstaller
pip install pyinstaller

# 打包为单文件 EXE（Windows）
pyinstaller --onefile --windowed --name="批量重命名工具" batch_rename_tool.py

# 如果有图标文件
pyinstaller --onefile --windowed --icon=icon.ico --name="批量重命名工具" batch_rename_tool.py
```

#### 使用 Auto-py-to-exe（图形化界面）
```bash
# 安装工具
pip install auto-py-to-exe

# 启动图形化打包界面
auto-py-to-exe
```

打包完成后，在 `dist` 文件夹中可以找到独立的可执行文件。

## 📖 使用指南

### 基本操作流程

1. **📂 添加文件**
   - 点击"选择文件"选择多个文件
   - 点击"选择文件夹"选择整个文件夹
   - 直接拖拽文件/文件夹到程序窗口

2. **🔍 设置筛选（可选）**
   - 选择特定扩展名（如只处理 .jpg 文件）
   - 选择文件类型（只处理文件或文件夹）

3. **✏️ 配置重命名规则**
   - 选择重命名模式
   - 填写相应的参数

4. **👁️ 预览更改**
   - 点击"🔄 预览更改"查看重命名效果
   - 检查颜色状态，确保无冲突

5. **✅ 执行重命名**
   - 确认无误后点击"✅ 执行重命名"
   - 在确认对话框中选择"是"

### 详细功能说明

#### 🔄 查找替换模式
```
原文件名：photo_2024_01.jpg
查找：2024
替换：2025
新文件名：photo_2025_01.jpg
```

#### ➕ 添加前缀模式
```
原文件名：document.pdf
前缀：重要_
新文件名：重要_document.pdf
```

#### ➕ 添加后缀模式
```
原文件名：report.docx
后缀：_final
新文件名：report_final.docx
```

#### 🔢 序号重命名模式
```
基础名：照片
起始序号：1
位数：3

原文件名：IMG001.jpg, IMG002.jpg, IMG003.jpg
新文件名：照片001.jpg, 照片002.jpg, 照片003.jpg
```

## ⚠️ 注意事项

### 文件名限制
- Windows 系统不支持的字符：`< > : " / \ | ? *`
- 文件名不能为空或只包含空格
- 文件名长度建议不超过 255 个字符

### 安全提醒
- ⚠️ **重命名操作不可撤销**，建议操作前备份重要文件
- 🔒 确保对目标文件夹有足够的读写权限
- 📋 建议先在测试文件夹中试用，熟悉后再处理重要文件
- 🎯 使用预览功能仔细检查重命名结果

### 性能说明
- ✅ 支持同时处理数千个文件
- ⚡ 使用高效的路径处理算法
- 💾 占用内存较少，适合大批量操作

## 🐛 故障排除

### 常见问题

**Q: 程序无法启动，提示缺少模块**
```
A: 确保使用 Python 3.7+ 版本，所有依赖都是标准库，无需额外安装
```

**Q: 拖拽功能不工作**
```
A: 某些 Linux 发行版可能需要安装额外的 tkinter 支持包：
   sudo apt-get install python3-tk
```

**Q: 重命名失败，提示权限错误**
```
A: 检查以下几点：
   - 确保对文件夹有写权限
   - 文件没有被其他程序占用
   - 以管理员身份运行程序（如果需要）
```

**Q: 中文文件名显示异常**
```
A: 确保系统支持 UTF-8 编码，Windows 用户可以在区域设置中启用 UTF-8 支持
```

### 错误代码对照

| 错误类型 | 解决方案 |
|---------|---------|
| 名称冲突 | 修改重命名规则，确保生成的文件名唯一 |
| 非法字符 | 移除文件名中的非法字符 `< > : " / \ | ? *` |
| 文件已存在 | 检查目标文件夹，删除或重命名冲突文件 |
| 权限不足 | 以管理员身份运行，或更改文件夹权限 |

## 📝 更新日志

### v1.0.0 (2025-9-28)
- ✨ 初始版本发布
- 🎯 支持四种重命名模式
- 🔍 实现筛选功能
- 👀 添加实时预览
- 🛡️ 完整的冲突检测
- 🎨 用户友好的 GUI 界面
- 📖 内置使用说明

## 🤝 贡献指南

欢迎贡献代码和提出建议！

1. **Fork** 本仓库
2. **创建**特性分支 (`git checkout -b feature/AmazingFeature`)
3. **提交**更改 (`git commit -m 'Add some AmazingFeature'`)
4. **推送**到分支 (`git push origin feature/AmazingFeature`)
5. **打开** Pull Request

### 开发环境设置
```bash
# 克隆仓库
git clone https://github.com/vestjin/python_demo.git

# 进入目录
cd batch-rename-tool

# 运行程序
python batch_rename_tool.py
```

## 📄 许可证

本项目采用 MIT 许可证 - 详细信息请查看 [LICENSE](LICENSE) 文件。

## 👨‍💻 作者

- **Jin** - *初始工作* - [GitHub](https://github.com/vestjin)

## 🙏 致谢

- 感谢 Python 社区提供的优秀标准库
- 感谢所有测试用户的反馈和建议
- 特别感谢 tkinter 框架的开发者们

## 📞 支持与联系

- 🐛 **问题报告**：[GitHub Issues]([Issues · vestjin/python_demo](https://github.com/vestjin/python_demo/issues))
- 💡 **功能建议**：[GitHub Discussions](https://github.com/vestjin/python_demo/discussions)
- 📧 **邮件联系**：17633088571@163.com

---

⭐ 如果这个工具对你有帮助，请给个 Star 支持一下！

📢 欢迎分享给其他需要批量重命名文件的朋友！