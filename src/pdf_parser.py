"""
PDF Parser module for extracting text and tables from PDF files.
Handles Thai language content properly.
"""

import re
import logging
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path

import pdfplumber
import fitz  # PyMuPDF
import pandas as pd


class PDFParser:
    """PDF parser class for extracting text and tables with Thai language support."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        # Thai Unicode range
        self.thai_pattern = re.compile(r'[\u0E00-\u0E7F]')
        
    def extract_text_and_tables(self, pdf_path: str) -> Dict[str, Any]:
        """
        Extract text and tables from PDF file.
        
        Args:
            pdf_path (str): Path to PDF file
            
        Returns:
            Dict containing extracted text, tables, and metadata
        """
        try:
            pdf_path = Path(pdf_path)
            if not pdf_path.exists():
                raise FileNotFoundError(f"PDF file not found: {pdf_path}")
                
            self.logger.info(f"Processing PDF: {pdf_path}")
            
            result = {
                'file_path': str(pdf_path),
                'pages': [],
                'tables': [],
                'text_content': '',
                'has_thai_content': False,
                'page_count': 0
            }
            
            # Use pdfplumber for primary extraction
            with pdfplumber.open(pdf_path) as pdf:
                result['page_count'] = len(pdf.pages)
                
                for page_num, page in enumerate(pdf.pages, 1):
                    self.logger.debug(f"Processing page {page_num}")
                    
                    # Extract text
                    text = page.extract_text() or ""
                    result['text_content'] += text + "\n"
                    
                    # Check for Thai content
                    if not result['has_thai_content'] and self.detect_thai_content(text):
                        result['has_thai_content'] = True
                    
                    # Extract tables
                    tables = page.extract_tables()
                    for table_idx, table in enumerate(tables):
                        if table:  # Skip empty tables
                            table_data = {
                                'page': page_num,
                                'table_index': table_idx,
                                'data': self._clean_table_data(table),
                                'rows': len(table),
                                'cols': len(table[0]) if table else 0
                            }
                            result['tables'].append(table_data)
                    
                    # Store page info
                    page_info = {
                        'page_number': page_num,
                        'text': text,
                        'table_count': len(tables),
                        'has_thai': self.detect_thai_content(text)
                    }
                    result['pages'].append(page_info)
            
            self.logger.info(f"Extraction complete. Pages: {result['page_count']}, "
                           f"Tables: {len(result['tables'])}, Thai content: {result['has_thai_content']}")
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error extracting from PDF {pdf_path}: {str(e)}")
            raise
    
    def extract_with_pymupdf(self, pdf_path: str) -> Dict[str, Any]:
        """
        Alternative extraction method using PyMuPDF for better Thai text handling.
        
        Args:
            pdf_path (str): Path to PDF file
            
        Returns:
            Dict containing extracted content
        """
        try:
            result = {
                'file_path': str(pdf_path),
                'text_content': '',
                'has_thai_content': False,
                'page_count': 0
            }
            
            doc = fitz.open(pdf_path)
            result['page_count'] = doc.page_count
            
            for page_num in range(doc.page_count):
                page = doc[page_num]
                text = page.get_text("text")
                result['text_content'] += text + "\n"
                
                if not result['has_thai_content'] and self.detect_thai_content(text):
                    result['has_thai_content'] = True
            
            doc.close()
            return result
            
        except Exception as e:
            self.logger.error(f"Error with PyMuPDF extraction: {str(e)}")
            raise
    
    def detect_thai_content(self, text: str) -> bool:
        """
        Check if text contains Thai characters.
        
        Args:
            text (str): Text to check
            
        Returns:
            bool: True if Thai content is found
        """
        if not text:
            return False
        return bool(self.thai_pattern.search(text))
    
    def _clean_table_data(self, table: List[List[str]]) -> List[List[str]]:
        """
        Clean and normalize table data.
        
        Args:
            table: Raw table data from PDF
            
        Returns:
            Cleaned table data
        """
        if not table:
            return []
        
        cleaned_table = []
        for row in table:
            cleaned_row = []
            for cell in row:
                # Handle None values and strip whitespace
                cleaned_cell = str(cell).strip() if cell is not None else ""
                cleaned_row.append(cleaned_cell)
            cleaned_table.append(cleaned_row)
        
        return cleaned_table
    
    def convert_tables_to_dataframes(self, tables: List[Dict]) -> List[pd.DataFrame]:
        """
        Convert extracted tables to pandas DataFrames.
        
        Args:
            tables: List of table dictionaries
            
        Returns:
            List of pandas DataFrames
        """
        dataframes = []
        
        for table in tables:
            try:
                data = table['data']
                if not data:
                    continue
                
                # Use first row as headers if it looks like headers
                headers = data[0] if data else []
                rows = data[1:] if len(data) > 1 else []
                
                # Create DataFrame
                df = pd.DataFrame(rows, columns=headers)
                
                # Add metadata
                df.attrs['page'] = table['page']
                df.attrs['table_index'] = table['table_index']
                
                dataframes.append(df)
                
            except Exception as e:
                self.logger.warning(f"Error converting table to DataFrame: {str(e)}")
                continue
        
        return dataframes
    
    def validate_pdf_file(self, pdf_path: str) -> bool:
        """
        Validate if file is a readable PDF.
        
        Args:
            pdf_path (str): Path to PDF file
            
        Returns:
            bool: True if valid PDF file
        """
        try:
            pdf_path = Path(pdf_path)
            
            # Check file exists and has PDF extension
            if not pdf_path.exists() or pdf_path.suffix.lower() != '.pdf':
                return False
            
            # Try to open with pdfplumber
            with pdfplumber.open(pdf_path) as pdf:
                return len(pdf.pages) > 0
                
        except Exception:
            return False


def main():
    """Test function for PDF parser."""
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    
    parser = PDFParser()
    
    # Test with a sample file (would need actual PDF file)
    print("PDF Parser initialized successfully")
    print("Thai content detection pattern:", parser.thai_pattern.pattern)


if __name__ == "__main__":
    main()