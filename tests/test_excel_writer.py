"""
Tests for Excel Writer module.
"""

import unittest
import tempfile
import os
from pathlib import Path
from src.excel_writer import ExcelWriter


class TestExcelWriter(unittest.TestCase):
    """Test cases for Excel writer."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.writer = ExcelWriter()
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up test fixtures."""
        # Clean up temporary files
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_create_workbook(self):
        """Test Excel workbook creation."""
        # Sample PDF data
        test_data = {
            'file_path': 'test.pdf',
            'page_count': 2,
            'has_thai_content': True,
            'tables': [
                {
                    'page': 1,
                    'table_index': 0,
                    'data': [
                        ['Name', 'Age', 'City'],
                        ['สมชาย', '25', 'กรุงเทพ'],
                        ['Mary', '30', 'Bangkok']
                    ],
                    'rows': 3,
                    'cols': 3
                }
            ],
            'pages': [
                {
                    'page_number': 1,
                    'text': 'สวัสดีครับ Hello',
                    'table_count': 1,
                    'has_thai': True
                },
                {
                    'page_number': 2,
                    'text': 'Page 2 content',
                    'table_count': 0,
                    'has_thai': False
                }
            ],
            'text_content': 'สวัสดีครับ Hello\nPage 2 content'
        }
        
        # Create Excel file
        output_path = os.path.join(self.temp_dir, 'test_output.xlsx')
        success = self.writer.create_workbook(test_data, output_path)
        
        self.assertTrue(success)
        self.assertTrue(os.path.exists(output_path))
    
    def test_table_to_dataframe(self):
        """Test table to DataFrame conversion."""
        table = {
            'page': 1,
            'table_index': 0,
            'data': [
                ['Name', 'Age', 'City'],
                ['John', '25', 'New York'],
                ['สมชาย', '30', 'กรุงเทพ']
            ]
        }
        
        df = self.writer._table_to_dataframe(table)
        
        self.assertEqual(list(df.columns), ['Name', 'Age', 'City'])
        self.assertEqual(len(df), 2)
        self.assertEqual(df.iloc[1]['Name'], 'สมชาย')
    
    def test_create_batch_summary(self):
        """Test batch summary creation."""
        results = [
            {
                'file_name': 'test1.pdf',
                'status': 'success',
                'page_count': 2,
                'table_count': 1,
                'has_thai_content': True,
                'processing_time': 1.5,
                'output_file': 'test1.xlsx',
                'error_message': None
            },
            {
                'file_name': 'test2.pdf',
                'status': 'error',
                'page_count': 0,
                'table_count': 0,
                'has_thai_content': False,
                'processing_time': 0.5,
                'output_file': None,
                'error_message': 'Invalid PDF'
            }
        ]
        
        output_path = os.path.join(self.temp_dir, 'batch_summary.xlsx')
        success = self.writer.create_batch_summary(results, output_path)
        
        self.assertTrue(success)
        self.assertTrue(os.path.exists(output_path))
    
    def test_validate_excel_output(self):
        """Test Excel output validation."""
        # Create a simple Excel file first
        test_data = {
            'file_path': 'test.pdf',
            'page_count': 1,
            'has_thai_content': False,
            'tables': [],
            'pages': [{'page_number': 1, 'text': 'Test', 'table_count': 0, 'has_thai': False}],
            'text_content': 'Test'
        }
        
        output_path = os.path.join(self.temp_dir, 'validation_test.xlsx')
        self.writer.create_workbook(test_data, output_path)
        
        # Test validation
        self.assertTrue(self.writer.validate_excel_output(output_path))
        
        # Test with non-existent file
        self.assertFalse(self.writer.validate_excel_output('nonexistent.xlsx'))


if __name__ == '__main__':
    unittest.main()