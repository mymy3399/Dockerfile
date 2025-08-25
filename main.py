#!/usr/bin/env python3
"""
PDF to Excel Converter - Main Entry Point
โปรแกรมแปลงไฟล์ PDF เป็น Excel (รองรับภาษาไทย)

This is the main entry point for the PDF to Excel converter application.
It provides both GUI and command-line interfaces.
"""

import sys
import os
import argparse
import logging
from pathlib import Path

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Try to import GUI components (may not be available in all environments)
try:
    from src.ui.main_window import MainWindow
    GUI_AVAILABLE = True
except ImportError as e:
    GUI_AVAILABLE = False
    MainWindow = None
    print(f"GUI not available: {e}")

from src.pdf_parser import PDFParser
from src.excel_writer import ExcelWriter
from src.batch_processor import BatchProcessor


def setup_logging(log_level: str = 'INFO'):
    """Set up logging configuration."""
    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f'Invalid log level: {log_level}')
    
    logging.basicConfig(
        level=numeric_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('pdf_to_excel.log', encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )


def convert_single_file_cli(input_file: str, output_file: str = None):
    """Convert a single PDF file via command line interface."""
    try:
        # Initialize processors
        pdf_parser = PDFParser()
        excel_writer = ExcelWriter()
        
        # Validate input file
        if not pdf_parser.validate_pdf_file(input_file):
            print(f"Error: Invalid or unreadable PDF file: {input_file}")
            return False
        
        # Generate output filename if not provided
        if not output_file:
            input_path = Path(input_file)
            output_file = str(input_path.parent / f"{input_path.stem}.xlsx")
        
        print(f"Converting: {input_file}")
        print(f"Output: {output_file}")
        
        # Extract data from PDF
        print("Extracting data from PDF...")
        pdf_data = pdf_parser.extract_text_and_tables(input_file)
        
        print(f"Found {pdf_data.get('page_count', 0)} pages, "
              f"{len(pdf_data.get('tables', []))} tables")
        
        if pdf_data.get('has_thai_content'):
            print("Thai content detected - applying Thai font settings")
        
        # Create Excel file
        print("Creating Excel file...")
        success = excel_writer.create_workbook(pdf_data, output_file)
        
        if success:
            print(f"✓ Conversion completed successfully: {output_file}")
            return True
        else:
            print("✗ Failed to create Excel file")
            return False
            
    except Exception as e:
        print(f"Error during conversion: {str(e)}")
        return False


def convert_batch_cli(input_files: list, output_dir: str, create_summary: bool = True):
    """Convert multiple PDF files via command line interface."""
    try:
        # Initialize batch processor
        batch_processor = BatchProcessor()
        
        # Setup progress callback
        def progress_callback(progress_data):
            status = progress_data.get('status', 'unknown')
            if status == 'processing':
                completed = progress_data.get('completed_files', 0)
                total = progress_data.get('total_files', 0)
                current = progress_data.get('current_file', '')
                percent = progress_data.get('progress_percent', 0)
                print(f"Progress: {percent:.1f}% ({completed}/{total}) - {current}")
        
        batch_processor.add_progress_callback(progress_callback)
        
        print(f"Starting batch conversion of {len(input_files)} files...")
        print(f"Output directory: {output_dir}")
        
        # Process files
        results = batch_processor.process_multiple_files(
            input_files, output_dir, create_summary
        )
        
        # Show results
        print("\n" + "="*50)
        print("BATCH CONVERSION RESULTS")
        print("="*50)
        print(f"Total files: {results['total_files']}")
        print(f"Successful: {results['successful_files']}")
        print(f"Failed: {results['failed_files']}")
        print(f"Total time: {results['total_processing_time']:.2f} seconds")
        print(f"Average time per file: {results['average_time_per_file']:.2f} seconds")
        
        if results['failed_files'] > 0:
            print("\nFailed files:")
            for result in results['results']:
                if result['status'] != 'success':
                    print(f"  ✗ {result['file_name']}: {result['error_message']}")
        
        if 'summary_file' in results:
            print(f"\nBatch summary saved to: {results['summary_file']}")
        
        return results['failed_files'] == 0
        
    except Exception as e:
        print(f"Error during batch conversion: {str(e)}")
        return False


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description='PDF to Excel Converter (รองรับภาษาไทย)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                              # Launch GUI
  %(prog)s file.pdf                     # Convert single file
  %(prog)s file.pdf -o output.xlsx      # Convert with custom output name
  %(prog)s *.pdf -d output_folder       # Convert multiple files
  %(prog)s --batch folder/ -d output/   # Convert all PDFs in folder
        """
    )
    
    parser.add_argument('input_files', nargs='*', 
                       help='PDF file(s) to convert')
    parser.add_argument('-o', '--output', 
                       help='Output Excel file name (for single file)')
    parser.add_argument('-d', '--output-dir', 
                       help='Output directory (for multiple files)')
    parser.add_argument('--batch', 
                       help='Convert all PDF files in directory')
    parser.add_argument('--no-summary', action='store_true',
                       help='Don\'t create batch summary file')
    parser.add_argument('--log-level', default='INFO',
                       choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
                       help='Set logging level')
    parser.add_argument('--cli', action='store_true',
                       help='Force command line mode (no GUI)')
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.log_level)
    
    # Determine mode of operation
    if args.input_files or args.batch or args.cli:
        # Command line mode
        print("PDF to Excel Converter - Command Line Mode")
        print("="*50)
        
        if args.batch:
            # Batch mode - convert all PDFs in directory
            batch_processor = BatchProcessor()
            pdf_files = batch_processor.find_pdf_files(args.batch, recursive=True)
            
            if not pdf_files:
                print(f"No PDF files found in directory: {args.batch}")
                return 1
            
            output_dir = args.output_dir or f"{args.batch}/converted"
            success = convert_batch_cli(pdf_files, output_dir, not args.no_summary)
            
        elif len(args.input_files) == 1:
            # Single file mode
            input_file = args.input_files[0]
            output_file = args.output
            
            if args.output_dir:
                output_name = Path(input_file).stem + '.xlsx'
                output_file = str(Path(args.output_dir) / output_name)
            
            success = convert_single_file_cli(input_file, output_file)
            
        elif len(args.input_files) > 1:
            # Multiple files mode
            if not args.output_dir:
                print("Error: Output directory (-d) required for multiple files")
                return 1
            
            success = convert_batch_cli(args.input_files, args.output_dir, 
                                      not args.no_summary)
        else:
            parser.print_help()
            return 1
        
        return 0 if success else 1
        
    else:
        # GUI mode
        if not GUI_AVAILABLE:
            print("Error: GUI is not available in this environment.")
            print("Use --cli flag to run in command line mode.")
            print("Install tkinter if you need GUI functionality.")
            return 1
            
        try:
            print("Starting PDF to Excel Converter GUI...")
            app = MainWindow()
            app.run()
            return 0
        except Exception as e:
            print(f"Error starting GUI: {str(e)}")
            print("Try using --cli flag for command line mode")
            return 1


if __name__ == "__main__":
    sys.exit(main())