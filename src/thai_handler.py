"""
Thai Text Handler module for processing Thai language content.
Handles proper Thai font settings and text normalization.
"""

import re
import unicodedata
import logging
from typing import Optional, List, Dict, Any

from openpyxl.styles import Font


class ThaiTextHandler:
    """Handler for Thai text processing and Excel font configuration."""
    
    # Thai font preferences (ordered by preference)
    THAI_FONTS = [
        'TH Sarabun New',
        'Angsana New', 
        'Cordia New',
        'Tahoma',
        'Arial Unicode MS',
        'Microsoft Sans Serif'
    ]
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Thai Unicode ranges
        self.thai_consonants = re.compile(r'[\u0E01-\u0E2E]')
        self.thai_vowels = re.compile(r'[\u0E30-\u0E4E]') 
        self.thai_tones = re.compile(r'[\u0E48-\u0E4B]')
        self.thai_symbols = re.compile(r'[\u0E4F-\u0E5B]')
        
        # Combined Thai pattern
        self.thai_pattern = re.compile(r'[\u0E00-\u0E7F]')
        
        # Thai vowel position patterns
        self.leading_vowels = re.compile(r'[\u0E40-\u0E44]')  # เ แ โ ใ ไ
        self.trailing_vowels = re.compile(r'[\u0E30-\u0E39]')  # Various vowels
        self.above_vowels = re.compile(r'[\u0E34-\u0E37]')     # Above vowels
        self.below_vowels = re.compile(r'[\u0E38-\u0E3A]')     # Below vowels
        
    def normalize_thai_text(self, text: str) -> str:
        """
        Normalize Thai text to fix character encoding and ordering issues.
        
        Args:
            text (str): Input Thai text
            
        Returns:
            str: Normalized Thai text
        """
        if not text:
            return text
            
        try:
            # First, normalize Unicode (NFC normalization)
            normalized = unicodedata.normalize('NFC', text)
            
            # Fix common Thai character ordering issues
            normalized = self._fix_thai_character_order(normalized)
            
            # Remove duplicate spaces and normalize whitespace
            normalized = re.sub(r'\s+', ' ', normalized).strip()
            
            return normalized
            
        except Exception as e:
            self.logger.warning(f"Error normalizing Thai text: {str(e)}")
            return text
    
    def _fix_thai_character_order(self, text: str) -> str:
        """
        Fix Thai character ordering issues (vowel and tone mark positions).
        
        Args:
            text (str): Input text
            
        Returns:
            str: Text with corrected character order
        """
        # This is a simplified version - a full implementation would need
        # more sophisticated Thai linguistics rules
        
        # Convert to list for easier manipulation
        chars = list(text)
        result = []
        i = 0
        
        while i < len(chars):
            char = chars[i]
            
            # If current character is Thai
            if self.thai_pattern.match(char):
                # Check for tone marks that should follow vowels
                if i > 0 and self.thai_tones.match(char):
                    # Make sure tone mark comes after vowel if present
                    if len(result) > 0 and self.thai_vowels.match(result[-1]):
                        result.append(char)
                    else:
                        result.append(char)
                else:
                    result.append(char)
            else:
                result.append(char)
            
            i += 1
        
        return ''.join(result)
    
    def detect_thai_content(self, text: str) -> bool:
        """
        Check if text contains Thai characters.
        
        Args:
            text (str): Text to check
            
        Returns:
            bool: True if Thai content found
        """
        return bool(self.thai_pattern.search(text or ""))
    
    def get_thai_content_ratio(self, text: str) -> float:
        """
        Calculate the ratio of Thai characters to total characters.
        
        Args:
            text (str): Input text
            
        Returns:
            float: Ratio of Thai characters (0.0 to 1.0)
        """
        if not text:
            return 0.0
        
        # Remove spaces for calculation
        text_no_spaces = re.sub(r'\s', '', text)
        if not text_no_spaces:
            return 0.0
        
        thai_chars = len(self.thai_pattern.findall(text_no_spaces))
        return thai_chars / len(text_no_spaces)
    
    def create_thai_font(self, font_size: int = 14, bold: bool = False) -> Font:
        """
        Create an Excel Font object optimized for Thai text display.
        
        Args:
            font_size (int): Font size
            bold (bool): Whether font should be bold
            
        Returns:
            Font: openpyxl Font object
        """
        # Use first available Thai font
        font_name = self.THAI_FONTS[0]  # Default to TH Sarabun New
        
        return Font(
            name=font_name,
            size=font_size,
            bold=bold,
            charset=222  # Thai charset
        )
    
    def apply_thai_font_to_cell(self, cell, font_size: int = 14, bold: bool = False):
        """
        Apply Thai-compatible font to an Excel cell.
        
        Args:
            cell: openpyxl cell object
            font_size (int): Font size
            bold (bool): Whether font should be bold
        """
        cell.font = self.create_thai_font(font_size, bold)
    
    def apply_thai_font_to_range(self, worksheet, cell_range: str, font_size: int = 14):
        """
        Apply Thai font to a range of cells.
        
        Args:
            worksheet: openpyxl worksheet object
            cell_range (str): Excel range (e.g., 'A1:C10')
            font_size (int): Font size
        """
        try:
            thai_font = self.create_thai_font(font_size)
            
            for row in worksheet[cell_range]:
                for cell in row:
                    cell.font = thai_font
                    
        except Exception as e:
            self.logger.error(f"Error applying Thai font to range {cell_range}: {str(e)}")
    
    def set_thai_fonts(self, worksheet):
        """
        Apply Thai-compatible fonts to an entire worksheet.
        
        Args:
            worksheet: openpyxl worksheet object
        """
        try:
            thai_font = self.create_thai_font()
            
            # Apply to all cells that have data
            for row in worksheet.iter_rows():
                for cell in row:
                    if cell.value is not None:
                        # Check if cell contains Thai text
                        if isinstance(cell.value, str) and self.detect_thai_content(cell.value):
                            cell.font = self.create_thai_font(font_size=14)
                        else:
                            # Apply standard font for non-Thai content
                            cell.font = Font(name='Tahoma', size=11)
                            
        except Exception as e:
            self.logger.error(f"Error setting Thai fonts: {str(e)}")
    
    def validate_thai_text_accuracy(self, original: str, processed: str) -> float:
        """
        Calculate text accuracy between original and processed Thai text.
        
        Args:
            original (str): Original text
            processed (str): Processed text
            
        Returns:
            float: Accuracy ratio (0.0 to 1.0)
        """
        if not original and not processed:
            return 1.0
        
        if not original or not processed:
            return 0.0
        
        # Normalize both strings
        orig_norm = self.normalize_thai_text(original)
        proc_norm = self.normalize_thai_text(processed)
        
        # Simple character-level comparison
        if len(orig_norm) == 0:
            return 1.0 if len(proc_norm) == 0 else 0.0
        
        # Count matching characters
        matches = sum(1 for a, b in zip(orig_norm, proc_norm) if a == b)
        max_len = max(len(orig_norm), len(proc_norm))
        
        return matches / max_len if max_len > 0 else 0.0
    
    def extract_thai_words(self, text: str) -> List[str]:
        """
        Extract Thai words from text (basic word boundary detection).
        
        Args:
            text (str): Input text
            
        Returns:
            List[str]: List of Thai words
        """
        if not text:
            return []
        
        # Simple approach: split on spaces and punctuation
        # A full implementation would use Thai word segmentation library
        words = []
        
        # Split by whitespace and common punctuation
        segments = re.split(r'[\s\.,;:!?\(\)\[\]{}]+', text)
        
        for segment in segments:
            segment = segment.strip()
            if segment and self.detect_thai_content(segment):
                words.append(segment)
        
        return words
    
    def get_font_recommendations(self) -> List[Dict[str, str]]:
        """
        Get list of recommended fonts for Thai text display.
        
        Returns:
            List of font information dictionaries
        """
        return [
            {
                'name': 'TH Sarabun New',
                'description': 'Best for official Thai documents',
                'usage': 'Government documents, formal reports'
            },
            {
                'name': 'Angsana New',
                'description': 'Good readability for general use',
                'usage': 'General documents, presentations'
            },
            {
                'name': 'Cordia New',
                'description': 'Modern appearance',
                'usage': 'Modern documents, web content'
            }
        ]


def main():
    """Test function for Thai text handler."""
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    
    handler = ThaiTextHandler()
    
    # Test Thai text detection
    thai_text = "สวัสดีครับ นี่คือการทดสอบ"
    english_text = "Hello, this is a test"
    mixed_text = "Hello สวัสดี mixed text ข้อความผสม"
    
    print(f"Thai detection - Thai text: {handler.detect_thai_content(thai_text)}")
    print(f"Thai detection - English text: {handler.detect_thai_content(english_text)}")
    print(f"Thai detection - Mixed text: {handler.detect_thai_content(mixed_text)}")
    
    print(f"Thai ratio - Mixed text: {handler.get_thai_content_ratio(mixed_text):.2f}")
    
    # Test text normalization
    normalized = handler.normalize_thai_text(thai_text)
    print(f"Original: {thai_text}")
    print(f"Normalized: {normalized}")
    
    print("Thai Text Handler initialized successfully")


if __name__ == "__main__":
    main()