import os
from PIL import Image, ImageDraw, ImageFont
import csv
import zipfile
import glob
import itertools

class QuoteImageGenerator:
    """A class to generate quote images."""

    RECTANGLE_WIDTH_PADDING = 0.85
    RECTANGLE_HEIGHT_PADDING = 0.59
    TEXT_PADDING = 0.8
    LOGO_SIZE = (200, 200)
    LOGO_MARGIN = 20
    AUTHOR_FONT_SIZE_MULTIPLIER = 0.6
    SHADOW_COLOR = (0, 0, 0, 51)  # Black with 20% transparency
    SHADOW_OFFSET = 2
    OVERLAY_COLOR = (160, 32, 240, 100) # purple

    def __init__(self, backgrounds_folder, fonts_folder, output_folder, quotes_csv, logo_path):
        self.backgrounds_folder = backgrounds_folder
        self.fonts_folder = fonts_folder
        self.output_folder = output_folder
        self.quotes_csv = quotes_csv
        self.logo_path = logo_path

    def create_output_folder(self):
        """Create output folder if it doesn't exist."""
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

    def _get_wrapped_text(self, draw, text, font, max_width):
        """Wrap text to fit within a maximum width."""
        lines = []
        for line in text.split('\n'):
            words = line.split(' ')
            current_line = ''
            for word in words:
                if draw.textlength(current_line + ' ' + word, font=font) <= max_width:
                    current_line += ' ' + word
                else:
                    lines.append(current_line.strip())
                    current_line = word
            lines.append(current_line.strip())
        return '\n'.join(lines)

    def _get_text_bbox(self, draw, text, font):
        """Get the bounding box of a text."""
        return draw.textbbox((0, 0), text, font=font)

    def get_optimal_font_size(self, quote, rectangle_width, rectangle_height, font_path):
        """
        Calculates the optimal font size to fill a percentage of the rectangle with the quote.
        """
        low = 10
        high = 300
        optimal_font_size = 10
        draw = ImageDraw.Draw(Image.new('RGB', (1, 1)))

        while low <= high:
            mid = (low + high) // 2
            font = ImageFont.truetype(font_path, mid)
            wrapped_quote = self._get_wrapped_text(draw, quote, font, rectangle_width * self.TEXT_PADDING)

            quote_bbox = self._get_text_bbox(ImageDraw.Draw(Image.new('RGB', (rectangle_width, rectangle_height))), wrapped_quote, font)
            text_height = quote_bbox[3] - quote_bbox[1]

            if text_height <= rectangle_height * self.TEXT_PADDING:
                optimal_font_size = mid
                low = mid + 1
            else:
                high = mid - 1

        return optimal_font_size

    def add_logo(self, image, image_size):
        """Add logo to the image."""
        if os.path.exists(self.logo_path):
            with Image.open(self.logo_path).convert("RGBA") as logo:
                logo.thumbnail(self.LOGO_SIZE)
                logo_x = image_size[0] - logo.width - self.LOGO_MARGIN
                logo_y = image_size[1] - logo.height - self.LOGO_MARGIN
                image.paste(logo, (logo_x, logo_y), logo)
        return image

    def create_transparent_overlay(self, image, rectangle_width, rectangle_height, color, image_size):
        """Create a transparent overlay for the rectangle."""
        overlay = Image.new('RGBA', image.size, (255, 255, 255, 0))
        draw_overlay = ImageDraw.Draw(overlay)
        rectangle_x = (image_size[0] - rectangle_width) / 2
        rectangle_y = (image_size[1] - rectangle_height) / 2
        draw_overlay.rectangle(
            [rectangle_x, rectangle_y, rectangle_x + rectangle_width, rectangle_y + rectangle_height],
            fill=color
        )
        return Image.alpha_composite(image.convert('RGBA'), overlay).convert('RGB'), rectangle_x, rectangle_y

    def _draw_text_with_shadow(self, draw, text, position, font, fill_color, align='left'):
        """Draw text with a shadow."""
        x, y = position
        draw.text((x + self.SHADOW_OFFSET, y + self.SHADOW_OFFSET), text, font=font, fill=self.SHADOW_COLOR, align=align)
        draw.text(position, text, font=font, fill=fill_color, align=align)

    def draw_text_on_image(self, draw, quote, author, optimal_font_size, rectangle_x, rectangle_y, rectangle_width, rectangle_height, image_size, font_path):
        """Draw the quote and author on the image."""
        font = ImageFont.truetype(font_path, optimal_font_size)
        wrapped_quote = self._get_wrapped_text(draw, quote, font, rectangle_width * self.TEXT_PADDING)

        quote_bbox = self._get_text_bbox(draw, wrapped_quote, font)
        quote_width = quote_bbox[2] - quote_bbox[0]
        quote_height = quote_bbox[3] - quote_bbox[1]

        text_x = rectangle_x + (rectangle_width - quote_width) / 2
        text_y = rectangle_y + (rectangle_height - quote_height) / 2

        self._draw_text_with_shadow(draw, wrapped_quote, (text_x, text_y), font, (255, 255, 255), align='center')

        if author:
            author_text = f"- {author}"
            author_font_size = int(optimal_font_size * self.AUTHOR_FONT_SIZE_MULTIPLIER)
            author_font = ImageFont.truetype(font_path, author_font_size)
            author_bbox = self._get_text_bbox(draw, author_text, font=author_font)
            author_width = author_bbox[2] - author_bbox[0]
            author_height = author_bbox[3] - author_bbox[1]

            author_x = image_size[0] - author_width - self.LOGO_MARGIN
            author_y = image_size[1] - author_height - self.LOGO_MARGIN

            self._draw_text_with_shadow(draw, author_text, (author_x, author_y), author_font, (255, 255, 255))

    def _prepare_base_image(self, image_template):
        """Prepare the base image by adding logo and overlay."""
        image_size = image_template.size
        image = image_template.copy().convert('RGBA')
        image = self.add_logo(image, image_size)

        # Create a transparent overlay over the entire background
        image, _, _ = self.create_transparent_overlay(
            image=image,
            rectangle_width=image_size[0],
            rectangle_height=image_size[1],
            color=self.OVERLAY_COLOR,
            image_size=image_size
        )

        rectangle_width = int(image_size[0] * self.RECTANGLE_WIDTH_PADDING)
        rectangle_height = int(image_size[1] * self.RECTANGLE_HEIGHT_PADDING)

        # The original transparent overlay for the text area is now part of the main overlay
        # so we just calculate the rectangle coordinates
        rectangle_x = (image_size[0] - rectangle_width) / 2
        rectangle_y = (image_size[1] - rectangle_height) / 2

        draw = ImageDraw.Draw(image)
        return image, draw, rectangle_x, rectangle_y, rectangle_width, rectangle_height, image_size

    def _add_text_to_image(self, draw, quote, author, rectangle_x, rectangle_y, rectangle_width, rectangle_height, image_size, font_path):
        """Add text to the image."""
        optimal_font_size = self.get_optimal_font_size(quote=quote, rectangle_width=rectangle_width, rectangle_height=rectangle_height, font_path=font_path)
        self.draw_text_on_image(draw=draw, quote=quote, author=author, optimal_font_size=optimal_font_size, rectangle_x=rectangle_x, rectangle_y=rectangle_y, rectangle_width=rectangle_width, rectangle_height=rectangle_height, image_size=image_size, font_path=font_path)

    def _save_image(self, image, index, background_name):
        """Save the image."""
        output_dir = os.path.join(self.output_folder, background_name)
        os.makedirs(output_dir, exist_ok=True)
        output_filename = f"{background_name}_quote_{index+1}.png"
        output_path = os.path.join(output_dir, output_filename)
        image.save(output_path)
        print(f"Generated: {output_path}")

    def _generate_single_image(self, image_template, row, index, background_name, font_path):
        """Generate a single quote image."""
        try:
            # quote = row.get('quote', '').upper()
            quote = row.get('quote', '')
            author = row.get('author', '').title()
            if not quote:
                print(f"Warning: Empty quote in row {index+1}, skipping.")
                return

            image, draw, rectangle_x, rectangle_y, rectangle_width, rectangle_height, image_size = self._prepare_base_image(image_template)
            self._add_text_to_image(draw, quote, author, rectangle_x, rectangle_y, rectangle_width, rectangle_height, image_size, font_path)
            self._save_image(image, index, background_name)

        except Exception as e:
            print(f"Error processing row {index+1}: {e}")

    def _process_csv(self, background_images, background_name, fonts):
        """Process the CSV file and generate images."""
        try:
            with open(self.quotes_csv, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                background_cycler = itertools.cycle(background_images)
                font_cycler = itertools.cycle(fonts)
                # Skip header row
                for index, line in enumerate(lines[1:]):
                    row = {'quote': line.strip(), 'author': ''}
                    background_image_path = next(background_cycler)
                    font_path = next(font_cycler)
                    with Image.open(background_image_path).convert('RGB') as image_template:
                        self._generate_single_image(image_template, row, index, background_name, font_path)
        except FileNotFoundError:
            print(f"Error: {self.quotes_csv} not found. Ensure it exists in the specified directory.")
        except Exception as e:
            print(f"Error reading CSV or processing data: {e}")
        else:
            print("Image generation completed!")


    def generate_images(self):
        """Generate quote images from a CSV file."""
        self.create_output_folder()
        try:
            fonts = glob.glob(os.path.join(self.fonts_folder, '*.ttf'))
            for background_folder in os.listdir(self.backgrounds_folder):
                background_folder_path = os.path.join(self.backgrounds_folder, background_folder)
                if os.path.isdir(background_folder_path):
                    background_images = glob.glob(os.path.join(background_folder_path, '*.png')) + \
                                        glob.glob(os.path.join(background_folder_path, '*.jpg')) + \
                                        glob.glob(os.path.join(background_folder_path, '*.jpeg'))

                    if background_images:
                        self._process_csv(background_images, background_folder, fonts)

                        output_dir = os.path.join(self.output_folder, background_folder)
                        generated_images = glob.glob(os.path.join(output_dir, '*.png'))
                        if generated_images:
                            zip_filename = f"{background_folder}_quotes.zip"
                            zip_filepath = os.path.join(self.output_folder, zip_filename)

                            with zipfile.ZipFile(zip_filepath, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zipf:
                                for image_file in generated_images:
                                    zipf.write(image_file, os.path.basename(image_file))
                            print(f"Created zip file: {zip_filepath}")
                        else:
                            print(f"No images generated for {background_folder}, skipping zip creation.")

        except FileNotFoundError:
            print(f"Error: Backgrounds folder {self.backgrounds_folder} not found.")

if __name__ == "__main__":
    QuoteImageGenerator(
        backgrounds_folder="./backgrounds",
        fonts_folder="./fonts",
        output_folder="quote_images",
        # quotes_csv= "./quotes/test.csv",
        # quotes_csv= "./quotes/tester.csv",
        quotes_csv= "./quotes/views.csv",
        logo_path="./logo/beyond_the_grind_logo_transparent.png",
    ).generate_images()
