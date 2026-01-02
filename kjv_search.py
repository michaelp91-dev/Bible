import textwrap
import shutil

def get_subscript(number):
    """Converts a standard number string into Unicode subscripts."""
    sub_map = {
        "0": "₀", "1": "₁", "2": "₂", "3": "₃", "4": "₄",
        "5": "₅", "6": "₆", "7": "₇", "8": "₈", "9": "₉"
    }
    return "".join(sub_map.get(char, char) for char in str(number))

def search_kjvdat_pro(file_path, book_abbr, chapter_num):
    # Detect terminal width automatically, default to 80 if it fails
    terminal_width = shutil.get_terminal_size((80, 20)).columns
    # Leave a small margin so it doesn't hit the absolute edge
    wrap_width = max(terminal_width - 4, 40) 

    search_prefix = f"{book_abbr}|{chapter_num}|"
    verses_text = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                # Use strip() to remove hidden newline characters before checking prefix
                clean_line = line.strip()
                if clean_line.startswith(search_prefix):
                    parts = clean_line.split('|')
                    if len(parts) >= 4:
                        verse_num = parts[2]
                        # Clean the text: remove the trailing ~ and any extra whitespace
                        text = parts[3].replace('~', '').strip()
                        
                        sub_v = get_subscript(verse_num)
                        verses_text.append(f"{sub_v}{text}")
            
            if verses_text:
                full_text = " ".join(verses_text)
                
                # Header Formatting
                header = f"--- {book_abbr.upper()} CHAPTER {chapter_num} ---"
                print("\n" + header.center(wrap_width))
                print("=" * wrap_width)
                
                # Text Wrapping Logic
                # replace_whitespace=False keeps the single spaces we added
                # drop_whitespace=True prevents lines from starting with a space
                wrapper = textwrap.TextWrapper(width=wrap_width, 
                                               replace_whitespace=False, 
                                               drop_whitespace=True)
                
                formatted_lines = wrapper.wrap(full_text)
                for line in formatted_lines:
                    print(line)
                
                print("=" * wrap_width + "\n")
            else:
                print(f"Error: Could not find {book_abbr} {chapter_num}.")
                print("Check if abbreviations match (e.g., Gen, Exo, Mat).")
                
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found in the current directory.")
