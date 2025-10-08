import unittest
import os
import sys
import csv
from PIL import Image, ImageDraw, ImageFont
import tempfile
import shutil

# Add src to path to allow importing generate_quote_images
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from generate_quote_images import QuoteImageGenerator

class TestQuoteImageGenerator(unittest.TestCase):

    def setUp(self):
        """Set up test environment."""
        self.test_dir = tempfile.mkdtemp()
        self.backgrounds_folder = os.path.join(self.test_dir, 'backgrounds')
        os.makedirs(self.backgrounds_folder)
        self.font_path = "./fonts/Quicksand_VariableFont_wght.ttf" # Using a real font for accurate testing
        self.output_folder = os.path.join(self.test_dir, 'output')
        self.quotes_csv = os.path.join(self.test_dir, 'quotes.csv')
        self.logo_path = os.path.join(self.test_dir, 'logo.png')

        # Create dummy files
        self.background_images = []
        for i in range(2):
            background_path = os.path.join(self.backgrounds_folder, f'background_{i}.png')
            Image.new('RGB', (1200, 1200), color = 'blue').save(background_path)
            self.background_images.append(background_path)

        Image.new('RGBA', (100, 100), color = (255, 0, 0, 255)).save(self.logo_path)
        with open(self.quotes_csv, 'w', newline='') as csvfile:
            fieldnames = ['quote', 'author']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({'quote': 'Test quote 1', 'author': 'Author 1'})
            writer.writerow({'quote': 'Test quote 2', 'author': ''})
            writer.writerow({'quote': '', 'author': 'Author 3'})


        self.generator = QuoteImageGenerator(self.backgrounds_folder, self.font_path, self.output_folder, self.quotes_csv, self.logo_path)
        self.quotes = []
        with open(self.quotes_csv, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row.get('quote'):
                    self.quotes.append(row)

    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.test_dir)

    def test_get_wrapped_text(self):
        """Test the _get_wrapped_text method."""
        font = ImageFont.truetype(self.font_path, 60)
        text = "This is a long quote that should be wrapped into multiple lines."
        wrapped_text = self.generator._get_wrapped_text(text, font, 500)
        self.assertIn('\n', wrapped_text)

    def test_add_logo(self):
        """Test the add_logo method."""
        img = Image.new('RGBA', (1200, 1200), (255, 255, 255, 255))
        img_with_logo = self.generator.add_logo(img, (1200, 1200))
        self.assertIsInstance(img_with_logo, Image.Image)
        # Check if the logo (red pixel) is present
        self.assertNotEqual(img_with_logo.getpixel((1100, 1100))[:3], (255, 255, 255))


    def test_create_transparent_overlay(self):
        """Test the create_transparent_overlay method."""
        img = Image.new('RGBA', (1200, 1200), (255, 255, 255, 255))
        rect_width = int(1200 * self.generator.RECTANGLE_PADDING)
        rect_height = int(1200 * self.generator.RECTANGLE_PADDING)
        img_with_overlay, _, _ = self.generator.create_transparent_overlay(img, rect_width, rect_height, (128, 0, 128, 77), (1200, 1200))
        self.assertIsInstance(img_with_overlay, Image.Image)
        # Check if the overlay has been applied
        self.assertNotEqual(img_with_overlay.getpixel((600, 600)), (255, 255, 255, 255))


    def test_draw_text_on_image(self):
        """Test the draw_text_on_image method."""
        img = Image.new('RGB', (1200, 1200), (0, 0, 0))
        draw = ImageDraw.Draw(img)
        quote = "This is a test quote."
        author = "Test Author"
        optimal_font_size = 60
        rect_x = 100
        rect_y = 100
        rect_width = 1000
        rect_height = 1000
        self.generator.draw_text_on_image(draw, quote, author, optimal_font_size, rectangle_x=rect_x, rectangle_y=rect_y, rectangle_width=rect_width, rectangle_height=rect_height, image_size=(1200, 1200))
        # Check that the image has been modified by checking if it has more than one color
        self.assertGreater(len(img.getcolors()), 1)

    def test_get_optimal_font_size(self):
        """Test the get_optimal_font_size method."""
        quote = "This is a test quote."
        rect_width = int(1200 * self.generator.RECTANGLE_PADDING)
        rect_height = int(1200 * self.generator.RECTANGLE_PADDING)
        
        font_size = self.generator.get_optimal_font_size(quote=quote, rectangle_width=rect_width, rectangle_height=rect_height)
        self.assertIsInstance(font_size, int)
        self.assertGreater(font_size, 0)

        long_quote = "This is a much longer test quote to see if the font size will be smaller as expected."
        long_quote_font_size = self.generator.get_optimal_font_size(quote=long_quote, rectangle_width=rect_width, rectangle_height=rect_height)
        self.assertLess(long_quote_font_size, font_size)

    def test_image_generation(self):
        """Test the image generation process."""
        # Run the image generation
        self.generator.generate_images()

        # Check that the output folder was created
        self.assertTrue(os.path.exists(self.output_folder))

        # Check that the correct number of images were generated
        generated_images = os.listdir(self.output_folder)
        self.assertEqual(len(generated_images), len(self.quotes) * len(self.background_images))

        # Check the properties of each generated image
        for background_image_path in self.background_images:
            background_name = os.path.splitext(os.path.basename(background_image_path))[0]
            for i, quote in enumerate(self.quotes):
                expected_filename = f"{background_name}_quote_{i+1}.png"
                self.assertIn(expected_filename, generated_images)
                image_path = os.path.join(self.output_folder, expected_filename)
                self.assertTrue(os.path.exists(image_path))
                self.assertGreater(os.path.getsize(image_path), 0)
                
                with Image.open(image_path) as img:
                    self.assertEqual(img.size, (1200, 1200))

    def test_error_handling(self):
        """Test the error handling."""
        generator = QuoteImageGenerator("non_existent_folder", self.font_path, self.output_folder, self.quotes_csv, self.logo_path)
        generator.generate_images()
        self.assertFalse(os.listdir(self.output_folder))

    def test_empty_csv(self):
        """Test with an empty csv"""
        empty_csv = os.path.join(self.test_dir, 'empty.csv')
        with open(empty_csv, 'w', newline='') as csvfile:
            fieldnames = ['quote', 'author']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
        
        generator = QuoteImageGenerator(self.backgrounds_folder, self.font_path, self.output_folder, empty_csv, self.logo_path)
        generator.generate_images()
        self.assertFalse(os.listdir(self.output_folder))


if __name__ == '__main__':
    unittest.main()