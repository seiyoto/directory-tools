#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
在指定文件中查找包含目标字符串的行，输出行号和匹配内容
"""
import os
import argparse
import chardet
from colorama import init, Fore, Style

init(autoreset=True)

def _validate_file(file_path: str) -> bool:
    """
    通用文件有效性校验
    
    Args:
        file_path: 待校验的文件路径
    
    Returns:
        bool: 有效返回True，无效返回False
    """
    if not os.path.exists(file_path):
        print(f"{Fore.RED}❌ 错误：文件不存在 -> {file_path}")
        return False
    if not os.path.isfile(file_path):
        print(f"{Fore.RED}❌ 错误：不是有效文件（可能是目录） -> {file_path}")
        return False
    return True

def detect_file_encoding(file_path: str) -> str:
    """
    自动检测文件编码（解决中文乱码问题）
    
    Args:
        file_path: 目标文件路径
    
    Returns:
        str: 检测到的编码（默认utf-8）
    """
    try:
        with open(file_path, 'rb') as f:
            raw_data = f.read(1024)  # 读取前1024字节检测编码
            result = chardet.detect(raw_data)
            encoding = result['encoding'] or 'utf-8'
            return encoding
    except Exception as e:
        print(f"{Fore.YELLOW}⚠️  警告：检测编码失败，使用默认编码utf-8，错误：{str(e)}")
        return 'utf-8'

def search_string_in_file(file_path: str, target_str: str, ignore_case: bool = False) -> list:
    """
    在文件中查找目标字符串，返回匹配的行信息
    
    Args:
        file_path: 目标文件路径
        target_str: 要查找的字符串
        ignore_case: 是否忽略大小写（默认False）
    
    Returns:
        list: 匹配结果，每个元素为 (行号, 行内容)，无匹配返回空列表
    """
    if not _validate_file(file_path):
        return []

    matches = []
    encoding = detect_file_encoding(file_path)
    
    try:
        with open(file_path, 'r', encoding=encoding, errors='ignore') as f:
            for line_num, line_content in enumerate(f, start=1):
                # 处理换行符和空格
                line_stripped = line_content.strip()
                # 忽略大小写处理
                compare_line = line_stripped.lower() if ignore_case else line_stripped
                compare_target = target_str.lower() if ignore_case else target_str
                
                if compare_target in compare_line:
                    matches.append((line_num, line_content.rstrip()))  # 保留原行内容（去掉末尾换行）
    except Exception as e:
        print(f"{Fore.RED}❌ 错误：读取文件失败 -> {file_path}，错误：{str(e)}")
        return []
    
    return matches

def main():
    """主函数：解析命令行参数并执行"""
    parser = argparse.ArgumentParser(description="在指定文件中查找包含目标字符串的行，输出行号和匹配内容")
    parser.add_argument("target_str", help="要查找的目标字符串")
    parser.add_argument("file_path", help="目标文件的绝对/相对路径")
    parser.add_argument("-i", "--ignore-case", action="store_true", help="忽略大小写（默认不忽略）")
    args = parser.parse_args()
    
    # 执行查找
    matches = search_string_in_file(args.file_path, args.target_str, args.ignore_case)
    
    # 输出结果
    if not matches:
        print(f"\n{Fore.BLUE}ℹ️  提示：在文件 {args.file_path} 中未找到字符串 '{args.target_str}'")
        return
    
    print(f"\n{Fore.GREEN}✅ 查找完成：")
    print(f"📄 目标文件：{args.file_path}")
    print(f"🔍 查找字符串：{args.target_str}（忽略大小写：{args.ignore_case}）")
    print(f"📊 匹配结果（共 {len(matches)} 行）：")
    for line_num, line_content in matches:
        # 高亮显示匹配的字符串
        highlighted = line_content.replace(
            args.target_str, 
            f"{Fore.RED}{Style.BRIGHT}{args.target_str}{Style.RESET_ALL}",
            1 if ignore_case else -1  # 忽略大小写时只高亮第一个匹配（避免编码问题）
        )
        print(f"  行{line_num:>4}: {highlighted}")

if __name__ == "__main__":
    main()
