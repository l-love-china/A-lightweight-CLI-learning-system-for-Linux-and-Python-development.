
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python 类操作系统 - 命令行工具
一个简单的命令行工具，用于学习Python命令行工具的编写
"""

import os
from pathlib import Path
import shutil
import sys
import subprocess
import time
from datetime import datetime

class PyOS:
    """Python 类操作系统命令行工具"""
    
    def __init__(self):
        self.current_dir = os.getcwd()
        self.running = True
        self.history = []
        self.max_history = 100
        self.start_time = time.time()
        self.command_count = 0
        
        # 颜色代码 - 更丰富的颜色方案
        self.COLORS = {
            'RESET': '\033[0m',
            'RED': '\033[91m',
            'GREEN': '\033[92m',
            'YELLOW': '\033[93m',
            'BLUE': '\033[94m',
            'PURPLE': '\033[95m',
            'CYAN': '\033[96m',
            'WHITE': '\033[97m',
            'BOLD': '\033[1m',
            'UNDERLINE': '\033[4m',
            'GRAY': '\033[90m',
            'ORANGE': '\033[38;5;214m',
            'PINK': '\033[38;5;205m',
            'TEAL': '\033[38;5;51m'
        }
        
        # UI配置
        self.ui_config = {
            'show_time': True,
            'show_path': True,
            'show_command_count': True,
            'color_scheme': 'modern',
            'prompt_style': 'detailed'
        }
        
    def display_prompt(self):
        """显示美观的命令提示符"""
        c = self.COLORS
        
        # 构建提示符组件
        components = []
        
        if self.ui_config['show_time']:
            current_time = datetime.now().strftime("%H:%M:%S")
            components.append(f"{c['GRAY']}[{current_time}]{c['RESET']}")
        
        if self.ui_config['show_command_count']:
            components.append(f"{c['PURPLE']}[cmd:{self.command_count}]{c['RESET']}")
        
        # 显示当前目录（简化路径）
        if self.ui_config['show_path']:
            # 简化路径显示
            home_dir = os.path.expanduser("~")
            if self.current_dir.startswith(home_dir):
                display_path = "~" + self.current_dir[len(home_dir):]
            else:
                display_path = self.current_dir
            
            # 如果路径太长，截断显示
            if len(display_path) > 40:
                display_path = "..." + display_path[-37:]
            
            components.append(f"{c['CYAN']}{display_path}{c['RESET']}")
        
        # 根据配置选择提示符样式
        if self.ui_config['prompt_style'] == 'simple':
            prompt = f"{c['GREEN']}PyOS>{c['RESET']} "
        elif self.ui_config['prompt_style'] == 'detailed':
            if components:
                prompt = f"{' '.join(components)} {c['GREEN']}➜{c['RESET']} "
            else:
                prompt = f"{c['GREEN']}PyOS ➜{c['RESET']} "
        else:  # modern
            prompt = f"{c['BLUE']}┌─[{c['YELLOW']}PyOS{c['BLUE']}]{c['RESET']}\n"
            if components:
                prompt += f"{c['BLUE']}└─{c['GREEN']}➜{c['RESET']} {' '.join(components)} "
            else:
                prompt += f"{c['BLUE']}└─{c['GREEN']}➜{c['RESET']} "
        
        print(prompt, end="")
    
    def dir_command(self, args=None):
        """显示当前目录内容"""
        try:
            items = os.listdir(self.current_dir)
            print(f"目录: {self.current_dir}")
            print("-" * 50)
            
            # 显示目录
            dirs = [item for item in items if os.path.isdir(os.path.join(self.current_dir, item))]
            if dirs:
                print("目录:")
                for d in sorted(dirs):
                    print(f"  [DIR]  {d}")
            
            # 显示文件
            files = [item for item in items if os.path.isfile(os.path.join(self.current_dir, item))]
            if files:
                print("文件:")
                for f in sorted(files):
                    size = os.path.getsize(os.path.join(self.current_dir, f))
                    print(f"  [FILE] {f} ({size} bytes)")
                    
            print(f"\n总计: {len(dirs)} 个目录, {len(files)} 个文件")
            
        except PermissionError:
            print("错误: 没有权限访问此目录")
        except Exception as e:
            print(f"错误: {e}")
    
    def cd_command(self, args):
        """切换目录"""
        if not args:
            print("用法: cd <目录路径>")
            return
            
        target_path = args[0]
        
        # 处理 cd ..
        if target_path == "..":
            parent_dir = os.path.dirname(self.current_dir)
            if parent_dir:
                self.current_dir = parent_dir
                print(f"切换到: {self.current_dir}")
            return
        
        # 处理相对路径和绝对路径
        if os.path.isabs(target_path):
            new_path = target_path
        else:
            new_path = os.path.join(self.current_dir, target_path)
        
        # 检查路径是否存在且是目录
        if os.path.exists(new_path) and os.path.isdir(new_path):
            self.current_dir = os.path.abspath(new_path)
            print(f"切换到: {self.current_dir}")
        else:
            print(f"错误: 目录不存在 - {target_path}")
    
    def new_command(self, args):
        """新建文件或文件夹"""
        if not args:
            print("用法: new <文件名> 或 new /j <文件夹名>")
            return
            
        if args[0] == "/j":
            # 新建文件夹
            if len(args) < 2:
                print("用法: new /j <文件夹名>")
                return
                
            folder_name = args[1]
            folder_path = os.path.join(self.current_dir, folder_name)
            
            try:
                os.makedirs(folder_path, exist_ok=True)
                print(f"文件夹已创建: {folder_name}")
            except Exception as e:
                print(f"错误: 无法创建文件夹 - {e}")
        else:
            # 新建文件
            file_name = args[0]
            file_path = os.path.join(self.current_dir, file_name)
            
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write("")
                print(f"文件已创建: {file_name}")
            except Exception as e:
                print(f"错误: 无法创建文件 - {e}")
    
    def pwd_command(self, args=None):
        """显示当前工作目录"""
        print(self.current_dir)
    
    def exit_command(self, args=None):
        """退出程序"""
        print("感谢使用 PyOS，再见！")
        self.running = False
    
    def pyb_command(self, args):
        """Python代码编辑器（带语法高亮）"""
        if not args:
            print("用法: pyb <python文件名>")
            return
            
        file_name = args[0]
        file_path = os.path.join(self.current_dir, file_name)
        
        # 检查文件扩展名
        if not file_name.endswith('.py'):
            print("提示: 建议使用.py扩展名")
        
        print(f"正在打开Python编辑器: {file_name}")
        print("功能: 语法高亮 | 基本关键字帮助 | 自动缩进")
        print("输入 'save' 保存并退出，输入 'quit' 放弃修改")
        print("-" * 50)
        
        # 读取现有文件内容
        content = ""
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                print("已加载现有文件内容")
            except Exception as e:
                print(f"读取文件错误: {e}")
        else:
            # 新建文件时添加基本模板
            content = "#!/usr/bin/env python3\n# -*- coding: utf-8 -*-\n\n"
            print("新建Python文件，已添加基本模板")
        
        # 显示Python关键字帮助
        python_keywords = ['def', 'class', 'if', 'else', 'elif', 'for', 'while', 'import', 'from', 'return', 'try', 'except', 'finally']
        print(f"Python关键字提示: {', '.join(python_keywords)}")
        
        # 编辑器循环
        editing = True
        lines = content.split('\n') if content else []
        
        while editing:
            try:
                # 显示当前内容（带行号）
                print("\n当前内容:")
                for i, line in enumerate(lines, 1):
                    # 简单的语法高亮
                    if any(keyword in line for keyword in ['def ', 'class ', 'import ', 'from ']):
                        print(f"{i:3d} | [32m{line}[0m")  # 绿色
                    elif any(keyword in line for keyword in ['if ', 'else:', 'elif ', 'for ', 'while ']):
                        print(f"{i:3d} | [33m{line}[0m")  # 黄色
                    elif '#' in line:
                        commented = line.split('#')
                        print(f"{i:3d} | {commented[0]}[90m#{commented[1]}[0m")  # 灰色注释
                    else:
                        print(f"{i:3d} | {line}")
                
                print("\n输入行号编辑该行，或输入命令:")
                print("  add <内容> - 添加新行")
                print("  del <行号> - 删除行")
                print("  :w - 保存文件")
                print("  :q - 退出编辑器")
                print("  :wq - 保存并退出")
                print("  :wq /c <文件名> - 另存为并退出")
                print("  quit - 放弃修改")
                
                user_input = input("pyb> ").strip()
                
                if user_input == ':w':
                    # 保存文件
                    try:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write('\n'.join(lines))
                        print(f"文件已保存: {file_name}")
                    except Exception as e:
                        print(f"保存错误: {e}")
                elif user_input == ':q':
                    print("退出编辑器")
                    editing = False
                elif user_input == ':wq':
                    # 保存并退出
                    try:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write('\n'.join(lines))
                        print(f"文件已保存并退出: {file_name}")
                        editing = False
                    except Exception as e:
                        print(f"保存错误: {e}")
                elif user_input.startswith(':wq /c '):
                    # 另存为并退出
                    new_filename = user_input[7:].strip()
                    if not new_filename:
                        print("错误: 请指定新文件名")
                        continue
                    
                    new_file_path = os.path.join(self.current_dir, new_filename)
                    
                    try:
                        with open(new_file_path, 'w', encoding='utf-8') as f:
                            f.write('\n'.join(lines))
                        print(f"文件已另存为: {new_filename}")
                        editing = False
                    except Exception as e:
                        print(f"另存为错误: {e}")
                elif user_input.lower() == 'save':
                    # 兼容旧版save命令
                    try:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write('\n'.join(lines))
                        print(f"文件已保存: {file_name}")
                        editing = False
                    except Exception as e:
                        print(f"保存错误: {e}")
                elif user_input.lower() == 'quit':
                    print("放弃修改，退出编辑器")
                    editing = False
                elif user_input.startswith('add '):
                    # 添加新行
                    new_line = user_input[4:]
                    lines.append(new_line)
                    print("已添加新行")
                elif user_input.startswith('del '):
                    # 删除行
                    try:
                        line_num = int(user_input[4:])
                        if 1 <= line_num <= len(lines):
                            removed = lines.pop(line_num - 1)
                            print(f"已删除第{line_num}行: {removed}")
                        else:
                            print("无效的行号")
                    except ValueError:
                        print("无效的行号格式")
                elif user_input.isdigit():
                    # 编辑指定行
                    line_num = int(user_input)
                    if 1 <= line_num <= len(lines):
                        print(f"编辑第{line_num}行: {lines[line_num-1]}")
                        new_content = input("新内容: ").strip()
                        lines[line_num-1] = new_content
                        print("行内容已更新")
                    else:
                        print("无效的行号")
                else:
                    print("未知命令，输入 'help' 查看帮助")
                    
            except KeyboardInterrupt:
                print("\n使用 Ctrl+C 退出编辑器")
                break
            except Exception as e:
                print(f"编辑器错误: {e}")
    
    def txtb_command(self, args):
        """文本编辑器（适用于pyb但没有高亮）"""
        if not args:
            print("用法: txtb <文件名>")
            return
            
        file_name = args[0]
        file_path = os.path.join(self.current_dir, file_name)
        
        print(f"正在打开文本编辑器: {file_name}")
        print("功能: 简单文本编辑 | 无语法高亮")
        print("输入 'save' 保存并退出，输入 'quit' 放弃修改")
        print("-" * 50)
        
        # 读取现有文件内容
        content = ""
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                print("已加载现有文件内容")
            except Exception as e:
                print(f"读取文件错误: {e}")
        
        # 编辑器循环
        editing = True
        lines = content.split('\n') if content else []
        
        while editing:
            try:
                # 显示当前内容（带行号）
                print("\n当前内容:")
                for i, line in enumerate(lines, 1):
                    print(f"{i:3d} | {line}")
                
                print("\n输入行号编辑该行，或输入命令:")
                print("  add <内容> - 添加新行")
                print("  del <行号> - 删除行")
                print("  :w - 保存文件")
                print("  :q - 退出编辑器")
                print("  :wq - 保存并退出")
                print("  :wq /c <文件名> - 另存为并退出")
                print("  quit - 放弃修改")
                
                user_input = input("txtb> ").strip()
                
                if user_input == ':w':
                    # 保存文件
                    try:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write('\n'.join(lines))
                        print(f"文件已保存: {file_name}")
                    except Exception as e:
                        print(f"保存错误: {e}")
                elif user_input == ':q':
                    print("退出编辑器")
                    editing = False
                elif user_input == ':wq':
                    # 保存并退出
                    try:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write('\n'.join(lines))
                        print(f"文件已保存并退出: {file_name}")
                        editing = False
                    except Exception as e:
                        print(f"保存错误: {e}")
                elif user_input.startswith(':wq /c '):
                    # 另存为并退出
                    new_filename = user_input[7:].strip()
                    if not new_filename:
                        print("错误: 请指定新文件名")
                        continue
                    
                    new_file_path = os.path.join(self.current_dir, new_filename)
                    
                    try:
                        with open(new_file_path, 'w', encoding='utf-8') as f:
                            f.write('\n'.join(lines))
                        print(f"文件已另存为: {new_filename}")
                        editing = False
                    except Exception as e:
                        print(f"另存为错误: {e}")
                elif user_input.lower() == 'save':
                    # 兼容旧版save命令
                    try:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write('\n'.join(lines))
                        print(f"文件已保存: {file_name}")
                        editing = False
                    except Exception as e:
                        print(f"保存错误: {e}")
                elif user_input.lower() == 'quit':
                    print("放弃修改，退出编辑器")
                    editing = False
                elif user_input.startswith('add '):
                    # 添加新行
                    new_line = user_input[4:]
                    lines.append(new_line)
                    print("已添加新行")
                elif user_input.startswith('del '):
                    # 删除行
                    try:
                        line_num = int(user_input[4:])
                        if 1 <= line_num <= len(lines):
                            removed = lines.pop(line_num - 1)
                            print(f"已删除第{line_num}行: {removed}")
                        else:
                            print("无效的行号")
                    except ValueError:
                        print("无效的行号格式")
                elif user_input.isdigit():
                    # 编辑指定行
                    line_num = int(user_input)
                    if 1 <= line_num <= len(lines):
                        print(f"编辑第{line_num}行: {lines[line_num-1]}")
                        new_content = input("新内容: ").strip()
                        lines[line_num-1] = new_content
                        print("行内容已更新")
                    else:
                        print("无效的行号")
                else:
                    print("未知命令")
                    
            except KeyboardInterrupt:
                print("\n使用 Ctrl+C 退出编辑器")
                break
            except Exception as e:
                print(f"编辑器错误: {e}")
    
    def del_command(self, args):
        """删除文件或文件夹"""
        if not args:
            print("用法: del <文件名或文件夹名>")
            return
            
        target_name = args[0]
        target_path = os.path.join(self.current_dir, target_name)
        
        if not os.path.exists(target_path):
            print(f"错误: 文件或文件夹不存在 - {target_name}")
            return
        
        try:
            if os.path.isfile(target_path):
                # 删除文件
                os.remove(target_path)
                print(f"文件已删除: {target_name}")
            elif os.path.isdir(target_path):
                # 删除文件夹
                shutil.rmtree(target_path)
                print(f"文件夹已删除: {target_name}")
        except PermissionError:
            print(f"错误: 没有权限删除 - {target_name}")
        except Exception as e:
            print(f"删除错误: {e}")
    
    def config_command(self, args):
        """配置界面设置"""
        c = self.COLORS
        
        if not args:
            # 显示当前配置
            print(f"{c['BLUE']}{'='*60}{c['RESET']}")
            print(f"{c['YELLOW']}{c['BOLD']}⚙️ PyOS 配置设置{c['RESET']}")
            print(f"{c['BLUE']}{'='*60}{c['RESET']}")
            
            print(f"{c['GREEN']}当前配置:{c['RESET']}")
            for key, value in self.ui_config.items():
                status = f"{c['GREEN']}启用{c['RESET']}" if value else f"{c['RED']}禁用{c['RESET']}"
                if isinstance(value, bool):
                    print(f"  {c['CYAN']}{key:<20}{c['RESET']}: {status}")
                else:
                    print(f"  {c['CYAN']}{key:<20}{c['RESET']}: {c['YELLOW']}{value}{c['RESET']}")
            
            print(f"\n{c['GREEN']}配置命令示例:{c['RESET']}")
            print(f"  {c['CYAN']}config show_time on{c['RESET']}    - 启用时间显示")
            print(f"  {c['CYAN']}config show_time off{c['RESET']}   - 禁用时间显示")
            print(f"  {c['CYAN']}config prompt_style simple{c['RESET']} - 设置提示符样式")
            print(f"  {c['CYAN']}config prompt_style detailed{c['RESET']}")
            print(f"  {c['CYAN']}config prompt_style modern{c['RESET']}")
            
            print(f"{c['BLUE']}{'='*60}{c['RESET']}")
            return
        
        if len(args) >= 2:
            setting = args[0]
            value = args[1].lower()
            
            if setting in self.ui_config:
                if isinstance(self.ui_config[setting], bool):
                    if value in ['on', 'true', '1', 'yes']:
                        self.ui_config[setting] = True
                        print(f"{c['GREEN']}✅ 已启用 {setting}{c['RESET']}")
                    elif value in ['off', 'false', '0', 'no']:
                        self.ui_config[setting] = False
                        print(f"{c['YELLOW']}⚠️ 已禁用 {setting}{c['RESET']}")
                    else:
                        print(f"{c['RED']}❌ 无效的值: {value} (请使用 on/off){c['RESET']}")
                else:
                    # 字符串类型的配置
                    if setting == 'prompt_style' and value in ['simple', 'detailed', 'modern']:
                        self.ui_config[setting] = value
                        print(f"{c['GREEN']}✅ 已设置 {setting} = {value}{c['RESET']}")
                    else:
                        print(f"{c['RED']}❌ 无效的值或配置项: {setting}{c['RESET']}")
            else:
                print(f"{c['RED']}❌ 未知的配置项: {setting}{c['RESET']}")
        else:
            print(f"{c['RED']}❌ 用法: config <设置项> <值>{c['RESET']}")
    
    def help_command(self, args=None):
        """显示美观的帮助信息"""
        c = self.COLORS
        
        print(f"{c['BLUE']}{'='*60}{c['RESET']}")
        print(f"{c['YELLOW']}{c['BOLD']}📚 PyOS 帮助手册{c['RESET']}")
        print(f"{c['BLUE']}{'='*60}{c['RESET']}")
        
        # 文件系统命令
        print(f"{c['GREEN']}{c['BOLD']}📁 文件系统命令:{c['RESET']}")
        print(f"  {c['CYAN']}dir{c['RESET']}              - 显示当前目录内容")
        print(f"  {c['CYAN']}cd{c['RESET']} <目录路径>    - 切换目录 (cd .. 返回上级目录)")
        print(f"  {c['CYAN']}new{c['RESET']} <文件名>     - 新建文件")
        print(f"  {c['CYAN']}new /j{c['RESET']} <文件夹名> - 新建文件夹")
        print(f"  {c['CYAN']}pwd{c['RESET']}              - 显示当前工作目录")
        print(f"  {c['CYAN']}del{c['RESET']} <名称>       - 删除文件或文件夹")
        print(f"  {c['CYAN']}cp{c['RESET']} <源> <目标> [-r] - 复制文件/目录")
        print(f"  {c['CYAN']}mv{c['RESET']} <源> <目标>    - 移动文件/目录")
        print(f"  {c['CYAN']}find{c['RESET']} <模式> [路径] - 搜索文件")
        print(f"  {c['CYAN']}cat{c['RESET']} <文件名> [行数] - 查看文件内容")
        print(f"  {c['CYAN']}type{c['RESET']} <文件名> [行数] - 查看文件内容(同cat)")
        print()
        
        # Python执行命令
        print(f"{c['TEAL']}{c['BOLD']}🐍 Python执行命令:{c['RESET']}")
        print(f"  {c['CYAN']}python{c['RESET']} <文件名>  - 运行Python文件")
        print(f"  {c['CYAN']}py{c['RESET']} <文件名>      - 运行Python文件（简写）")
        print()
        
        # 编辑器命令
        print(f"{c['PURPLE']}{c['BOLD']}✏️ 编辑器命令:{c['RESET']}")
        print(f"  {c['CYAN']}pyb{c['RESET']} <文件名>     - Python代码编辑器（语法高亮）")
        print(f"  {c['CYAN']}txtb{c['RESET']} <文件名>    - 文本编辑器（无高亮）")
        print()
        
        # cmd命令执行
        print(f"{c['ORANGE']}{c['BOLD']}💻 cmd命令执行:{c['RESET']}")
        print(f"  任何未知命令将自动在系统cmd中运行")
        print(f"  例如: {c['GRAY']}ipconfig, ping, echo, 等系统命令{c['RESET']}")
        print()
        
        # 编辑器内部命令
        print(f"{c['PINK']}{c['BOLD']}🔧 编辑器内部命令:{c['RESET']}")
        print(f"  {c['GRAY']}:w{c['RESET']}               - 保存文件")
        print(f"  {c['GRAY']}:q{c['RESET']}               - 退出编辑器")
        print(f"  {c['GRAY']}:wq{c['RESET']}              - 保存并退出")
        print(f"  {c['GRAY']}:wq /c{c['RESET']} <文件名>  - 另存为并退出")
        print(f"  {c['GRAY']}add{c['RESET']} <内容>       - 添加新行")
        print(f"  {c['GRAY']}del{c['RESET']} <行号>       - 删除指定行")
        print()
        
        # 系统命令
        print(f"{c['ORANGE']}{c['BOLD']}⚙️ 系统命令:{c['RESET']}")
        print(f"  {c['CYAN']}help{c['RESET']}             - 显示此帮助信息")
        print(f"  {c['CYAN']}config{c['RESET']}         - 自定义界面设置")
        print(f"  {c['CYAN']}sysinfo{c['RESET']}         - 显示系统信息")
        print(f"  {c['CYAN']}history{c['RESET']}         - 显示命令历史")
        print(f"  {c['CYAN']}exit{c['RESET']}             - 退出程序")
        print()
        
        # 使用示例
        print(f"{c['YELLOW']}{c['BOLD']}💡 使用示例:{c['RESET']}")
        print(f"  {c['GRAY']}dir{c['RESET']}              # 显示当前目录")
        print(f"  {c['GRAY']}cd Documents{c['RESET']}     # 切换到Documents目录")
        print(f"  {c['GRAY']}cd ..{c['RESET']}            # 返回上级目录")
        print(f"  {c['GRAY']}new test.txt{c['RESET']}     # 新建文件test.txt")
        print(f"  {c['GRAY']}new /j myfolder{c['RESET']}  # 新建文件夹myfolder")
        print(f"  {c['GRAY']}pyb hello.py{c['RESET']}     # 编辑Python文件")
        print(f"  {c['GRAY']}txtb readme.txt{c['RESET']}  # 编辑文本文件")
        print(f"  {c['GRAY']}del oldfile.txt{c['RESET']}  # 删除文件")
        print()
        
        # 编辑器使用示例
        print(f"{c['YELLOW']}{c['BOLD']}💡 编辑器使用示例:{c['RESET']}")
        print(f"  {c['GRAY']}pyb test.py{c['RESET']}      # 编辑Python文件")
        print(f"  {c['GRAY']}:w{c['RESET']}               # 保存文件")
        print(f"  {c['GRAY']}:wq{c['RESET']}              # 保存并退出")
        print(f"  {c['GRAY']}:wq /c new.py{c['RESET']}    # 另存为new.py并退出")
        
        print(f"{c['BLUE']}{'='*60}{c['RESET']}")
    
    def parse_command(self, command_line):
        """解析命令行输入"""
        parts = command_line.strip().split()
        if not parts:
            return None, None
            
        command = parts[0].lower()
        args = parts[1:] if len(parts) > 1 else []
        
        return command, args
    
    def execute_command(self, command, args):
        """执行命令"""
        command_map = {
            'dir': self.dir_command,
            'cd': self.cd_command,
            'new': self.new_command,
            'pwd': self.pwd_command,
            'del': self.del_command,
            'find': self.find_command,
            'cat': self.cat_command,
            'type': self.cat_command,
            'pyb': self.pyb_command,
            'txtb': self.txtb_command,
            'python': self.run_python_file,
            'py': self.run_python_file,
            'help': self.help_command,
            'config': self.config_command,
            'sysinfo': self.sysinfo_command,
            'history': self.history_command,
            'exit': self.exit_command,
            'quit': self.exit_command,
            'cp': self.cp_command,
            'mv': self.mv_command
        }
        
        if command in command_map:
            command_map[command](args)
        else:
            # 无法解析的命令，尝试在cmd中运行
            print(f"未知命令: {command}，尝试在cmd中运行...")
            self.run_in_cmd(command, args)
    
    def cp_command(self, args):
        """复制文件或目录"""
        c = self.COLORS
        
        if len(args) < 2:
            print(f"{c['RED']}❌ 用法: cp <源文件> <目标文件> [选项]{c['RESET']}")
            print(f"{c['GRAY']}示例: cp file1.txt file2.txt{c['RESET']}")
            print(f"{c['GRAY']}示例: cp -r folder1 folder2{c['RESET']}")
            return
        
        source = args[0]
        target = args[1]
        recursive = '-r' in args or '-R' in args
        
        source_path = os.path.join(self.current_dir, source)
        target_path = os.path.join(self.current_dir, target)
        
        if not os.path.exists(source_path):
            print(f"{c['RED']}❌ 源文件不存在: {source}{c['RESET']}")
            return
        
        try:
            if os.path.isfile(source_path):
                # 复制文件
                shutil.copy2(source_path, target_path)
                print(f"{c['GREEN']}✅ 文件复制成功: {source} -> {target}{c['RESET']}")
            elif os.path.isdir(source_path):
                if recursive:
                    # 递归复制目录
                    shutil.copytree(source_path, target_path)
                    print(f"{c['GREEN']}✅ 目录复制成功: {source} -> {target}{c['RESET']}")
                else:
                    print(f"{c['RED']}❌ 目录复制需要使用 -r 选项{c['RESET']}")
            
        except Exception as e:
            print(f"{c['RED']}❌ 复制失败: {e}{c['RESET']}")
    
    def mv_command(self, args):
        """移动文件或目录"""
        c = self.COLORS
        
        if len(args) < 2:
            print(f"{c['RED']}❌ 用法: mv <源文件> <目标文件>{c['RESET']}")
            print(f"{c['GRAY']}示例: mv old.txt new.txt{c['RESET']}")
            print(f"{c['GRAY']}示例: mv folder1 folder2{c['RESET']}")
            return
        
        source = args[0]
        target = args[1]
        
        source_path = os.path.join(self.current_dir, source)
        target_path = os.path.join(self.current_dir, target)
        
        if not os.path.exists(source_path):
            print(f"{c['RED']}❌ 源文件不存在: {source}{c['RESET']}")
            return
        
        try:
            shutil.move(source_path, target_path)
            print(f"{c['GREEN']}✅ 移动成功: {source} -> {target}{c['RESET']}")
        except Exception as e:
            print(f"{c['RED']}❌ 移动失败: {e}{c['RESET']}")
    
    def sysinfo_command(self, args=None):
        """显示系统信息"""
        c = self.COLORS
        
        print(f"{c['BLUE']}{'='*60}{c['RESET']}")
        print(f"{c['YELLOW']}{c['BOLD']}💻 PyOS 系统信息{c['RESET']}")
        print(f"{c['BLUE']}{'='*60}{c['RESET']}")
        
        # 操作系统信息
        print(f"{c['GREEN']}📊 操作系统信息:{c['RESET']}")
        print(f"  系统平台: {sys.platform}")
        print(f"  Python版本: {sys.version}")
        print(f"  当前用户: {os.getlogin() if hasattr(os, 'getlogin') else 'N/A'}")
        print(f"  当前工作目录: {self.current_dir}")
        print()
        
        # PyOS运行信息
        print(f"{c['PURPLE']}🚀 PyOS运行信息:{c['RESET']}")
        current_time = time.time()
        uptime = current_time - self.start_time
        hours = int(uptime // 3600)
        minutes = int((uptime % 3600) // 60)
        seconds = int(uptime % 60)
        print(f"  运行时间: {hours:02d}:{minutes:02d}:{seconds:02d}")
        print(f"  命令执行次数: {self.command_count}")
        print(f"  命令历史记录: {len(self.history)} 条")
        print()
        
        # 内存信息（Windows系统）
        print(f"{c['CYAN']}💾 内存信息:{c['RESET']}")
        try:
            import psutil
            memory = psutil.virtual_memory()
            print(f"  总内存: {memory.total // (1024**3)} GB")
            print(f"  已用内存: {memory.used // (1024**3)} GB")
            print(f"  可用内存: {memory.available // (1024**3)} GB")
            print(f"  内存使用率: {memory.percent}%")
        except ImportError:
            print(f"  {c['YELLOW']}⚠️ 需要安装psutil库来显示详细内存信息{c['RESET']}")
        print()
        
        # 磁盘信息
        print(f"{c['ORANGE']}💽 磁盘信息:{c['RESET']}")
        try:
            disk_usage = shutil.disk_usage(self.current_dir)
            total_gb = disk_usage.total // (1024**3)
            used_gb = disk_usage.used // (1024**3)
            free_gb = disk_usage.free // (1024**3)
            usage_percent = (disk_usage.used / disk_usage.total) * 100
            
            print(f"  磁盘总空间: {total_gb} GB")
            print(f"  已用空间: {used_gb} GB")
            print(f"  可用空间: {free_gb} GB")
            print(f"  使用率: {usage_percent:.1f}%")
        except Exception as e:
            print(f"  {c['RED']}❌ 获取磁盘信息失败: {e}{c['RESET']}")
        print()
        
        # 网络信息
        print(f"{c['TEAL']}🌐 网络信息:{c['RESET']}")
        try:
            import socket
            hostname = socket.gethostname()
            print(f"  主机名: {hostname}")
            
            # 获取本机IP地址
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip_address = s.getsockname()[0]
            s.close()
            print(f"  IP地址: {ip_address}")
        except Exception as e:
            print(f"  {c['RED']}❌ 获取网络信息失败: {e}{c['RESET']}")
        print()
        
        # 系统性能建议
        print(f"{c['PINK']}💡 系统性能建议:{c['RESET']}")
        if len(self.history) > 50:
            print(f"  {c['YELLOW']}⚠️ 命令历史记录较多，建议定期清理{c['RESET']}")
        
        if uptime > 3600:  # 运行超过1小时
            print(f"  {c['GREEN']}✅ 系统运行稳定{c['RESET']}")
        
        print(f"{c['BLUE']}{'='*60}{c['RESET']}")
    
    def history_command(self, args=None):
        """显示命令历史"""
        c = self.COLORS
        
        if not self.history:
            print(f"{c['YELLOW']}📝 命令历史为空{c['RESET']}")
            return
        
        # 解析参数
        show_all = False
        clear_history = False
        search_term = None
        
        if args:
            for arg in args:
                if arg == '-a' or arg == '--all':
                    show_all = True
                elif arg == '-c' or arg == '--clear':
                    clear_history = True
                elif arg == '-h' or arg == '--help':
                    print(f"{c['BLUE']}📖 history命令用法:{c['RESET']}")
                    print(f"  {c['CYAN']}history{c['RESET']}          - 显示最近10条命令")
                    print(f"  {c['CYAN']}history -a{c['RESET']}       - 显示所有命令历史")
                    print(f"  {c['CYAN']}history -c{c['RESET']}       - 清除命令历史")
                    print(f"  {c['CYAN']}history <关键词>{c['RESET']} - 搜索包含关键词的命令")
                    return
                else:
                    search_term = arg
        
        # 清除历史记录
        if clear_history:
            self.history.clear()
            print(f"{c['GREEN']}✅ 命令历史已清除{c['RESET']}")
            return
        
        # 搜索命令历史
        if search_term:
            matching_commands = []
            for i, cmd in enumerate(self.history):
                if search_term.lower() in cmd.lower():
                    matching_commands.append((i + 1, cmd))
            
            if matching_commands:
                print(f"{c['BLUE']}🔍 搜索命令历史 (包含'{search_term}'):{c['RESET']}")
                print(f"{c['GRAY']}{'-'*50}{c['RESET']}")
                for idx, cmd in matching_commands:
                    print(f"{c['PURPLE']}{idx:3d}{c['RESET']}: {cmd}")
                print(f"{c['GREEN']}✅ 找到 {len(matching_commands)} 条匹配命令{c['RESET']}")
            else:
                print(f"{c['YELLOW']}⚠️ 未找到包含'{search_term}'的命令{c['RESET']}")
            return
        
        # 显示命令历史
        print(f"{c['BLUE']}📝 命令历史 (最近{min(10, len(self.history))}条):{c['RESET']}")
        print(f"{c['GRAY']}{'-'*50}{c['RESET']}")
        
        # 确定要显示的命令数量
        if show_all:
            commands_to_show = self.history
            print(f"{c['PURPLE']}显示所有 {len(commands_to_show)} 条命令:{c['RESET']}")
        else:
            commands_to_show = self.history[-10:]  # 显示最近10条
        
        # 显示命令
        start_idx = max(0, len(self.history) - len(commands_to_show))
        for i, cmd in enumerate(commands_to_show):
            cmd_num = start_idx + i + 1
            print(f"{c['PURPLE']}{cmd_num:3d}{c['RESET']}: {cmd}")
        
        # 显示统计信息
        print(f"{c['GRAY']}{'-'*50}{c['RESET']}")
        print(f"{c['CYAN']}总计: {len(self.history)} 条命令{c['RESET']}")
        
        if not show_all and len(self.history) > 10:
            print(f"{c['YELLOW']}提示: 使用 {c['CYAN']}history -a{c['YELLOW']} 查看所有命令{c['RESET']}")
        
        print(f"{c['YELLOW']}提示: 使用 {c['CYAN']}history -c{c['YELLOW']} 清除历史记录{c['RESET']}")
        print(f"{c['YELLOW']}提示: 使用 {c['CYAN']}history <关键词>{c['YELLOW']} 搜索命令{c['RESET']}")
    
    def cat_command(self, args):
        """查看文件内容"""
        c = self.COLORS
        
        if not args:
            print(f"{c['RED']}❌ 用法: cat <文件名> [行数限制]{c['RESET']}")
            print(f"{c['GRAY']}示例: cat readme.txt{c['RESET']}")
            print(f"{c['GRAY']}示例: cat main.py 20{c['RESET']}")
            return
        
        filename = args[0]
        filepath = os.path.join(self.current_dir, filename)
        
        if not os.path.exists(filepath):
            print(f"{c['RED']}❌ 文件不存在: {filename}{c['RESET']}")
            return
        
        if os.path.isdir(filepath):
            print(f"{c['RED']}❌ {filename} 是一个目录，不能查看内容{c['RESET']}")
            return
        
        # 检查文件大小，避免读取过大文件
        file_size = os.path.getsize(filepath)
        if file_size > 1024 * 1024:  # 1MB
            print(f"{c['YELLOW']}⚠️ 文件较大 ({file_size} bytes)，建议使用其他工具查看{c['RESET']}")
            return
        
        # 行数限制
        line_limit = 100  # 默认限制100行
        if len(args) > 1:
            try:
                line_limit = int(args[1])
                if line_limit <= 0:
                    line_limit = 100
            except ValueError:
                print(f"{c['YELLOW']}⚠️ 行数限制无效，使用默认值100{c['RESET']}")
        
        print(f"{c['BLUE']}📄 查看文件: {filename}{c['RESET']}")
        print(f"{c['GRAY']}{'-'*50}{c['RESET']}")
        
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
                
                # 显示文件信息
                print(f"{c['CYAN']}文件大小: {file_size} bytes, 总行数: {len(lines)}{c['RESET']}")
                
                # 显示内容
                for i, line in enumerate(lines[:line_limit]):
                    line_num = i + 1
                    # 简单的语法高亮
                    if filename.endswith('.py'):
                        # Python文件语法高亮
                        if line.strip().startswith('#'):
                            print(f"{c['GRAY']}{line_num:3d}: {line.rstrip()}{c['RESET']}")
                        elif any(keyword in line for keyword in ['def ', 'class ', 'import ', 'from ']):
                            print(f"{c['GREEN']}{line_num:3d}: {line.rstrip()}{c['RESET']}")
                        elif any(keyword in line for keyword in ['if ', 'else:', 'elif ', 'for ', 'while ']):
                            print(f"{c['YELLOW']}{line_num:3d}: {line.rstrip()}{c['RESET']}")
                        else:
                            print(f"{line_num:3d}: {line.rstrip()}")
                    else:
                        # 普通文本文件
                        print(f"{line_num:3d}: {line.rstrip()}")
                
                # 如果文件行数超过限制，显示提示
                if len(lines) > line_limit:
                    remaining = len(lines) - line_limit
                    print(f"{c['YELLOW']}... 还有 {remaining} 行未显示 (使用 cat {filename} {line_limit + 100} 查看更多){c['RESET']}")
                
                print(f"{c['GREEN']}✅ 文件查看完成{c['RESET']}")
                
        except UnicodeDecodeError:
            print(f"{c['RED']}❌ 无法解码文件内容 (可能是二进制文件){c['RESET']}")
        except Exception as e:
            print(f"{c['RED']}❌ 读取文件时出错: {e}{c['RESET']}")
    
    def find_command(self, args):
        """文件搜索功能"""
        c = self.COLORS
        
        if not args:
            print(f"{c['RED']}❌ 用法: find <文件名或模式> [搜索路径]{c['RESET']}")
            print(f"{c['GRAY']}示例: find *.py{c['RESET']}")
            print(f"{c['GRAY']}示例: find main.py{c['RESET']}")
            print(f"{c['GRAY']}示例: find *.txt /home{c['RESET']}")
            return
        
        pattern = args[0]
        search_path = self.current_dir
        
        if len(args) > 1:
            search_path = args[1]
            if not os.path.exists(search_path):
                print(f"{c['RED']}❌ 搜索路径不存在: {search_path}{c['RESET']}")
                return
        
        print(f"{c['BLUE']}🔍 搜索文件: {pattern} 在 {search_path}{c['RESET']}")
        print(f"{c['GRAY']}{'-'*50}{c['RESET']}")
        
        found_count = 0
        
        try:
            for root, dirs, files in os.walk(search_path):
                for file in files:
                    # 简单的模式匹配
                    if pattern == '*' or pattern in file or file.endswith(pattern.replace('*', '')):
                        file_path = os.path.join(root, file)
                        relative_path = os.path.relpath(file_path, search_path)
                        size = os.path.getsize(file_path)
                        
                        # 显示文件信息
                        print(f"{c['CYAN']}{relative_path}{c['RESET']} ({size} bytes)")
                        found_count += 1
                        
                        # 限制显示数量，避免过多输出
                        if found_count >= 100:
                            print(f"{c['YELLOW']}⚠️ 显示前100个结果，更多结果被隐藏{c['RESET']}")
                            break
                
                if found_count >= 100:
                    break
            
            if found_count == 0:
                print(f"{c['YELLOW']}🔍 未找到匹配的文件{c['RESET']}")
            else:
                print(f"{c['GREEN']}✅ 找到 {found_count} 个文件{c['RESET']}")
                
        except Exception as e:
            print(f"{c['RED']}❌ 搜索过程中出错: {e}{c['RESET']}")
    
    def run_python_file(self, args):
        """运行Python文件"""
        c = self.COLORS
        
        if not args:
            print(f"{c['RED']}❌ 用法: python <文件名.py>{c['RESET']}")
            return
        
        filename = args[0]
        filepath = os.path.join(self.current_dir, filename)
        
        if not os.path.exists(filepath):
            print(f"{c['RED']}❌ 文件不存在: {filename}{c['RESET']}")
            return
        
        if not filename.endswith('.py'):
            print(f"{c['YELLOW']}⚠️ 警告: 文件不是Python文件，但仍尝试运行{c['RESET']}")
        
        print(f"{c['BLUE']}🚀 运行Python文件: {filename}{c['RESET']}")
        print(f"{c['GRAY']}{'-'*50}{c['RESET']}")
        
        try:
            # 直接运行Python文件
            result = subprocess.run(
                ['python', filename],
                shell=True,
                cwd=self.current_dir,
                capture_output=True,
                text=False
            )
            
            # 处理编码
            try:
                stdout = result.stdout.decode('gbk', errors='replace')
            except UnicodeDecodeError:
                stdout = result.stdout.decode('utf-8', errors='replace')
                
            try:
                stderr = result.stderr.decode('gbk', errors='replace')
            except UnicodeDecodeError:
                stderr = result.stderr.decode('utf-8', errors='replace')
            
            # 输出结果
            if stdout:
                print(stdout)
            
            if stderr:
                print(f"{c['RED']}错误输出:{c['RESET']}")
                print(stderr)
            
            # 显示返回码
            if result.returncode != 0:
                print(f"{c['YELLOW']}程序执行完成，返回码: {result.returncode}{c['RESET']}")
            else:
                print(f"{c['GREEN']}✅ 程序执行成功{c['RESET']}")
                
        except Exception as e:
            print(f"{c['RED']}❌ 运行Python文件时出错: {e}{c['RESET']}")
    
    def run_in_cmd(self, command, args):
        """在系统cmd中运行命令"""
        c = self.COLORS
        
        try:
            # 构建完整的命令
            full_command = f"{command} {' '.join(args)}".strip()
            
            print(f"{c['BLUE']}在cmd中执行: {full_command}{c['RESET']}")
            print(f"{c['GRAY']}{'-'*50}{c['RESET']}")
            
            # 使用subprocess运行命令，处理中文编码
            result = subprocess.run(
                full_command,
                shell=True,
                cwd=self.current_dir,
                capture_output=True,
                text=False  # 不自动解码，手动处理编码
            )
            
            # 手动处理编码，优先尝试gbk（中文Windows默认编码）
            try:
                stdout = result.stdout.decode('gbk', errors='replace')
            except UnicodeDecodeError:
                stdout = result.stdout.decode('utf-8', errors='replace')
                
            try:
                stderr = result.stderr.decode('gbk', errors='replace')
            except UnicodeDecodeError:
                stderr = result.stderr.decode('utf-8', errors='replace')
            
            # 输出结果
            if stdout:
                print(stdout)
            
            if stderr:
                print(f"{c['RED']}错误输出:{c['RESET']}")
                print(stderr)
            
            # 显示返回码
            if result.returncode != 0:
                print(f"{c['YELLOW']}命令执行完成，返回码: {result.returncode}{c['RESET']}")
            else:
                print(f"{c['GREEN']}命令执行成功{c['RESET']}")
                
        except FileNotFoundError:
            print(f"{c['RED']}❌ 错误: 命令 '{command}' 不存在{c['RESET']}")
        except PermissionError:
            print(f"{c['RED']}❌ 错误: 没有权限执行命令 '{command}'{c['RESET']}")
        except Exception as e:
            print(f"{c['RED']}❌ 执行命令时出错: {e}{c['RESET']}")
    
    def run(self):
        """主运行循环"""
        c = self.COLORS
        
        # 美观的欢迎信息
        print(f"{c['BLUE']}{'='*60}{c['RESET']}")
        print(f"{c['YELLOW']}{c['BOLD']}🚀 欢迎使用 PyOS - Python 类操作系统{c['RESET']}")
        print(f"{c['GRAY']}✨ 现代化的命令行体验 • 功能丰富的开发环境{c['RESET']}")
        print(f"{c['BLUE']}{'='*60}{c['RESET']}")
        print(f"{c['GREEN']}💡 提示: 输入 {c['BOLD']}help{c['RESET']}{c['GREEN']} 查看可用命令{c['RESET']}")
        print(f"{c['GREEN']}💡 提示: 输入 {c['BOLD']}config{c['RESET']}{c['GREEN']} 自定义界面设置{c['RESET']}")
        print(f"{c['BLUE']}{'-'*60}{c['RESET']}")
        
        while self.running:
            try:
                self.display_prompt()
                user_input = input().strip()
                
                if not user_input:
                    continue
                    
                # 添加到历史记录
                self.history.append(user_input)
                if len(self.history) > self.max_history:
                    self.history.pop(0)
                
                # 增加命令计数
                self.command_count += 1
                
                # 解析命令
                command, args = self.parse_command(user_input)
                
                if command:
                    self.execute_command(command, args)
                    
            except KeyboardInterrupt:
                print(f"\n{c['YELLOW']}💡 提示: 使用 {c['BOLD']}exit{c['RESET']}{c['YELLOW']} 或 {c['BOLD']}quit{c['RESET']}{c['YELLOW']} 退出程序{c['RESET']}")
            except EOFError:
                print(f"\n{c['GREEN']}👋 再见! 感谢使用 PyOS{c['RESET']}")
                self.running = False
            except Exception as e:
                print(f"{c['RED']}❌ 错误: {e}{c['RESET']}")

def main():
    """主函数"""
    pyos = PyOS()
    pyos.run()

if __name__ == "__main__":
    main()
