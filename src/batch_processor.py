"""
Batch Processor module for handling multiple PDF files.
Provides progress tracking and summary reporting.
"""

import os
import time
import logging
import threading
from typing import List, Dict, Any, Callable, Optional
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

from .pdf_parser import PDFParser
from .excel_writer import ExcelWriter


class BatchProcessor:
    """Batch processor for converting multiple PDF files to Excel."""
    
    def __init__(self, max_workers: int = 4):
        self.logger = logging.getLogger(__name__)
        self.pdf_parser = PDFParser()
        self.excel_writer = ExcelWriter()
        self.max_workers = max_workers
        
        # Progress tracking
        self.total_files = 0
        self.completed_files = 0
        self.failed_files = 0
        self.progress_callbacks = []
        
    def add_progress_callback(self, callback: Callable[[Dict[str, Any]], None]):
        """
        Add callback function for progress updates.
        
        Args:
            callback: Function that receives progress dict
        """
        self.progress_callbacks.append(callback)
    
    def _notify_progress(self, progress_data: Dict[str, Any]):
        """Notify all registered progress callbacks."""
        for callback in self.progress_callbacks:
            try:
                callback(progress_data)
            except Exception as e:
                self.logger.error(f"Error in progress callback: {str(e)}")
    
    def process_multiple_files(self, 
                             file_list: List[str], 
                             output_dir: str,
                             create_summary: bool = True) -> Dict[str, Any]:
        """
        Process multiple PDF files and convert to Excel.
        
        Args:
            file_list (List[str]): List of PDF file paths
            output_dir (str): Output directory for Excel files
            create_summary (bool): Whether to create batch summary file
            
        Returns:
            Dict: Processing results summary
        """
        start_time = time.time()
        
        # Initialize progress tracking
        self.total_files = len(file_list)
        self.completed_files = 0
        self.failed_files = 0
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        results = []
        
        self.logger.info(f"Starting batch processing of {self.total_files} files")
        
        # Initial progress notification
        self._notify_progress({
            'status': 'started',
            'total_files': self.total_files,
            'completed_files': 0,
            'current_file': None,
            'progress_percent': 0.0
        })
        
        # Process files using thread pool
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all jobs
            future_to_file = {
                executor.submit(self._process_single_file, file_path, output_dir): file_path
                for file_path in file_list
            }
            
            # Collect results as they complete
            for future in as_completed(future_to_file):
                file_path = future_to_file[future]
                
                try:
                    result = future.result()
                    results.append(result)
                    
                    if result['status'] == 'success':
                        self.completed_files += 1
                    else:
                        self.failed_files += 1
                        
                except Exception as e:
                    self.logger.error(f"Unexpected error processing {file_path}: {str(e)}")
                    results.append({
                        'file_path': file_path,
                        'file_name': Path(file_path).name,
                        'status': 'error',
                        'error_message': str(e),
                        'processing_time': 0,
                        'page_count': 0,
                        'table_count': 0,
                        'has_thai_content': False,
                        'output_file': None
                    })
                    self.failed_files += 1
                
                # Progress notification
                progress_percent = (self.completed_files + self.failed_files) / self.total_files * 100
                self._notify_progress({
                    'status': 'processing',
                    'total_files': self.total_files,
                    'completed_files': self.completed_files + self.failed_files,
                    'current_file': Path(file_path).name,
                    'progress_percent': progress_percent,
                    'last_result': result if 'result' in locals() else None
                })
        
        # Calculate summary statistics
        total_time = time.time() - start_time
        
        summary = {
            'total_files': self.total_files,
            'successful_files': self.completed_files,
            'failed_files': self.failed_files,
            'total_processing_time': total_time,
            'average_time_per_file': total_time / self.total_files if self.total_files > 0 else 0,
            'results': results,
            'output_directory': str(output_path)
        }
        
        # Create batch summary Excel file
        if create_summary:
            summary_path = output_path / f"batch_summary_{int(time.time())}.xlsx"
            success = self.excel_writer.create_batch_summary(results, str(summary_path))
            if success:
                summary['summary_file'] = str(summary_path)
        
        # Final progress notification
        self._notify_progress({
            'status': 'completed',
            'total_files': self.total_files,
            'completed_files': self.completed_files,
            'failed_files': self.failed_files,
            'progress_percent': 100.0,
            'summary': summary
        })
        
        self.logger.info(f"Batch processing completed. Success: {self.completed_files}, "
                        f"Failed: {self.failed_files}, Total time: {total_time:.2f}s")
        
        return summary
    
    def _process_single_file(self, file_path: str, output_dir: str) -> Dict[str, Any]:
        """
        Process a single PDF file.
        
        Args:
            file_path (str): Path to PDF file
            output_dir (str): Output directory
            
        Returns:
            Dict: Processing result
        """
        file_start_time = time.time()
        file_name = Path(file_path).name
        
        result = {
            'file_path': file_path,
            'file_name': file_name,
            'status': 'processing',
            'processing_time': 0,
            'page_count': 0,
            'table_count': 0,
            'has_thai_content': False,
            'output_file': None,
            'error_message': None
        }
        
        try:
            self.logger.debug(f"Processing file: {file_name}")
            
            # Validate PDF file
            if not self.pdf_parser.validate_pdf_file(file_path):
                result.update({
                    'status': 'error',
                    'error_message': 'Invalid or unreadable PDF file',
                    'processing_time': time.time() - file_start_time
                })
                return result
            
            # Extract data from PDF
            pdf_data = self.pdf_parser.extract_text_and_tables(file_path)
            
            result.update({
                'page_count': pdf_data.get('page_count', 0),
                'table_count': len(pdf_data.get('tables', [])),
                'has_thai_content': pdf_data.get('has_thai_content', False)
            })
            
            # Generate output file path
            output_name = Path(file_name).stem + '.xlsx'
            output_file_path = Path(output_dir) / output_name
            
            # Create Excel file
            success = self.excel_writer.create_workbook(pdf_data, str(output_file_path))
            
            if success:
                result.update({
                    'status': 'success',
                    'output_file': str(output_file_path)
                })
                self.logger.debug(f"Successfully processed: {file_name}")
            else:
                result.update({
                    'status': 'error',
                    'error_message': 'Failed to create Excel file'
                })
                self.logger.error(f"Failed to create Excel for: {file_name}")
            
        except Exception as e:
            error_msg = str(e)
            self.logger.error(f"Error processing {file_name}: {error_msg}")
            result.update({
                'status': 'error',
                'error_message': error_msg
            })
        
        finally:
            result['processing_time'] = time.time() - file_start_time
        
        return result
    
    def find_pdf_files(self, directory: str, recursive: bool = True) -> List[str]:
        """
        Find all PDF files in a directory.
        
        Args:
            directory (str): Directory to search
            recursive (bool): Whether to search subdirectories
            
        Returns:
            List[str]: List of PDF file paths
        """
        pdf_files = []
        directory_path = Path(directory)
        
        if not directory_path.exists() or not directory_path.is_dir():
            self.logger.error(f"Directory does not exist: {directory}")
            return pdf_files
        
        try:
            if recursive:
                pattern = "**/*.pdf"
            else:
                pattern = "*.pdf"
            
            pdf_files = [str(p) for p in directory_path.glob(pattern) if p.is_file()]
            
            self.logger.info(f"Found {len(pdf_files)} PDF files in {directory}")
            
        except Exception as e:
            self.logger.error(f"Error searching for PDF files: {str(e)}")
        
        return sorted(pdf_files)  # Sort for consistent ordering
    
    def estimate_processing_time(self, file_list: List[str]) -> Dict[str, float]:
        """
        Estimate processing time for a list of files.
        
        Args:
            file_list (List[str]): List of PDF file paths
            
        Returns:
            Dict: Estimated times
        """
        # Base estimates (rough approximations)
        base_time_per_page = 0.5  # seconds
        base_time_per_file = 2.0  # seconds overhead
        
        total_estimated_time = 0
        file_estimates = []
        
        for file_path in file_list:
            try:
                # Quick page count estimate (without full processing)
                with open(file_path, 'rb') as f:
                    # Very rough page count estimation
                    content = f.read(1024)  # Read first 1KB
                    # This is a very rough estimate
                    estimated_pages = max(1, content.count(b'/Type/Page') or 1)
                
                file_time = base_time_per_file + (estimated_pages * base_time_per_page)
                file_estimates.append(file_time)
                total_estimated_time += file_time
                
            except Exception:
                # Fallback estimate
                file_estimates.append(base_time_per_file + base_time_per_page)
                total_estimated_time += base_time_per_file + base_time_per_page
        
        return {
            'total_estimated_time': total_estimated_time,
            'average_estimated_time': total_estimated_time / len(file_list) if file_list else 0,
            'file_estimates': file_estimates
        }
    
    def get_processing_stats(self) -> Dict[str, Any]:
        """
        Get current processing statistics.
        
        Returns:
            Dict: Current processing stats
        """
        return {
            'total_files': self.total_files,
            'completed_files': self.completed_files,
            'failed_files': self.failed_files,
            'remaining_files': self.total_files - self.completed_files - self.failed_files,
            'success_rate': (self.completed_files / self.total_files * 100) if self.total_files > 0 else 0,
            'completion_rate': ((self.completed_files + self.failed_files) / self.total_files * 100) if self.total_files > 0 else 0
        }


def main():
    """Test function for batch processor."""
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    
    processor = BatchProcessor()
    
    # Example progress callback
    def progress_callback(progress_data):
        print(f"Progress: {progress_data.get('progress_percent', 0):.1f}% - "
              f"Status: {progress_data.get('status', 'unknown')}")
        if progress_data.get('current_file'):
            print(f"Processing: {progress_data['current_file']}")
    
    processor.add_progress_callback(progress_callback)
    
    # Test file discovery
    test_dir = "/tmp"  # Example directory
    pdf_files = processor.find_pdf_files(test_dir, recursive=False)
    print(f"Found {len(pdf_files)} PDF files for testing")
    
    # Test time estimation
    if pdf_files:
        estimates = processor.estimate_processing_time(pdf_files)
        print(f"Estimated processing time: {estimates['total_estimated_time']:.2f} seconds")
    
    print("Batch Processor initialized successfully")


if __name__ == "__main__":
    main()