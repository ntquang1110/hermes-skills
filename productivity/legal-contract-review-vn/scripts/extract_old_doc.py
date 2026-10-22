#!/usr/bin/env python3
"""
Extract readable Vietnamese text from old .doc (OLE2) format files.
Usage: python extract_old_doc.py <file.doc>
"""
import olefile
import re
import sys

def extract_doc_text(filepath):
    """Extract text from old OLE2 .doc files."""
    try:
        ole = olefile.OleFileIO(filepath)
    except Exception as e:
        print(f"Error opening OLE2 file: {e}")
        return ""
    
    if not ole.exists('WordDocument'):
        print("Not a valid Word document (no WordDocument stream)")
        ole.close()
        return ""
    
    data = ole.openstream('WordDocument').read()
    ole.close()
    
    # Decode UTF-16LE (standard for Word documents)
    text = data.decode('utf-16-le', errors='replace')
    
    # Extract readable Vietnamese text segments
    segments = re.findall(
        r'[A-Za-zÀ-ỹ0-9\s.,;:()\-/\%"\'\u2013\u2014\u2018\u2019\u201c\u201dđ]+',
        text
    )
    
    result = []
    for seg in segments:
        s = seg.strip()
        if len(s) > 10:
            result.append(s)
    
    return '\n---\n'.join(result)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python extract_old_doc.py <file.doc>")
        sys.exit(1)
    
    text = extract_doc_text(sys.argv[1])
    print(text)
