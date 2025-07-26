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
    Counts lines in all detected text files in the current directory,
    then prints the results sorted by line count in descending order.
    """
    file_lines = []
    total_lines = 0
    
    print("Scanning files in the current directory...")
    try:
        script_name = os.path.basename(__file__)

        for filename in os.listdir('.'):
            if os.path.isfile(filename) and filename != script_name:
                if is_text_file(filename):
                    try:
                        with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
                            line_count = sum(1 for line in f)
                            total_lines += line_count
                            file_lines.append((filename, line_count))
                    except Exception as e:
                        print(f"Could not process file {filename}: {e}")
        
        # Sort the list of files by line count in descending order.
        file_lines.sort(key=lambda item: item[1], reverse=True)

        print("\n--- Line Count Report (from highest to lowest) ---")
        for filename, line_count in file_lines:
            print(f"Lines: {line_count:<7} | File: {filename}")

        print("--------------------------------------------------")
        print(f"Total lines in all scanned text files: {total_lines}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    count_and_sort_file_lines()
