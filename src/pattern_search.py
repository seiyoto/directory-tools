#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
递归查找指定目录下匹配指定模式的文件路径（支持通配符）
"""
import os
import fnmatch
import argparse
from typing import List
from colorama import init, Fore, Style

init(autoreset=True)

def _validate_directory(directory: str) -> bool:
    """通用目录有效性校验"""
    if not os.path.exists(directory):
        print(f"{Fore.RED}❌ 错误：目录不存在 -> {directory}")
        return False
    if not os.path.isdir(directory):
        print(f"{Fore.RED}❌ 错误：不是有效目录（可能是文件） -> {directory}")
        return False
    return True

def search_files_by_pattern(directory: str, pattern: str) -> List[str]:
    """
    递归查找目录下匹配指定模式的文件路径
    
    Args:
        directory: 目标目录路径
        pattern: 文件匹配模式（支持通配符，如*.txt、test*.py）
    
    Returns:
        List[str]: 匹配的文件路径列表，失败返回空列表
    """
    if not _validate_directory(directory):
        return []

    matched_files = []

    try:
        for root, dirs, files in os.walk(directory):
            try:
                for file_name in files:
                    # 匹配文件模式
                    if fnmatch.fnmatch(file_name, pattern):
                        file_path = os.path.abspath(os.path.join(root, file_name))
                        matched_files.append(file_path)
            except PermissionError:
                print(f"{Fore.YELLOW}⚠️  警告：无权访问目录，跳过 -> {root}")
            except Exception as e:
                print(f"{Fore.YELLOW}⚠️  警告：处理目录失败 -> {root}，错误：{str(e)}")
    except Exception as e:
        print(f"{Fore.RED}❌ 错误：遍历目录失败 -> {directory}，错误：{str(e)}")
    
    return matched_files

def main():
    """主函数：解析命令行参数并执行"""
    parser = argparse.ArgumentParser(description="递归查找指定目录下匹配指定模式的文件路径（支持通配符）")
    parser.add_argument("directory", help="目标目录的绝对/相对路径")
    parser.add_argument("pattern", help="文件匹配模式（如*.txt、test*.py、*.jpg）")
    args = parser.parse_args()
    
    # 执行查找
    matched_files = search_files_by_pattern(args.directory, args.pattern)
    
    # 输出结果
    if not matched_files:
        print(f"\n{Fore.BLUE}ℹ️  提示：在目录 {args.directory} 中未找到匹配模式 '{args.pattern}' 的文件")
        return
    
    print(f"\n{Fore.GREEN}✅ 查找完成：")
    print(f"📁 目标目录：{args.directory}")
    print(f"🔍 匹配模式：{args.pattern}")
    print(f"📊 匹配结果（共 {len(matched_files)} 个文件）：")
    for idx, file_path in enumerate(matched_files, start=1):
        print(f"  {idx:>3}. {file_path}")

if __name__ == "__main__":
    main()
