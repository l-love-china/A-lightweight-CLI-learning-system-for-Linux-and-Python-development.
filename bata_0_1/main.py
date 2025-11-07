
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

class PyOS:
    """Python 类操作系统命令行工具"""
    
    def __init__(self):
        self.current_dir = os.getcwd()
        self.running = True
        
    def display_prompt(self):
        """显示命令行提示符"""
        current_dir_name = os.path.basename(self.current_dir)
        return f"PyOS:{current_dir_name}> "
    
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
    
    def help_command(self, args=None):
        """显示帮助信息"""
        print("""
PyOS 命令列表:

文件系统命令:
  dir              - 显示当前目录内容
  cd <目录路径>    - 切换目录 (cd .. 返回上级目录)
  new <文件名>     - 新建文件
  new /j <文件夹名> - 新建文件夹
  pwd              - 显示当前工作目录
  del <名称>       - 删除文件或文件夹

编辑器命令:
  pyb <文件名>     - Python代码编辑器（语法高亮）
  txtb <文件名>    - 文本编辑器（无高亮）

编辑器内部命令:
  :w               - 保存文件
  :q               - 退出编辑器
  :wq              - 保存并退出
  :wq /c <文件名>  - 另存为并退出
  add <内容>       - 添加新行
  del <行号>       - 删除指定行

系统命令:
  help             - 显示此帮助信息
  exit             - 退出程序

示例:
  dir              # 显示当前目录
  cd Documents     # 切换到Documents目录
  cd ..            # 返回上级目录
  new test.txt     # 新建文件test.txt
  new /j myfolder  # 新建文件夹myfolder
  pyb hello.py     # 编辑Python文件
  txtb readme.txt  # 编辑文本文件
  del oldfile.txt  # 删除文件

编辑器使用示例:
  pyb test.py      # 编辑Python文件
  :w               # 保存文件
  :wq              # 保存并退出
  :wq /c new.py    # 另存为new.py并退出
""")
    
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
            'pyb': self.pyb_command,
            'txtb': self.txtb_command,
            'help': self.help_command,
            'exit': self.exit_command,
            'quit': self.exit_command
        }
        
        if command in command_map:
            command_map[command](args)
        else:
            print(f"未知命令: {command}。输入 'help' 查看可用命令。")
    
    def run(self):
        """主运行循环"""
        print("欢迎使用 PyOS - Python 类操作系统")
        print("输入 'help' 查看可用命令")
        print("-" * 50)
        
        while self.running:
            try:
                command_line = input(self.display_prompt())
                command, args = self.parse_command(command_line)
                
                if command:
                    self.execute_command(command, args)
                    
            except KeyboardInterrupt:
                print("\n使用 Ctrl+C 退出，请输入 'exit' 或 'quit' 退出程序")
            except EOFError:
                print("\n检测到文件结束，退出程序")
                break
            except Exception as e:
                print(f"错误: {e}")

def main():
    """主函数"""
    pyos = PyOS()
    pyos.run()

if __name__ == "__main__":
    main()
