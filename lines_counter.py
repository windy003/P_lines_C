import os

def is_text_file(file_path, block_size=1024):
    """
    Tries to guess if a file is a text file by reading a block of it.
    It checks for the absence of null bytes.
    """
    try:
        with open(file_path, 'rb') as f:
            block = f.read(block_size)
        if b'\0' in block:
            return False
    except IOError:
        return False
    
    try:
        block.decode('utf-8')
        return True
    except UnicodeDecodeError:
        return False

def count_and_sort_file_lines():
    """
    Counts lines in all detected text files in the current directory and all subdirectories,
    then prints the total lines and lines by file type.
    """
    type_lines = {}
    total_lines = 0
    
    print("Scanning files in the current directory and all subdirectories...")
    try:
        script_name = os.path.basename(__file__)

        for root, dirs, files in os.walk('.'):
            for filename in files:
                file_path = os.path.join(root, filename)
                relative_path = os.path.relpath(file_path, '.')
                
                if relative_path != script_name:
                    if is_text_file(file_path):
                        try:
                            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                                line_count = sum(1 for line in f)
                                total_lines += line_count
                                
                                # Get file extension
                                _, ext = os.path.splitext(filename)
                                if not ext:
                                    ext = "no extension"
                                else:
                                    ext = ext.lower()
                                
                                if ext not in type_lines:
                                    type_lines[ext] = 0
                                type_lines[ext] += line_count
                        except Exception as e:
                            print(f"Could not process file {relative_path}: {e}")
        
        print("\n--- Line Count by File Type (from highest to lowest) ---")
        for file_type, line_count in sorted(type_lines.items(), key=lambda x: x[1], reverse=True):
            print(f"{file_type:<15}: {line_count:>8} lines")

        print("----------------------------------")
        print(f"Total lines: {total_lines}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    count_and_sort_file_lines()
