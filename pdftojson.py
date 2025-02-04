import os
import json
import pdfplumber
import re

def clean_description(text):
    """Clean description text by replacing newlines with spaces and removing extra whitespace."""
    if not text:
        return ""
    # Replace newlines with spaces and remove multiple spaces
    return ' '.join(text.replace('\n', ' ').split())

def extract_entries_from_pdf(pdf_path):
    """Extract all entries from the PDF file."""
    entries = []
    
    print(f"Opening PDF file: {pdf_path}")
    with pdfplumber.open(pdf_path) as pdf:
        print(f"Number of pages in PDF: {len(pdf.pages)}")
        
        for page_num, page in enumerate(pdf.pages, 1):
            print(f"\nProcessing page {page_num}")
            
            # Extract tables from the page
            tables = page.extract_tables()
            if not tables:
                continue
                
            print(f"Found {len(tables)} tables on page {page_num}")
            
            for table in tables:
                # Skip empty tables
                if not table:
                    continue
                    
                # Process each row in the table
                for row in table:
                    if not row or len(row) < 3:  # Skip rows without enough columns
                        continue
                        
                    # Try to extract UN number from first column
                    un_number = None
                    description = None
                    classification = None
                    
                    # Look for UN number pattern in the first column
                    if row[0]:
                        un_match = re.search(r'(\d{4})', str(row[0]))
                        if un_match:
                            un_number = un_match.group(1)
                    
                    # Get description from second column if it exists
                    if len(row) > 1 and row[1]:
                        description = clean_description(str(row[1]))
                    
                    # Get classification from third column if it exists
                    if len(row) > 2 and row[2]:
                        class_match = re.search(r'(\d+)', str(row[2]))
                        if class_match:
                            classification = class_match.group(1)
                    
                    # If we found a UN number, create an entry
                    if un_number:
                        entry = {
                            "number": un_number.zfill(4),
                            "description": description or "",
                            "class": classification or "",
                            "tunnel": ""  # Will be filled in later
                        }
                        entries.append(entry)
                        print(f"Found entry: UN {entry['number']}")
            
            # Look for tunnel codes on the page
            text = page.extract_text() or ""
            lines = text.split('\n')
            
            current_un = None
            for line in lines:
                # Look for UN number
                un_match = re.search(r'UN No\.\s*(\d{4})', line)
                if un_match:
                    current_un = un_match.group(1).zfill(4)
                
                # Look for tunnel code
                tunnel_match = re.search(r'Tunnel restriction code:\s*([A-E](/[A-E])?)', line)
                if tunnel_match and current_un:
                    tunnel_code = tunnel_match.group(1)
                    # Update the corresponding entry
                    for entry in entries:
                        if entry["number"] == current_un:
                            entry["tunnel"] = tunnel_code
                            print(f"Added tunnel code {tunnel_code} to UN {current_un}")
                            break
    
    print(f"\nTotal entries found: {len(entries)}")
    return entries

def main():
    # Create newData directory if it doesn't exist
    if not os.path.exists('newData'):
        os.makedirs('newData')
        print("Created newData directory")
    
    # Process the unnumberdata PDF
    print("\nStarting PDF processing...")
    entries = extract_entries_from_pdf('unnumberdata.pdf')
    
    # Create JSON files for each entry
    print("\nCreating JSON files...")
    for entry in entries:
        json_filename = f"{entry['number']}.json"
        json_path = os.path.join('newData', json_filename)
        
        # Write data to JSON file
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(entry, f, ensure_ascii=False, indent=2)
        
        print(f"Created {json_filename}")
    
    print(f"\nProcessing complete. Created {len(entries)} JSON files.")

if __name__ == "__main__":
    main()
