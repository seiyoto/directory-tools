#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
递归计算指定目录的总大小，支持字节/KB/MB/GB格式化输出
"""
import os
import argparse
from typing import Union
from colorama import init, Fore, Style

# 初始化colorama，支持跨平台彩色输出
init(autoreset=True)

def _validate_directory(directory: str) -> bool:
    """
    通用目录有效性校验
    
    Args:
        directory: 待校验的目录路径
    
    Returns:
        bool: 有效返回True，无效返回False
    """
    if not os.path.exists(directory):
        print(f"{Fore.RED}错误：目录不存在 -> {directory}")
        return False
    if not os.path.isdir(directory):
        print(f"{Fore.RED}错误：不是有效目录（可能是文件） -> {directory}")
        return False
    return True

def calculate_dir_size(directory: str) -> Union[int, float]:
    """
    递归计算目录总大小（字节）
    
    Args:
        directory: 目标目录路径
    
    Returns:
        Union[int, float]: 目录总字节数，失败返回0
    """
    if not _validate_directory(directory):
        return 0

    total_size = 0
    try:
        # 遍历目录下所有项
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            # 如果是文件，直接累加大小
            if os.path.isfile(item_path):
                try:
                    total_size += os.path.getsize(item_path)
                except PermissionError:
                    print(f"{Fore.YELLOW}⚠️  警告：无权访问文件，跳过 -> {item_path}")
                except Exception as e:
                    print(f"{Fore.YELLOW}⚠️  警告：读取文件大小失败 -> {item_path}，错误：{str(e)}")
            # 如果是目录，递归计算
            elif os.path.isdir(item_path):
                total_size += calculate_dir_size(item_path)
    except PermissionError:
        print(f"{Fore.YELLOW}⚠️  警告：无权访问目录，跳过 -> {directory}")
    except Exception as e:
        print(f"{Fore.RED}❌ 错误：处理目录失败 -> {directory}，错误：{str(e)}")
    
    return total_size

def format_size(size_bytes: Union[int, float]) -> dict:
    """
    将字节数格式化为 KB/MB/GB（保留2位小数）
    
    Args:
        size_bytes: 原始字节数
    
    Returns:
        dict: 包含不同单位的大小字典
    """
    size_kb = size_bytes / 1024
    size_mb = size_kb / 1024
    size_gb = size_mb / 1024
    return {
        "bytes": size_bytes,
        "KB": round(size_kb, 2),
        "MB": round(size_mb, 2),
        "GB": round(size_gb, 2)
    }

def main():
    """主函数：解析命令行参数并执行"""
    # 命令行参数解析
    parser = argparse.ArgumentParser(description="递归计算目录总大小（支持字节/KB/MB/GB）")
    parser.add_argument("directory", help="目标目录的绝对/相对路径")
    args = parser.parse_args()
    
    # 计算并格式化大小
    total_bytes = calculate_dir_size(args.directory)
    if total_bytes == 0:
        return
    
    size_info = format_size(total_bytes)
    
    # 友好输出结果
    print(f"\n{Fore.GREEN}✅ 目录大小计算完成：")
    print(f"📁 目标目录：{args.directory}")
    print(f"📊 大小统计：")
    for unit, value in size_info.items():
        print(f"  - {unit.upper()}: {value}")

if __name__ == "__main__":
    main()
