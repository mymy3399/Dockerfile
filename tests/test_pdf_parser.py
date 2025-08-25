"""
Tests for PDF Parser module.
"""

import unittest
import tempfile
import os
from pathlib import Path

from src.pdf_parser import PDFParser


class TestPDFParser(unittest.TestCase):
    """Test cases for PDF parser."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.parser = PDFParser()
    
    def test_thai_content_detection(self):
        """Test Thai content detection."""
        # Test Thai text
        thai_text = "สวัสดีครับ นี่คือการทดสอบ"
        self.assertTrue(self.parser.detect_thai_content(thai_text))
        
        # Test English text
        english_text = "Hello, this is a test"
        self.assertFalse(self.parser.detect_thai_content(english_text))
        
        # Test mixed text
        mixed_text = "Hello สวัสดี mixed text"
        self.assertTrue(self.parser.detect_thai_content(mixed_text))
        
        # Test empty text
        self.assertFalse(self.parser.detect_thai_content(""))
        self.assertFalse(self.parser.detect_thai_content(None))
    
    def test_clean_table_data(self):
        """Test table data cleaning."""
        # Test with normal data
        table_data = [
            ["Header 1", "Header 2", "Header 3"],
            ["Row 1 Col 1", "Row 1 Col 2", "Row 1 Col 3"],
            ["Row 2 Col 1", None, "Row 2 Col 3"]
        ]
        
        cleaned = self.parser._clean_table_data(table_data)
        
        self.assertEqual(len(cleaned), 3)
        self.assertEqual(cleaned[2][1], "")  # None should become empty string
        
        # Test with empty table
        self.assertEqual(self.parser._clean_table_data([]), [])
        self.assertEqual(self.parser._clean_table_data(None), [])
    
    def test_validate_pdf_file(self):
        """Test PDF file validation."""
        # Test with non-existent file
        self.assertFalse(self.parser.validate_pdf_file("nonexistent.pdf"))
        
        # Test with non-PDF file
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as temp_file:
            temp_file.write(b"This is not a PDF")
            temp_path = temp_file.name
        
        try:
            self.assertFalse(self.parser.validate_pdf_file(temp_path))
        finally:
            os.unlink(temp_path)
    
    def test_convert_tables_to_dataframes(self):
        """Test table to DataFrame conversion."""
        tables = [
            {
                'page': 1,
                'table_index': 0,
                'data': [
                    ['Name', 'Age', 'City'],
                    ['John', '25', 'New York'],
                    ['สมชาย', '30', 'กรุงเทพ']
                ]
            }
        ]
        
        dataframes = self.parser.convert_tables_to_dataframes(tables)
        
        self.assertEqual(len(dataframes), 1)
        df = dataframes[0]
        self.assertEqual(list(df.columns), ['Name', 'Age', 'City'])
        self.assertEqual(len(df), 2)
        self.assertEqual(df.iloc[1]['Name'], 'สมชาย')


if __name__ == '__main__':
    unittest.main()