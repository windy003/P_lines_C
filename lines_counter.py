import os
import argparse

# 默认排除的目录:版本控制、依赖、构建产物、缓存等
DEFAULT_EXCLUDE_FOLDERS = {
    '.git', '.svn', '.hg',
    'node_modules', 'bower_components',
    'venv', '.venv', 'env', '.env',
    '__pycache__', '.pytest_cache', '.mypy_cache',
    'dist', 'build', 'out', 'target',
    '.idea', '.vscode',
}

def parse_args():
    parser = argparse.ArgumentParser(description='Count lines in text files.')
    parser.add_argument('path', nargs='?', default='.',
                        help='Directory to scan (default: current directory)')
    parser.add_argument('--exclude-folder', nargs='+', default=[], help='Folder names to exclude')
    parser.add_argument('--exclude-file', nargs='+', default=[], help='File names to exclude')
    parser.add_argument('--no-default-excludes', action='store_true',
                        help='Do not exclude .git/node_modules/venv etc. by default')
    return parser.parse_args()

def is_text_file(file_path, block_size=4096):
    """
    通过读取文件开头一段来判断是否为文本文件。
    判定标准:不含 NUL 字节。

    注意:不在这里做严格的 utf-8 解码,因为按固定字节数读取可能
    把一个多字节字符(如中文)截断,导致 utf-8 文本被误判为二进制。
    """
    try:
        with open(file_path, 'rb') as f:
            block = f.read(block_size)
    except (IOError, OSError):
        return False

    # 空文件视为文本文件
    if not block:
        return True

    # 含 NUL 字节几乎可以确定是二进制
    if b'\0' in block:
        return False

    return True

def count_and_sort_file_lines(scan_path='.', exclude_folders=None, exclude_files=None):
    """
    统计指定目录及其所有子目录下文本文件的行数,
    并按文件类型输出行数,以及总行数。
    """
    exclude_folders = set(exclude_folders or [])
    exclude_files = set(exclude_files or [])
    type_lines = {}
    type_files = {}
    total_lines = 0
    total_files = 0

    print(f"Scanning: {os.path.abspath(scan_path)}")
    if exclude_folders:
        print(f"Excluding folders: {', '.join(sorted(exclude_folders))}")
    if exclude_files:
        print(f"Excluding files: {', '.join(sorted(exclude_files))}")
    print("Scanning files in the given directory and all subdirectories...")

    try:
        script_name = os.path.basename(__file__)

        for root, dirs, files in os.walk(scan_path):
            # 原地过滤,os.walk 就不会再进入被排除的目录
            dirs[:] = [d for d in dirs if d not in exclude_folders]
            for filename in files:
                file_path = os.path.join(root, filename)
                relative_path = os.path.relpath(file_path, scan_path)

                # 跳过脚本自身和被排除的文件
                if os.path.abspath(file_path) == os.path.abspath(__file__):
                    continue
                if filename in exclude_files:
                    continue
                if not is_text_file(file_path):
                    continue

                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        line_count = sum(1 for _ in f)
                except Exception as e:
                    print(f"Could not process file {relative_path}: {e}")
                    continue

                total_lines += line_count
                total_files += 1

                _, ext = os.path.splitext(filename)
                ext = ext.lower() if ext else "no extension"

                type_lines[ext] = type_lines.get(ext, 0) + line_count
                type_files[ext] = type_files.get(ext, 0) + 1

        print("\n--- Line Count by File Type (from highest to lowest) ---")
        for file_type, line_count in sorted(type_lines.items(), key=lambda x: x[1], reverse=True):
            print(f"{file_type:<15}: {line_count:>8} lines  ({type_files[file_type]} files)")

        print("----------------------------------")
        print(f"Total: {total_lines} lines in {total_files} files")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    args = parse_args()
    excludes = set(args.exclude_folder)
    if not args.no_default_excludes:
        excludes |= DEFAULT_EXCLUDE_FOLDERS
    count_and_sort_file_lines(args.path, excludes, args.exclude_file)
