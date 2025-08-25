"""
Progress Bar component for the PDF to Excel converter GUI.
Shows processing progress and status updates.
"""

import tkinter as tk
from tkinter import ttk
import threading
import time
from typing import Dict, Any, Optional


class ProgressWindow:
    """Progress window for showing batch processing progress."""
    
    def __init__(self, parent: tk.Tk, title: str = "Processing PDF Files"):
        self.parent = parent
        self.window = tk.Toplevel(parent)
        self.window.title(title)
        self.window.geometry("500x300")
        self.window.resizable(False, False)
        
        # Make window modal
        self.window.transient(parent)
        self.window.grab_set()
        
        # Center window
        self.window.geometry("+{}+{}".format(
            parent.winfo_rootx() + 50,
            parent.winfo_rooty() + 50
        ))
        
        self.is_cancelled = False
        self.is_completed = False
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Set up the progress window UI."""
        # Main frame
        main_frame = ttk.Frame(self.window, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Status label
        self.status_label = ttk.Label(main_frame, text="Initializing...", 
                                     font=('TH Sarabun New', 12))
        self.status_label.grid(row=0, column=0, columnspan=2, pady=(0, 10), sticky=tk.W)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(main_frame, variable=self.progress_var, 
                                          maximum=100, length=400)
        self.progress_bar.grid(row=1, column=0, columnspan=2, pady=(0, 10), sticky=(tk.W, tk.E))
        
        # Progress percentage label
        self.percent_label = ttk.Label(main_frame, text="0%", 
                                      font=('TH Sarabun New', 10))
        self.percent_label.grid(row=2, column=0, sticky=tk.W)
        
        # File count label
        self.file_count_label = ttk.Label(main_frame, text="0 / 0 files", 
                                         font=('TH Sarabun New', 10))
        self.file_count_label.grid(row=2, column=1, sticky=tk.E)
        
        # Current file label
        self.current_file_label = ttk.Label(main_frame, text="", 
                                           font=('TH Sarabun New', 10), 
                                           foreground="blue")
        self.current_file_label.grid(row=3, column=0, columnspan=2, pady=(10, 0), sticky=tk.W)
        
        # Details text area with scrollbar
        details_frame = ttk.Frame(main_frame)
        details_frame.grid(row=4, column=0, columnspan=2, pady=(10, 0), sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.details_text = tk.Text(details_frame, height=8, width=60, 
                                   font=('TH Sarabun New', 9))
        scrollbar = ttk.Scrollbar(details_frame, orient="vertical", command=self.details_text.yview)
        self.details_text.configure(yscrollcommand=scrollbar.set)
        
        self.details_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        details_frame.columnconfigure(0, weight=1)
        details_frame.rowconfigure(0, weight=1)
        
        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=(10, 0))
        
        # Cancel button
        self.cancel_button = ttk.Button(button_frame, text="ยกเลิก (Cancel)", 
                                       command=self._on_cancel)
        self.cancel_button.grid(row=0, column=0, padx=(0, 10))
        
        # Close button (initially hidden)
        self.close_button = ttk.Button(button_frame, text="ปิด (Close)", 
                                      command=self._on_close)
        self.close_button.grid(row=0, column=1)
        self.close_button.grid_remove()  # Hide initially
        
        # Configure grid weights
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(4, weight=1)
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        
        # Handle window closing
        self.window.protocol("WM_DELETE_WINDOW", self._on_window_close)
    
    def update_progress(self, progress_data: Dict[str, Any]):
        """
        Update progress display with new data.
        
        Args:
            progress_data (Dict): Progress information
        """
        if self.is_cancelled:
            return
        
        # Update progress bar
        progress_percent = progress_data.get('progress_percent', 0)
        self.progress_var.set(progress_percent)
        self.percent_label.config(text=f"{progress_percent:.1f}%")
        
        # Update file count
        completed = progress_data.get('completed_files', 0)
        total = progress_data.get('total_files', 0)
        self.file_count_label.config(text=f"{completed} / {total} files")
        
        # Update status
        status = progress_data.get('status', '')
        if status == 'started':
            self.status_label.config(text="เริ่มการประมวลผล... (Starting processing...)")
        elif status == 'processing':
            current_file = progress_data.get('current_file', '')
            if current_file:
                self.status_label.config(text=f"กำลังประมวลผล... (Processing...)")
                self.current_file_label.config(text=f"Current: {current_file}")
        elif status == 'completed':
            self.status_label.config(text="การประมวลผลเสร็จสิ้น! (Processing completed!)")
            self.current_file_label.config(text="")
            self.is_completed = True
            self._show_completion_ui()
        
        # Add details
        if progress_data.get('last_result'):
            self._add_detail(progress_data['last_result'])
        
        # Update window
        self.window.update_idletasks()
    
    def _add_detail(self, result: Dict[str, Any]):
        """Add processing result to details text."""
        file_name = result.get('file_name', 'Unknown')
        status = result.get('status', 'Unknown')
        processing_time = result.get('processing_time', 0)
        
        # Format status message
        if status == 'success':
            status_text = "สำเร็จ ✓"
            page_count = result.get('page_count', 0)
            table_count = result.get('table_count', 0)
            thai_content = "มี" if result.get('has_thai_content', False) else "ไม่มี"
            detail_msg = f"หน้า: {page_count}, ตาราง: {table_count}, ภาษาไทย: {thai_content}"
        else:
            status_text = "ล้มเหลว ✗"
            error_msg = result.get('error_message', 'Unknown error')
            detail_msg = f"ข้อผิดพลาด: {error_msg}"
        
        # Add to text widget
        log_entry = f"[{time.strftime('%H:%M:%S')}] {file_name} - {status_text}\n"
        log_entry += f"  เวลา: {processing_time:.2f}s, {detail_msg}\n\n"
        
        self.details_text.insert(tk.END, log_entry)
        self.details_text.see(tk.END)  # Scroll to bottom
    
    def _show_completion_ui(self):
        """Show completion UI elements."""
        self.cancel_button.grid_remove()
        self.close_button.grid()
        
        # Change progress bar color to green (if supported)
        try:
            style = ttk.Style()
            style.configure("Completed.Horizontal.TProgressbar", 
                          foreground='green', background='green')
            self.progress_bar.configure(style="Completed.Horizontal.TProgressbar")
        except:
            pass  # Ignore if style change fails
    
    def _on_cancel(self):
        """Handle cancel button click."""
        self.is_cancelled = True
        self.status_label.config(text="กำลังยกเลิก... (Cancelling...)")
        self.cancel_button.config(state='disabled')
    
    def _on_close(self):
        """Handle close button click."""
        self.window.destroy()
    
    def _on_window_close(self):
        """Handle window close event."""
        if not self.is_completed:
            self._on_cancel()
        else:
            self._on_close()
    
    def show_error(self, error_message: str):
        """Show error message in the progress window."""
        self.status_label.config(text="เกิดข้อผิดพลาด! (Error occurred!)")
        self.details_text.insert(tk.END, f"\nERROR: {error_message}\n")
        self.details_text.see(tk.END)
        self._show_completion_ui()


class SimpleProgressBar:
    """Simple progress bar for single file operations."""
    
    def __init__(self, parent: tk.Widget, width: int = 300):
        self.frame = ttk.Frame(parent)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self.frame, variable=self.progress_var,
                                          maximum=100, length=width)
        self.progress_bar.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # Status label
        self.status_label = ttk.Label(self.frame, text="Ready", 
                                     font=('TH Sarabun New', 10))
        self.status_label.grid(row=1, column=0, pady=(5, 0))
        
        self.frame.columnconfigure(0, weight=1)
    
    def set_progress(self, percent: float, status: str = ""):
        """Set progress percentage and status text."""
        self.progress_var.set(percent)
        if status:
            self.status_label.config(text=status)
    
    def reset(self):
        """Reset progress bar to initial state."""
        self.progress_var.set(0)
        self.status_label.config(text="Ready")
    
    def show_error(self, error_message: str):
        """Show error status."""
        self.status_label.config(text=f"Error: {error_message}", foreground='red')
    
    def show_success(self, message: str = "Completed successfully"):
        """Show success status."""
        self.progress_var.set(100)
        self.status_label.config(text=message, foreground='green')


def main():
    """Test function for progress components."""
    root = tk.Tk()
    root.title("Progress Test")
    root.geometry("400x200")
    
    # Test simple progress bar
    simple_progress = SimpleProgressBar(root)
    simple_progress.frame.pack(pady=20, padx=20, fill=tk.X)
    
    def test_progress():
        for i in range(0, 101, 10):
            simple_progress.set_progress(i, f"Processing... {i}%")
            root.update()
            time.sleep(0.1)
        simple_progress.show_success("Test completed!")
    
    test_button = ttk.Button(root, text="Test Progress", command=test_progress)
    test_button.pack(pady=10)
    
    # Test progress window
    def test_progress_window():
        progress_win = ProgressWindow(root, "Test Progress Window")
        
        def simulate_progress():
            for i in range(0, 101, 20):
                progress_data = {
                    'progress_percent': i,
                    'completed_files': i // 20,
                    'total_files': 5,
                    'status': 'processing',
                    'current_file': f'test_file_{i//20}.pdf'
                }
                progress_win.update_progress(progress_data)
                time.sleep(0.5)
            
            # Completion
            progress_win.update_progress({
                'progress_percent': 100,
                'completed_files': 5,
                'total_files': 5,
                'status': 'completed'
            })
        
        # Start simulation in thread
        thread = threading.Thread(target=simulate_progress)
        thread.daemon = True
        thread.start()
    
    window_test_button = ttk.Button(root, text="Test Progress Window", 
                                   command=test_progress_window)
    window_test_button.pack(pady=5)
    
    print("Progress components test initialized")
    root.mainloop()


if __name__ == "__main__":
    main()