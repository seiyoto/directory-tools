#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统计指定目录下的文件总数、子目录总数（递归）
"""
import os
import argparse
from typing import Tuple
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

def count_dir_items(directory: str) -> Tuple[int, int]:
    """
    递归统计目录下的文件数和子目录数
    
    Args:
        directory: 目标目录路径
    
    Returns:
        Tuple[int, int]: (文件总数, 子目录总数)，失败返回(0, 0)
    """
    if not _validate_directory(directory):
        return 0, 0

    file_count = 0
    dir_count = 0

    try:
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            try:
                if os.path.isfile(item_path):
                    file_count += 1
                elif os.path.isdir(item_path):
                    dir_count += 1
                    # 递归统计子目录
                    sub_file, sub_dir = count_dir_items(item_path)
                    file_count += sub_file
                    dir_count += sub_dir
            except PermissionError:
                print(f"{Fore.YELLOW}⚠️  警告：无权访问，跳过 -> {item_path}")
            except Exception as e:
                print(f"{Fore.YELLOW}⚠️  警告：处理项失败 -> {item_path}，错误：{str(e)}")
    except PermissionError:
        print(f"{Fore.YELLOW}⚠️  警告：无权访问目录，跳过 -> {directory}")
    except Exception as e:
        print(f"{Fore.RED}❌ 错误：处理目录失败 -> {directory}，错误：{str(e)}")
    
    return file_count, dir_count

def main():
    """主函数：解析命令行参数并执行"""
    parser = argparse.ArgumentParser(description="递归统计目录下的文件总数和子目录总数")
    parser.add_argument("directory", help="目标目录的绝对/相对路径")
    args = parser.parse_args()
    
    file_total, dir_total = count_dir_items(args.directory)
    if file_total == 0 and dir_total == 0:
        return
    
    # 友好输出结果
    print(f"\n{Fore.GREEN}✅ 目录统计完成：")
    print(f"📁 目标目录：{args.directory}")
    print(f"📊 统计结果：")
    print(f"  - 文件总数：{file_total}")
    print(f"  - 子目录总数：{dir_total}")

if __name__ == "__main__":
    main()
