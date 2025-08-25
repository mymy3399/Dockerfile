"""
Main GUI window for PDF to Excel converter.
Provides user interface for file selection, processing, and batch operations.
"""

import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
from pathlib import Path
from typing import List, Optional, Dict, Any

from ..pdf_parser import PDFParser
from ..excel_writer import ExcelWriter
from ..batch_processor import BatchProcessor
from .progress_bar import ProgressWindow, SimpleProgressBar


class MainWindow:
    """Main application window for PDF to Excel converter."""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("PDF to Excel Converter (รองรับภาษาไทย)")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)
        
        # Initialize processors
        self.pdf_parser = PDFParser()
        self.excel_writer = ExcelWriter()
        self.batch_processor = BatchProcessor()
        
        # UI state
        self.selected_files = []
        self.output_directory = ""
        self.processing_thread = None
        
        # Setup UI
        self._setup_styles()
        self._setup_ui()
        self._setup_menu()
        
        # Center window
        self._center_window()
    
    def _setup_styles(self):
        """Configure UI styles for Thai language support."""
        style = ttk.Style()
        
        # Configure fonts for Thai support
        thai_font = ('TH Sarabun New', 12)
        thai_font_small = ('TH Sarabun New', 10)
        thai_font_large = ('TH Sarabun New', 14, 'bold')
        
        style.configure('Thai.TLabel', font=thai_font)
        style.configure('Thai.TButton', font=thai_font)
        style.configure('Thai.TFrame', font=thai_font)
        style.configure('Title.TLabel', font=thai_font_large)
        style.configure('Small.TLabel', font=thai_font_small)
    
    def _setup_ui(self):
        """Set up the main user interface."""
        # Main container
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, 
                               text="PDF to Excel Converter\n(โปรแกรมแปลง PDF เป็น Excel)", 
                               style='Title.TLabel',
                               anchor='center')
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # File selection section
        file_section = ttk.LabelFrame(main_frame, text="เลือกไฟล์ PDF (Select PDF Files)", 
                                     style='Thai.TFrame', padding="10")
        file_section.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        file_section.columnconfigure(1, weight=1)
        
        # Single file mode
        ttk.Label(file_section, text="ไฟล์เดียว:", style='Thai.TLabel').grid(row=0, column=0, sticky=tk.W)
        
        self.single_file_var = tk.StringVar()
        self.single_file_entry = ttk.Entry(file_section, textvariable=self.single_file_var,
                                          state='readonly', width=50)
        self.single_file_entry.grid(row=0, column=1, padx=(10, 10), sticky=(tk.W, tk.E))
        
        ttk.Button(file_section, text="เลือกไฟล์", style='Thai.TButton',
                  command=self._select_single_file).grid(row=0, column=2)
        
        ttk.Button(file_section, text="แปลงไฟล์เดียว", style='Thai.TButton',
                  command=self._convert_single_file).grid(row=0, column=3, padx=(5, 0))
        
        # Batch mode
        ttk.Label(file_section, text="หลายไฟล์:", style='Thai.TLabel').grid(row=1, column=0, 
                                                                        sticky=tk.W, pady=(10, 0))
        
        ttk.Button(file_section, text="เลือกหลายไฟล์", style='Thai.TButton',
                  command=self._select_multiple_files).grid(row=1, column=1, 
                                                           sticky=tk.W, pady=(10, 0))
        
        ttk.Button(file_section, text="เลือกจากโฟลเดอร์", style='Thai.TButton',
                  command=self._select_from_folder).grid(row=1, column=2, pady=(10, 0))
        
        ttk.Button(file_section, text="แปลงทั้งหมด", style='Thai.TButton',
                  command=self._convert_batch).grid(row=1, column=3, padx=(5, 0), pady=(10, 0))
        
        # Selected files display
        files_frame = ttk.Frame(file_section)
        files_frame.grid(row=2, column=0, columnspan=4, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        files_frame.columnconfigure(0, weight=1)
        
        ttk.Label(files_frame, text="ไฟล์ที่เลือก:", style='Thai.TLabel').grid(row=0, column=0, sticky=tk.W)
        
        # Files listbox with scrollbar
        listbox_frame = ttk.Frame(files_frame)
        listbox_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(5, 0))
        listbox_frame.columnconfigure(0, weight=1)
        listbox_frame.rowconfigure(0, weight=1)
        
        self.files_listbox = tk.Listbox(listbox_frame, height=6, font=('TH Sarabun New', 10))
        files_scrollbar = ttk.Scrollbar(listbox_frame, orient="vertical", command=self.files_listbox.yview)
        self.files_listbox.configure(yscrollcommand=files_scrollbar.set)
        
        self.files_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        files_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        ttk.Button(files_frame, text="ลบไฟล์ที่เลือก", style='Thai.TButton',
                  command=self._remove_selected_file).grid(row=2, column=0, sticky=tk.W, pady=(5, 0))
        
        ttk.Button(files_frame, text="ล้างรายการ", style='Thai.TButton',
                  command=self._clear_file_list).grid(row=2, column=1, sticky=tk.W, padx=(10, 0), pady=(5, 0))
        
        # Output settings section
        output_section = ttk.LabelFrame(main_frame, text="การตั้งค่าผลลัพธ์ (Output Settings)", 
                                       style='Thai.TFrame', padding="10")
        output_section.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        output_section.columnconfigure(1, weight=1)
        
        ttk.Label(output_section, text="โฟลเดอร์ผลลัพธ์:", style='Thai.TLabel').grid(row=0, column=0, sticky=tk.W)
        
        self.output_dir_var = tk.StringVar()
        self.output_dir_entry = ttk.Entry(output_section, textvariable=self.output_dir_var,
                                         state='readonly', width=50)
        self.output_dir_entry.grid(row=0, column=1, padx=(10, 10), sticky=(tk.W, tk.E))
        
        ttk.Button(output_section, text="เลือกโฟลเดอร์", style='Thai.TButton',
                  command=self._select_output_directory).grid(row=0, column=2)
        
        # Options
        self.create_summary_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(output_section, text="สร้างไฟล์สรุปผล (Create summary report)",
                       variable=self.create_summary_var, style='Thai.TButton').grid(row=1, column=0, 
                                                                                   columnspan=2, sticky=tk.W, pady=(10, 0))
        
        # Progress section
        progress_section = ttk.LabelFrame(main_frame, text="สถานะการประมวลผล (Processing Status)", 
                                         style='Thai.TFrame', padding="10")
        progress_section.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        progress_section.columnconfigure(0, weight=1)
        
        # Simple progress bar for single file operations
        self.simple_progress = SimpleProgressBar(progress_section, width=400)
        self.simple_progress.frame.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # Status and information section  
        info_section = ttk.LabelFrame(main_frame, text="ข้อมูลและความช่วยเหลือ (Information & Help)", 
                                     style='Thai.TFrame', padding="10")
        info_section.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))
        info_section.columnconfigure(0, weight=1)
        info_section.rowconfigure(0, weight=1)
        
        # Info text area
        info_text = tk.Text(info_section, height=8, wrap=tk.WORD, font=('TH Sarabun New', 10),
                           state='normal')
        info_scrollbar = ttk.Scrollbar(info_section, orient="vertical", command=info_text.yview)
        info_text.configure(yscrollcommand=info_scrollbar.set)
        
        info_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        info_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Add helpful information
        help_text = """วิธีการใช้งาน (How to use):
1. เลือกไฟล์ PDF ที่ต้องการแปลง (รองรับไฟล์เดียวหรือหลายไฟล์)
2. เลือกโฟลเดอร์สำหรับบันทึกไฟล์ Excel
3. กดปุ่ม \"แปลงไฟล์\" เพื่อเริ่มการแปลง

คุณสมบัติ (Features):
• รองรับภาษาไทย (TH Sarabun, Angsana, Cordia fonts)
• แปลงตารางและข้อความ
• ประมวลผลหลายไฟล์พร้อมกัน
• สร้างรายงานสรุปผล

หมายเหตุ (Notes):
• รองรับไฟล์ PDF แบบ Text-based เท่านั้น
• ไฟล์ที่เป็นรูปภาพอาจแปลงได้ไม่สมบูรณ์
• แนะนำให้ตรวจสอบผลลัพธ์ก่อนนำไปใช้งาน"""
        
        info_text.insert('1.0', help_text)
        info_text.config(state='disabled')
        
        # Configure grid weights for expandable sections
        main_frame.rowconfigure(4, weight=1)
        file_section.rowconfigure(2, weight=1)
    
    def _setup_menu(self):
        """Set up the application menu."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="ไฟล์ (File)", menu=file_menu)
        file_menu.add_command(label="เลือกไฟล์ PDF", command=self._select_single_file)
        file_menu.add_command(label="เลือกหลายไฟล์", command=self._select_multiple_files)
        file_menu.add_separator()
        file_menu.add_command(label="ออก (Exit)", command=self.root.quit)
        
        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="เครื่องมือ (Tools)", menu=tools_menu)
        tools_menu.add_command(label="ตรวจสอบไฟล์ PDF", command=self._validate_pdf_files)
        tools_menu.add_command(label="ทดสอบฟอนต์ภาษาไทย", command=self._test_thai_fonts)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="ช่วยเหลือ (Help)", menu=help_menu)
        help_menu.add_command(label="เกี่ยวกับ (About)", command=self._show_about)
    
    def _center_window(self):
        """Center the application window on screen."""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() - width) // 2
        y = (self.root.winfo_screenheight() - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    # File selection methods
    def _select_single_file(self):
        """Select a single PDF file."""
        file_path = filedialog.askopenfilename(
            title="เลือกไฟล์ PDF",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        if file_path:
            self.single_file_var.set(file_path)
            self.simple_progress.reset()
    
    def _select_multiple_files(self):
        """Select multiple PDF files."""
        file_paths = filedialog.askopenfilenames(
            title="เลือกไฟล์ PDF หลายไฟล์",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        if file_paths:
            self.selected_files.extend(file_paths)
            self._update_files_display()
    
    def _select_from_folder(self):
        """Select PDF files from a folder."""
        folder_path = filedialog.askdirectory(title="เลือกโฟลเดอร์ที่มีไฟล์ PDF")
        if folder_path:
            pdf_files = self.batch_processor.find_pdf_files(folder_path, recursive=True)
            if pdf_files:
                self.selected_files.extend(pdf_files)
                self._update_files_display()
                messagebox.showinfo("สำเร็จ", f"พบไฟล์ PDF จำนวน {len(pdf_files)} ไฟล์")
            else:
                messagebox.showwarning("แจ้งเตือน", "ไม่พบไฟล์ PDF ในโฟลเดอร์ที่เลือก")
    
    def _select_output_directory(self):
        """Select output directory."""
        dir_path = filedialog.askdirectory(title="เลือกโฟลเดอร์สำหรับบันทึกไฟล์ Excel")
        if dir_path:
            self.output_dir_var.set(dir_path)
            self.output_directory = dir_path
    
    def _update_files_display(self):
        """Update the files listbox display."""
        self.files_listbox.delete(0, tk.END)
        for file_path in self.selected_files:
            self.files_listbox.insert(tk.END, Path(file_path).name)
    
    def _remove_selected_file(self):
        """Remove selected file from the list."""
        selection = self.files_listbox.curselection()
        if selection:
            index = selection[0]
            del self.selected_files[index]
            self._update_files_display()
    
    def _clear_file_list(self):
        """Clear all files from the list."""
        self.selected_files.clear()
        self._update_files_display()
    
    # Processing methods
    def _convert_single_file(self):
        """Convert single PDF file."""
        file_path = self.single_file_var.get()
        if not file_path:
            messagebox.showwarning("แจ้งเตือน", "กรุณาเลือกไฟล์ PDF ก่อน")
            return
        
        if not self.output_directory:
            messagebox.showwarning("แจ้งเตือน", "กรุณาเลือกโฟลเดอร์ผลลัพธ์ก่อน")
            return
        
        # Start processing in separate thread
        self.processing_thread = threading.Thread(
            target=self._process_single_file_thread,
            args=(file_path,)
        )
        self.processing_thread.daemon = True
        self.processing_thread.start()
    
    def _process_single_file_thread(self, file_path: str):
        """Process single file in separate thread."""
        try:
            self.simple_progress.set_progress(10, "กำลังอ่านไฟล์ PDF...")
            
            # Extract data from PDF
            pdf_data = self.pdf_parser.extract_text_and_tables(file_path)
            
            self.simple_progress.set_progress(50, "กำลังสร้างไฟล์ Excel...")
            
            # Generate output filename
            output_name = Path(file_path).stem + '.xlsx'
            output_path = Path(self.output_directory) / output_name
            
            # Create Excel file
            success = self.excel_writer.create_workbook(pdf_data, str(output_path))
            
            if success:
                self.simple_progress.show_success(f"แปลงเสร็จสิ้น: {output_name}")
                messagebox.showinfo("สำเร็จ", f"แปลงไฟล์เสร็จสิ้น!\nบันทึกที่: {output_path}")
            else:
                self.simple_progress.show_error("ไม่สามารถสร้างไฟล์ Excel ได้")
                messagebox.showerror("ข้อผิดพลาด", "ไม่สามารถสร้างไฟล์ Excel ได้")
                
        except Exception as e:
            error_msg = f"เกิดข้อผิดพลาด: {str(e)}"
            self.simple_progress.show_error(error_msg)
            messagebox.showerror("ข้อผิดพลาด", error_msg)
    
    def _convert_batch(self):
        """Convert multiple files in batch mode."""
        if not self.selected_files:
            messagebox.showwarning("แจ้งเตือน", "กรุณาเลือกไฟล์ PDF ก่อน")
            return
        
        if not self.output_directory:
            messagebox.showwarning("แจ้งเตือน", "กรุณาเลือกโฟลเดอร์ผลลัพธ์ก่อน")
            return
        
        # Show progress window
        progress_window = ProgressWindow(self.root, "กำลังแปลงไฟล์ PDF")
        
        # Setup progress callback
        def progress_callback(progress_data):
            self.root.after(0, lambda: progress_window.update_progress(progress_data))
        
        self.batch_processor.add_progress_callback(progress_callback)
        
        # Start batch processing in separate thread
        def batch_thread():
            try:
                results = self.batch_processor.process_multiple_files(
                    self.selected_files,
                    self.output_directory,
                    self.create_summary_var.get()
                )
                
                # Show completion message
                successful = results['successful_files']
                failed = results['failed_files']
                total_time = results['total_processing_time']
                
                self.root.after(0, lambda: messagebox.showinfo(
                    "เสร็จสิ้น",
                    f"การแปลงเสร็จสิ้น!\n"
                    f"สำเร็จ: {successful} ไฟล์\n"
                    f"ล้มเหลว: {failed} ไฟล์\n"
                    f"เวลารวม: {total_time:.2f} วินาที"
                ))
                
            except Exception as e:
                self.root.after(0, lambda: progress_window.show_error(str(e)))
        
        thread = threading.Thread(target=batch_thread)
        thread.daemon = True
        thread.start()
    
    # Utility methods
    def _validate_pdf_files(self):
        """Validate selected PDF files."""
        if not self.selected_files and not self.single_file_var.get():
            messagebox.showwarning("แจ้งเตือน", "กรุณาเลือกไฟล์ก่อน")
            return
        
        files_to_check = self.selected_files.copy()
        if self.single_file_var.get():
            files_to_check.append(self.single_file_var.get())
        
        valid_files = []
        invalid_files = []
        
        for file_path in files_to_check:
            if self.pdf_parser.validate_pdf_file(file_path):
                valid_files.append(Path(file_path).name)
            else:
                invalid_files.append(Path(file_path).name)
        
        message = f"ไฟล์ที่ถูกต้อง: {len(valid_files)}\nไฟล์ที่ไม่ถูกต้อง: {len(invalid_files)}"
        if invalid_files:
            message += f"\n\nไฟล์ที่มีปัญหา:\n" + "\n".join(invalid_files[:5])
            if len(invalid_files) > 5:
                message += f"\n... และอีก {len(invalid_files) - 5} ไฟล์"
        
        messagebox.showinfo("ผลการตรวจสอบ", message)
    
    def _test_thai_fonts(self):
        """Test Thai font display."""
        test_window = tk.Toplevel(self.root)
        test_window.title("ทดสอบฟอนต์ภาษาไทย")
        test_window.geometry("400x300")
        
        test_text = "สวัสดีครับ นี่คือการทดสอบฟอนต์ภาษาไทย\nHello, this is Thai font test"
        
        fonts_to_test = ['TH Sarabun New', 'Angsana New', 'Cordia New', 'Tahoma', 'Arial']
        
        for i, font_name in enumerate(fonts_to_test):
            ttk.Label(test_window, text=f"{font_name}:", font=(font_name, 10, 'bold')).pack(anchor='w', padx=10)
            ttk.Label(test_window, text=test_text, font=(font_name, 12)).pack(anchor='w', padx=20, pady=(0, 10))
    
    def _show_about(self):
        """Show about dialog."""
        about_text = """PDF to Excel Converter v1.0

โปรแกรมแปลงไฟล์ PDF เป็น Excel 
รองรับภาษาไทยอย่างสมบูรณ์

คุณสมบัติ:
• รองรับฟอนต์ภาษาไทย
• แปลงตารางและข้อความ
• ประมวลผลหลายไฟล์
• สร้างรายงานสรุปผล

พัฒนาโดย: PDF to Excel Converter Team
"""
        messagebox.showinfo("เกี่ยวกับโปรแกรม", about_text)
    
    def run(self):
        """Start the application."""
        self.root.mainloop()


def main():
    """Main function to run the application."""
    app = MainWindow()
    app.run()


if __name__ == "__main__":
    main()