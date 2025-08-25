"""
Excel Writer module for creating Excel files from PDF data.
Handles Thai text formatting and table structure preservation.
"""

import logging
from typing import List, Dict, Any, Optional
from pathlib import Path

import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.utils import get_column_letter

from .thai_handler import ThaiTextHandler


class ExcelWriter:
    """Excel writer class for creating Excel files with Thai language support."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.thai_handler = ThaiTextHandler()
        
        # Default styling
        self.header_font = Font(name='TH Sarabun New', size=14, bold=True)
        self.data_font = Font(name='TH Sarabun New', size=12)
        self.header_fill = PatternFill(start_color='E6E6FA', end_color='E6E6FA', fill_type='solid')
        self.border = Border(
            left=Side(style='thin'),
            right=Side(style='thin'),
            top=Side(style='thin'),
            bottom=Side(style='thin')
        )
    
    def create_workbook(self, data: Dict[str, Any], output_path: str) -> bool:
        """
        Create Excel workbook from PDF extracted data.
        
        Args:
            data (Dict): Extracted PDF data
            output_path (str): Output Excel file path
            
        Returns:
            bool: True if successful
        """
        try:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            workbook = Workbook()
            
            # Remove default worksheet
            workbook.remove(workbook.active)
            
            # Create summary worksheet
            self._create_summary_sheet(workbook, data)
            
            # Create worksheets for tables
            if data.get('tables'):
                self._create_table_sheets(workbook, data['tables'])
            
            # Create text content worksheet
            if data.get('text_content'):
                self._create_text_sheet(workbook, data)
            
            # Save workbook
            workbook.save(output_path)
            self.logger.info(f"Excel file created successfully: {output_path}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error creating Excel workbook: {str(e)}")
            return False
    
    def _create_summary_sheet(self, workbook: Workbook, data: Dict[str, Any]):
        """Create summary worksheet with PDF information."""
        ws = workbook.create_sheet("Summary", 0)
        
        # Summary data
        summary_info = [
            ['PDF File Information', ''],
            ['File Path', data.get('file_path', 'Unknown')],
            ['Total Pages', data.get('page_count', 0)],
            ['Total Tables', len(data.get('tables', []))],
            ['Thai Content Detected', 'Yes' if data.get('has_thai_content', False) else 'No'],
            ['Extraction Date', pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')],
            ['', ''],
            ['Page Details', '']
        ]
        
        # Add page details
        for page in data.get('pages', []):
            summary_info.append([
                f"Page {page['page_number']}", 
                f"Tables: {page['table_count']}, Thai: {'Yes' if page['has_thai'] else 'No'}"
            ])
        
        # Write data
        for row_idx, (key, value) in enumerate(summary_info, 1):
            ws[f'A{row_idx}'] = key
            ws[f'B{row_idx}'] = value
            
            # Apply formatting
            if row_idx == 1 or row_idx == 8:  # Headers
                ws[f'A{row_idx}'].font = self.header_font
                ws[f'A{row_idx}'].fill = self.header_fill
                ws[f'B{row_idx}'].font = self.header_font
                ws[f'B{row_idx}'].fill = self.header_fill
            else:
                ws[f'A{row_idx}'].font = self.data_font
                ws[f'B{row_idx}'].font = self.data_font
        
        # Auto-adjust column widths
        ws.column_dimensions['A'].width = 20
        ws.column_dimensions['B'].width = 50
        
        # Apply Thai fonts where needed
        self.thai_handler.set_thai_fonts(ws)
    
    def _create_table_sheets(self, workbook: Workbook, tables: List[Dict]):
        """Create separate worksheets for each table."""
        for table in tables:
            try:
                sheet_name = f"Table_P{table['page']}_T{table['table_index']}"
                ws = workbook.create_sheet(sheet_name)
                
                # Convert table data to DataFrame
                df = self._table_to_dataframe(table)
                
                if df.empty:
                    continue
                
                # Write data to worksheet
                for r_idx, row in enumerate(dataframe_to_rows(df, index=False, header=True), 1):
                    for c_idx, value in enumerate(row, 1):
                        cell = ws.cell(row=r_idx, column=c_idx, value=value)
                        
                        # Apply formatting
                        if r_idx == 1:  # Header row
                            cell.font = self.header_font
                            cell.fill = self.header_fill
                            cell.alignment = Alignment(horizontal='center', vertical='center')
                        else:
                            cell.font = self.data_font
                        
                        cell.border = self.border
                
                # Auto-adjust column widths
                self._adjust_column_widths(ws)
                
                # Apply Thai fonts
                self.thai_handler.set_thai_fonts(ws)
                
                self.logger.debug(f"Created sheet: {sheet_name} with {df.shape[0]} rows")
                
            except Exception as e:
                self.logger.warning(f"Error creating table sheet: {str(e)}")
    
    def _create_text_sheet(self, workbook: Workbook, data: Dict[str, Any]):
        """Create worksheet with text content from PDF."""
        ws = workbook.create_sheet("Text_Content")
        
        # Add header
        ws['A1'] = 'Page'
        ws['B1'] = 'Text Content'
        ws['A1'].font = self.header_font
        ws['B1'].font = self.header_font
        ws['A1'].fill = self.header_fill
        ws['B1'].fill = self.header_fill
        
        # Add text content by page
        row_idx = 2
        for page in data.get('pages', []):
            if page.get('text', '').strip():
                ws[f'A{row_idx}'] = page['page_number']
                ws[f'B{row_idx}'] = page['text']
                
                ws[f'A{row_idx}'].font = self.data_font
                ws[f'B{row_idx}'].font = self.data_font
                
                # Set row height for text content
                ws.row_dimensions[row_idx].height = max(50, len(page['text']) // 10)
                
                row_idx += 1
        
        # Set column widths
        ws.column_dimensions['A'].width = 10
        ws.column_dimensions['B'].width = 80
        
        # Apply Thai fonts
        self.thai_handler.set_thai_fonts(ws)
    
    def _table_to_dataframe(self, table: Dict) -> pd.DataFrame:
        """Convert table data to pandas DataFrame."""
        try:
            data = table.get('data', [])
            if not data:
                return pd.DataFrame()
            
            # Use first row as headers if it looks like headers
            headers = data[0] if data else []
            rows = data[1:] if len(data) > 1 else []
            
            # Clean headers
            clean_headers = []
            for i, header in enumerate(headers):
                header_str = str(header).strip() if header else f"Column_{i+1}"
                # Normalize Thai text in headers
                header_str = self.thai_handler.normalize_thai_text(header_str)
                clean_headers.append(header_str)
            
            # Clean row data
            clean_rows = []
            for row in rows:
                clean_row = []
                for cell in row:
                    cell_str = str(cell).strip() if cell else ""
                    # Normalize Thai text in cells
                    cell_str = self.thai_handler.normalize_thai_text(cell_str)
                    clean_row.append(cell_str)
                clean_rows.append(clean_row)
            
            # Create DataFrame
            df = pd.DataFrame(clean_rows, columns=clean_headers)
            
            return df
            
        except Exception as e:
            self.logger.error(f"Error converting table to DataFrame: {str(e)}")
            return pd.DataFrame()
    
    def _adjust_column_widths(self, worksheet):
        """Auto-adjust column widths based on content."""
        try:
            for column in worksheet.columns:
                max_length = 0
                column_letter = get_column_letter(column[0].column)
                
                for cell in column:
                    if cell.value:
                        # Calculate length considering Thai characters
                        cell_value = str(cell.value)
                        # Thai characters typically need more space
                        thai_ratio = self.thai_handler.get_thai_content_ratio(cell_value)
                        length_multiplier = 1.5 if thai_ratio > 0.3 else 1.0
                        cell_length = len(cell_value) * length_multiplier
                        max_length = max(max_length, cell_length)
                
                # Set column width (with limits)
                adjusted_width = min(max(max_length + 2, 10), 50)
                worksheet.column_dimensions[column_letter].width = adjusted_width
                
        except Exception as e:
            self.logger.warning(f"Error adjusting column widths: {str(e)}")
    
    def create_batch_summary(self, results: List[Dict[str, Any]], output_path: str) -> bool:
        """
        Create summary Excel file for batch processing results.
        
        Args:
            results (List): List of processing results
            output_path (str): Output Excel file path
            
        Returns:
            bool: True if successful
        """
        try:
            workbook = Workbook()
            ws = workbook.active
            ws.title = "Batch_Processing_Summary"
            
            # Headers
            headers = [
                'File Name', 'Status', 'Pages', 'Tables', 'Thai Content',
                'Processing Time (s)', 'Output File', 'Error Message'
            ]
            
            for col, header in enumerate(headers, 1):
                cell = ws.cell(row=1, column=col, value=header)
                cell.font = self.header_font
                cell.fill = self.header_fill
                cell.border = self.border
            
            # Data rows
            for row_idx, result in enumerate(results, 2):
                data_row = [
                    result.get('file_name', ''),
                    result.get('status', ''),
                    result.get('page_count', 0),
                    result.get('table_count', 0),
                    'Yes' if result.get('has_thai_content', False) else 'No',
                    result.get('processing_time', 0),
                    result.get('output_file', ''),
                    result.get('error_message', '')
                ]
                
                for col, value in enumerate(data_row, 1):
                    cell = ws.cell(row=row_idx, column=col, value=value)
                    cell.font = self.data_font
                    cell.border = self.border
            
            # Auto-adjust columns
            for col in range(1, len(headers) + 1):
                column_letter = get_column_letter(col)
                ws.column_dimensions[column_letter].width = 15
            
            # Apply Thai fonts
            self.thai_handler.set_thai_fonts(ws)
            
            # Save workbook
            workbook.save(output_path)
            self.logger.info(f"Batch summary created: {output_path}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error creating batch summary: {str(e)}")
            return False
    
    def validate_excel_output(self, file_path: str) -> bool:
        """
        Validate that Excel file was created successfully and can be opened.
        
        Args:
            file_path (str): Path to Excel file
            
        Returns:
            bool: True if valid Excel file
        """
        try:
            from openpyxl import load_workbook
            
            if not Path(file_path).exists():
                return False
            
            # Try to load the workbook
            wb = load_workbook(file_path)
            return len(wb.sheetnames) > 0
            
        except Exception as e:
            self.logger.error(f"Excel validation failed: {str(e)}")
            return False


def main():
    """Test function for Excel writer."""
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    
    writer = ExcelWriter()
    
    # Test data
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
                ]
            }
        ],
        'pages': [
            {'page_number': 1, 'text': 'สวัสดีครับ Hello', 'table_count': 1, 'has_thai': True},
            {'page_number': 2, 'text': 'Page 2 content', 'table_count': 0, 'has_thai': False}
        ]
    }
    
    # Test Excel creation
    success = writer.create_workbook(test_data, 'test_output.xlsx')
    print(f"Excel creation test: {'Success' if success else 'Failed'}")
    
    print("Excel Writer initialized successfully")


if __name__ == "__main__":
    main()