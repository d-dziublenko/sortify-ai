"""
Basic tests for Sortify AI Image Analyzer
"""

import pytest
import os
from unittest.mock import Mock, patch
from pathlib import Path

# Add parent directory to path
import sys
sys.path.append(str(Path(__file__).parent.parent))

from image_analyzer import ImageAnalyzer, find_images


class TestImageAnalyzer:
    """Test cases for the ImageAnalyzer class"""
    
    @pytest.fixture
    def analyzer(self):
        """Create an ImageAnalyzer instance with mock API key"""
        return ImageAnalyzer(api_key="test-api-key")
    
    def test_analyzer_initialization(self, analyzer):
        """Test that analyzer initializes correctly"""
        assert analyzer.client is not None
        assert analyzer.model == "gpt-4o"
    
    def test_merge_categories(self, analyzer):
        """Test category merging functionality"""
        category_groups = [
            {"main": "travel", "subcategories": ["beaches", "cities"]},
            {"main": "travel", "subcategories": ["cities", "landmarks"]},
            {"main": "food", "subcategories": ["desserts"]}
        ]
        
        merged = analyzer._merge_categories(category_groups)
        
        # Check that categories are properly merged
        assert len(merged) == 2
        
        # Find travel category
        travel_cat = next(c for c in merged if c["main"] == "travel")
        assert set(travel_cat["subcategories"]) == {"beaches", "cities", "landmarks"}
        
        # Find food category
        food_cat = next(c for c in merged if c["main"] == "food")
        assert food_cat["subcategories"] == ["desserts"]


class TestUtilityFunctions:
    """Test utility functions"""
    
    def test_find_images_non_recursive(self, tmp_path):
        """Test finding images in a single directory"""
        # Create test files
        (tmp_path / "image1.jpg").touch()
        (tmp_path / "image2.png").touch()
        (tmp_path / "document.txt").touch()
        
        images = find_images(str(tmp_path), recursive=False)
        
        assert len(images) == 2
        assert any("image1.jpg" in img for img in images)
        assert any("image2.png" in img for img in images)
        assert not any("document.txt" in img for img in images)
    
    def test_find_images_recursive(self, tmp_path):
        """Test finding images recursively"""
        # Create nested structure
        subdir = tmp_path / "subdir"
        subdir.mkdir()
        
        (tmp_path / "image1.jpg").touch()
        (subdir / "image2.png").touch()
        (subdir / "image3.gif").touch()
        
        images = find_images(str(tmp_path), recursive=True)
        
        assert len(images) == 3
        assert any("image1.jpg" in img for img in images)
        assert any("image2.png" in img for img in images)
        assert any("image3.gif" in img for img in images)
    
    def test_find_images_empty_directory(self, tmp_path):
        """Test behavior with empty directory"""
        images = find_images(str(tmp_path), recursive=False)
        assert images == []
    
    def test_find_images_supported_formats(self, tmp_path):
        """Test that all supported formats are recognized"""
        formats = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']
        
        for fmt in formats:
            (tmp_path / f"test{fmt}").touch()
        
        images = find_images(str(tmp_path), recursive=False)
        assert len(images) == len(formats)


class TestImageAnalyzerMocked:
    """Test ImageAnalyzer with mocked OpenAI API"""
    
    @patch('image_analyzer.OpenAI')
    def test_categorize_image_success(self, mock_openai):
        """Test successful image categorization"""
        # Mock the API response
        mock_response = Mock()
        mock_response.choices = [Mock(message=Mock(content="travel/beaches: Beautiful sunset at the beach"))]
        mock_openai.return_value.chat.completions.create.return_value = mock_response
        
        analyzer = ImageAnalyzer(api_key="test-key")
        
        # Create a test image file
        with patch('builtins.open', create=True) as mock_open:
            mock_open.return_value.__enter__.return_value.read.return_value = b'fake_image_data'
            
            result = analyzer.categorize_image("test.jpg", [{"main": "travel", "subcategories": ["beaches"]}])
        
        assert result["category"] == "travel/beaches"
        assert "Beautiful sunset" in result["explanation"]
        assert result["filename"] == "test.jpg"
    
    @patch('image_analyzer.OpenAI')
    def test_analyze_image_matches(self, mock_openai):
        """Test image analysis for query matching"""
        # Mock the API response
        mock_response = Mock()
        mock_response.choices = [Mock(message=Mock(content="YES, this image contains a dog playing in the park"))]
        mock_openai.return_value.chat.completions.create.return_value = mock_response
        
        analyzer = ImageAnalyzer(api_key="test-key")
        
        with patch('builtins.open', create=True) as mock_open:
            mock_open.return_value.__enter__.return_value.read.return_value = b'fake_image_data'
            
            result = analyzer.analyze_image("dog.jpg", "dogs playing")
        
        assert result["matches"] is True
        assert "dog playing" in result["explanation"]
        assert result["filename"] == "dog.jpg"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])