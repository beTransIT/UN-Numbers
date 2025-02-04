import os
import json
import pdfplumber
import re

def clean_description(text):
    """Clean description text by replacing newlines with spaces and removing extra whitespace."""
    if not text:
        return ""
    return ' '.join(text.replace('\n', ' ').split())

def get_column_indices(row):
    """Get the indices of important columns from the numbered row."""
    indices = {}
    for i, cell in enumerate(row):
        cell_text = str(cell or '')
        if '(1)' in cell_text:
            indices['number'] = i
        elif '(2)' in cell_text:
            indices['description'] = i
        elif '(3a)' in cell_text:
            indices['class'] = i
        elif '(3b)' in cell_text:
            indices['classCode'] = i
        elif '(15)' in cell_text:
            indices['tunnel'] = i
    return indices

def has_required_columns(indices):
    """Check if all required column indices are present."""
    required_columns = ['number', 'description', 'class', 'classCode']
    return all(col in indices for col in required_columns)

def extract_entries_from_pdf(pdf_path):
    """Extract all entries from the PDF file."""
    entries = {}
    tunnel_codes = {}
    
    print(f"Opening PDF file: {pdf_path}")
    with pdfplumber.open(pdf_path) as pdf:
        # First pass: collect tunnel codes
        for page_num, page in enumerate(pdf.pages, 1):
            tables = page.extract_tables()
            for table in tables:
                if not table or len(table) < 4:
                    continue
                
                for row_idx, row in enumerate(table):
                    if row and any('(15)' in str(cell) for cell in row):
                        indices = get_column_indices(row)
                        if 'tunnel' in indices and 'number' in indices:
                            for data_row in table[row_idx + 1:]:
                                if not data_row or len(data_row) <= max(indices['tunnel'], indices['number']):
                                    continue
                                
                                un_match = re.search(r'(\d{4})', str(data_row[indices['number']]))
                                if un_match:
                                    un_number = un_match.group(1).zfill(4)
                                    tunnel = clean_description(str(data_row[indices['tunnel']]))
                                    if tunnel:
                                        tunnel_codes[un_number] = tunnel
        
        # Second pass: collect main entries
        for page_num, page in enumerate(pdf.pages, 1):
            tables = page.extract_tables()
            for table in tables:
                if not table or len(table) < 4:
                    continue
                
                for row_idx, row in enumerate(table):
                    if row and any('(1)' in str(cell) for cell in row):
                        indices = get_column_indices(row)
                        if has_required_columns(indices):
                            for data_row in table[row_idx + 1:]:
                                if not data_row or len(data_row) <= max(indices.values()):
                                    continue
                                
                                if data_row[indices['number']]:
                                    un_match = re.search(r'(\d{4})', str(data_row[indices['number']]))
                                    if un_match:
                                        un_number = un_match.group(1).zfill(4)
                                        
                                        entries[un_number] = {
                                            "number": un_number,
                                            "description": clean_description(str(data_row[indices['description']])),
                                            "class": str(data_row[indices['class']]).strip(),
                                            "classCode": str(data_row[indices['classCode']]).strip(),
                                            "tunnel": tunnel_codes.get(un_number, "")
                                        }
    
    entries_list = list(entries.values())
    print(f"\nTotal entries found: {len(entries_list)}")
    print(f"Total tunnel codes found: {len(tunnel_codes)}")
    return entries_list

def main():
    if not os.path.exists('data'):
        os.makedirs('data')
    
    print("\nStarting PDF processing...")
    entries = extract_entries_from_pdf('unnumberdata.pdf')
    
    print("\nCreating JSON files...")
    for entry in entries:
        json_path = os.path.join('data', f"{entry['number']}.json")
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(entry, f, ensure_ascii=False, indent=2)
    
    print(f"Processing complete. Created {len(entries)} JSON files.")

if __name__ == "__main__":
    main()
