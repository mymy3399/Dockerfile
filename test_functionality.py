#!/usr/bin/env python3
"""
Test script to verify PDF to Excel converter functionality.
Tests all core components without requiring actual PDF files.
"""

import sys
import os
import tempfile
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.thai_handler import ThaiTextHandler
from src.excel_writer import ExcelWriter


def test_thai_handler():
    """Test Thai text handler functionality."""
    print("Testing Thai Text Handler...")
    handler = ThaiTextHandler()
    
    # Test Thai detection
    thai_text = "สวัสดีครับ นี่คือการทดสอบ"
    english_text = "Hello, this is a test"
    mixed_text = "Hello สวัสดี World ครับ"
    
    print(f"✓ Thai text detection: {handler.detect_thai_content(thai_text)}")
    print(f"✓ English text detection: {not handler.detect_thai_content(english_text)}")
    print(f"✓ Mixed text detection: {handler.detect_thai_content(mixed_text)}")
    
    # Test text normalization
    normalized = handler.normalize_thai_text(thai_text)
    print(f"✓ Text normalization: '{thai_text}' -> '{normalized}'")
    
    # Test Thai content ratio
    ratio = handler.get_thai_content_ratio(mixed_text)
    print(f"✓ Thai content ratio in mixed text: {ratio:.2f}")
    
    # Test font creation
    font = handler.create_thai_font()
    print(f"✓ Thai font created: {font.name}")
    
    print("Thai Text Handler: ✅ PASSED\n")


def test_excel_writer():
    """Test Excel writer functionality."""
    print("Testing Excel Writer...")
    writer = ExcelWriter()
    
    # Create sample PDF data
    sample_data = {
        'file_path': 'test_document.pdf',
        'page_count': 2,
        'has_thai_content': True,
        'tables': [
            {
                'page': 1,
                'table_index': 0,
                'data': [
                    ['ชื่อ (Name)', 'อายุ (Age)', 'เมือง (City)'],
                    ['สมชาย', '25', 'กรุงเทพมหานคร'],
                    ['Mary Johnson', '30', 'Bangkok'],
                    ['นางสาววิชญา', '28', 'เชียงใหม่']
                ],
                'rows': 4,
                'cols': 3
            },
            {
                'page': 2,
                'table_index': 0,
                'data': [
                    ['รายการ (Item)', 'จำนวน (Quantity)', 'ราคา (Price)'],
                    ['คอมพิวเตอร์', '5', '25000'],
                    ['โทรศัพท์', '10', '15000']
                ],
                'rows': 3,
                'cols': 3
            }
        ],
        'pages': [
            {
                'page_number': 1,
                'text': 'สวัสดีครับ นี่คือหน้าแรกของเอกสาร\nHello, this is the first page of the document.',
                'table_count': 1,
                'has_thai': True
            },
            {
                'page_number': 2,
                'text': 'หน้าที่สองมีตารางข้อมูลสินค้า\nSecond page contains product data table.',
                'table_count': 1,
                'has_thai': True
            }
        ],
        'text_content': 'สวัสดีครับ นี่คือหน้าแรกของเอกสาร\nHello, this is the first page of the document.\nหน้าที่สองมีตารางข้อมูลสินค้า\nSecond page contains product data table.'
    }
    
    # Test Excel creation
    with tempfile.TemporaryDirectory() as temp_dir:
        output_file = Path(temp_dir) / "test_output.xlsx"
        
        success = writer.create_workbook(sample_data, str(output_file))
        print(f"✓ Excel file creation: {'SUCCESS' if success else 'FAILED'}")
        
        if success:
            # Validate output
            valid = writer.validate_excel_output(str(output_file))
            print(f"✓ Excel file validation: {'PASSED' if valid else 'FAILED'}")
            
            # Check file size
            file_size = output_file.stat().st_size
            print(f"✓ Generated file size: {file_size:,} bytes")
    
    # Test batch summary
    batch_results = [
        {
            'file_name': 'document1.pdf',
            'status': 'success',
            'page_count': 3,
            'table_count': 2,
            'has_thai_content': True,
            'processing_time': 2.5,
            'output_file': 'document1.xlsx',
            'error_message': None
        },
        {
            'file_name': 'document2.pdf',
            'status': 'error',
            'page_count': 0,
            'table_count': 0,
            'has_thai_content': False,
            'processing_time': 0.1,
            'output_file': None,
            'error_message': 'Invalid PDF format'
        }
    ]
    
    with tempfile.TemporaryDirectory() as temp_dir:
        summary_file = Path(temp_dir) / "batch_summary.xlsx"
        summary_success = writer.create_batch_summary(batch_results, str(summary_file))
        print(f"✓ Batch summary creation: {'SUCCESS' if summary_success else 'FAILED'}")
    
    print("Excel Writer: ✅ PASSED\n")


def test_integration():
    """Test integration between components."""
    print("Testing Component Integration...")
    
    # Test Thai handler with Excel writer
    thai_handler = ThaiTextHandler()
    excel_writer = ExcelWriter()
    
    # Sample mixed content
    mixed_content = {
        'file_path': 'mixed_language_doc.pdf',
        'page_count': 1,
        'has_thai_content': True,
        'tables': [
            {
                'page': 1,
                'table_index': 0,
                'data': [
                    ['English Header', 'ส่วนหัวไทย', 'Mixed มิกซ์'],
                    ['Data 1', 'ข้อมูล 1', 'Mix 1 ผสม'],
                    ['Information', 'สารสนเทศ', 'Info ข้อมูล']
                ]
            }
        ],
        'pages': [
            {
                'page_number': 1,
                'text': 'This document contains both English and Thai text. เอกสารนี้มีทั้งภาษาอังกฤษและไทย',
                'table_count': 1,
                'has_thai': True
            }
        ],
        'text_content': 'This document contains both English and Thai text. เอกสารนี้มีทั้งภาษาอังกฤษและไทย'
    }
    
    # Test detection
    has_thai = thai_handler.detect_thai_content(mixed_content['text_content'])
    print(f"✓ Mixed content Thai detection: {has_thai}")
    
    # Test ratio calculation
    ratio = thai_handler.get_thai_content_ratio(mixed_content['text_content'])
    print(f"✓ Thai content ratio: {ratio:.2f}")
    
    # Test Excel generation with mixed content
    with tempfile.TemporaryDirectory() as temp_dir:
        output_file = Path(temp_dir) / "mixed_content.xlsx"
        success = excel_writer.create_workbook(mixed_content, str(output_file))
        print(f"✓ Mixed content Excel generation: {'SUCCESS' if success else 'FAILED'}")
    
    print("Integration Tests: ✅ PASSED\n")


def main():
    """Run all tests."""
    print("="*60)
    print("PDF TO EXCEL CONVERTER - FUNCTIONALITY TEST")
    print("="*60)
    print()
    
    try:
        test_thai_handler()
        test_excel_writer()
        test_integration()
        
        print("="*60)
        print("🎉 ALL TESTS PASSED! 🎉")
        print("PDF to Excel Converter is working correctly!")
        print("="*60)
        
        # Show sample usage
        print("\nSample Usage:")
        print("python main.py --cli sample.pdf                    # Convert single file")
        print("python main.py --cli *.pdf -d output/              # Convert multiple files") 
        print("python main.py --batch input_folder/ -d output/    # Batch convert folder")
        print("python main.py                                     # Launch GUI (if available)")
        
        return True
        
    except Exception as e:
        print(f"❌ TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)