"""
Tests for Thai Text Handler module.
"""

import unittest
from src.thai_handler import ThaiTextHandler


class TestThaiTextHandler(unittest.TestCase):
    """Test cases for Thai text handler."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.handler = ThaiTextHandler()
    
    def test_detect_thai_content(self):
        """Test Thai content detection."""
        # Test Thai text
        thai_text = "สวัสดีครับ"
        self.assertTrue(self.handler.detect_thai_content(thai_text))
        
        # Test English text
        english_text = "Hello World"
        self.assertFalse(self.handler.detect_thai_content(english_text))
        
        # Test mixed text
        mixed_text = "Hello สวัสดี World"
        self.assertTrue(self.handler.detect_thai_content(mixed_text))
        
        # Test empty/None
        self.assertFalse(self.handler.detect_thai_content(""))
        self.assertFalse(self.handler.detect_thai_content(None))
    
    def test_get_thai_content_ratio(self):
        """Test Thai content ratio calculation."""
        # Pure Thai text
        thai_text = "สวัสดีครับ"
        ratio = self.handler.get_thai_content_ratio(thai_text)
        self.assertEqual(ratio, 1.0)
        
        # Pure English text
        english_text = "Hello"
        ratio = self.handler.get_thai_content_ratio(english_text)
        self.assertEqual(ratio, 0.0)
        
        # Mixed text (roughly 50/50)
        mixed_text = "สวัสดีHello"
        ratio = self.handler.get_thai_content_ratio(mixed_text)
        self.assertGreater(ratio, 0.0)
        self.assertLess(ratio, 1.0)
        
        # Empty text
        self.assertEqual(self.handler.get_thai_content_ratio(""), 0.0)
        self.assertEqual(self.handler.get_thai_content_ratio(None), 0.0)
    
    def test_normalize_thai_text(self):
        """Test Thai text normalization."""
        # Test with normal text
        text = "สวัสดีครับ   นี่คือการทดสอบ"
        normalized = self.handler.normalize_thai_text(text)
        
        # Should remove extra spaces
        self.assertNotIn("   ", normalized)
        self.assertTrue(normalized.strip())
        
        # Test with empty text
        self.assertEqual(self.handler.normalize_thai_text(""), "")
        self.assertEqual(self.handler.normalize_thai_text(None), None)
    
    def test_extract_thai_words(self):
        """Test Thai word extraction."""
        text = "สวัสดีครับ Hello นี่คือการทดสอบ World"
        words = self.handler.extract_thai_words(text)
        
        # Should extract Thai words only
        self.assertIn("สวัสดีครับ", words)
        self.assertIn("นี่คือการทดสอบ", words)
        self.assertNotIn("Hello", words)
        self.assertNotIn("World", words)
        
        # Test with empty text
        self.assertEqual(self.handler.extract_thai_words(""), [])
        self.assertEqual(self.handler.extract_thai_words(None), [])
    
    def test_create_thai_font(self):
        """Test Thai font creation."""
        font = self.handler.create_thai_font()
        
        # Should have Thai font name
        self.assertIn(font.name, self.handler.THAI_FONTS)
        self.assertEqual(font.charset, 222)  # Thai charset
        
        # Test with custom parameters
        bold_font = self.handler.create_thai_font(font_size=16, bold=True)
        self.assertEqual(bold_font.size, 16)
        self.assertTrue(bold_font.bold)
    
    def test_validate_thai_text_accuracy(self):
        """Test text accuracy validation."""
        # Identical text should have 100% accuracy
        text = "สวัสดีครับ"
        accuracy = self.handler.validate_thai_text_accuracy(text, text)
        self.assertEqual(accuracy, 1.0)
        
        # Empty texts
        accuracy = self.handler.validate_thai_text_accuracy("", "")
        self.assertEqual(accuracy, 1.0)
        
        # Different texts should have lower accuracy
        text1 = "สวัสดีครับ"
        text2 = "สวัสดีค่ะ"
        accuracy = self.handler.validate_thai_text_accuracy(text1, text2)
        self.assertLess(accuracy, 1.0)
        self.assertGreater(accuracy, 0.0)
    
    def test_font_recommendations(self):
        """Test font recommendations."""
        recommendations = self.handler.get_font_recommendations()
        
        self.assertIsInstance(recommendations, list)
        self.assertGreater(len(recommendations), 0)
        
        # Check structure of recommendations
        for rec in recommendations:
            self.assertIn('name', rec)
            self.assertIn('description', rec)
            self.assertIn('usage', rec)


if __name__ == '__main__':
    unittest.main()