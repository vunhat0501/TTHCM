import re
import json
import os

def read_file_safely(filepath):
    """Attempts to read a file using multiple common encodings to avoid crashes."""
    encodings = ['utf-8', 'utf-8-sig', 'utf-16', 'windows-1258', 'cp1252']
    
    for enc in encodings:
        try:
            with open(filepath, 'r', encoding=enc) as f:
                return f.read()
        except UnicodeDecodeError:
            continue
            
    # If all standard encodings fail, force read it and safely ignore the broken bytes
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        return f.read()

def convert_md_to_json(input_file, output_file):
    # Safety check: ensure the file actually exists
    if not os.path.exists(input_file):
        print(f"Warning: {input_file} not found. Skipping...")
        return
    
    print(f"Đang xử lý {input_file}...")
    content = read_file_safely(input_file)
    lines = content.split('\n')
    
    questions = []
    current_q_num = None
    current_q_text = []
    current_options = []
    current_answer_idx = -1
    
    # Regex to find questions
    q_pattern = re.compile(r'^Câu\s+(\d+)', re.IGNORECASE)
    # Regex to find answer
    opt_pattern = re.compile(r'^\s*(\*?)\s*[A-Z]\.\s*(.*)$', re.IGNORECASE)
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        if line.lower().startswith('phần'):
            continue
        
        q_match = q_pattern.match(line)
        if q_match:
            if current_q_num is not None:
                q_text = f"Câu {current_q_num}: " + " ".join(current_q_text)
                questions.append({
                    "question": q_text,
                    "options": current_options,
                    "answer": current_answer_idx
                })
            
            current_q_num = q_match.group(1)
            current_q_text = []
            current_options = []
            current_answer_idx = -1
            continue
        
        if current_q_num is not None:
            opt_match = opt_pattern.match(line)
            
            if opt_match:
                is_correct = bool(opt_match.group(1))
                opt_text = opt_match.group(2).strip()
                
                if opt_text.endswith('*'):
                    opt_text = opt_text[:-1].strip()
                    
                current_options.append(opt_text)
                
                if is_correct:
                    current_answer_idx = len(current_options) - 1
            
            else:
                if len(current_options) == 0:
                    current_q_text.append(line)
                else:
                    current_options[-1] += " " + line
    if current_q_num is not None:
        q_text = f"Câu {current_q_num}: " + " ".join(current_q_text)
        questions.append({
            "question": q_text,
            "options": current_options,
            "answer": current_answer_idx
        })
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(questions, f, indent=4, ensure_ascii=False)
        
    print(f"\nThành công! Đã trích xuất và chuyển đổi {len(questions)} câu hỏi vào file {output_file}.")

if __name__ == "__main__":
    # Đọc file 200-cloud.md và xuất ra data.json
    convert_md_to_json(input_file='200-cloud.md', output_file='data.json')