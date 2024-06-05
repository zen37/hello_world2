# azure.py

from openai import AzureOpenAI
import os
import logging
from datetime import datetime
import requests
from PIL import Image
import json

from image.interface import ImageInterface
from constants import (
    DIR_IMAGES, FORMAT_TIME, FILE_IMAGE_EXT, IMAGE_SERVICE,
    DEFAULT_IMAGE_QUALITY, DEFAULT_IMAGE_SIZE, DEFAULT_IMAGE_STYLE
)
from utils import get_api_key

class AzureImageService(ImageInterface):
    def __init__(self, config):
        self.config = config
        self.client = AzureOpenAI(
            api_version=self.config["api_version_image"],
            api_key=get_api_key(IMAGE_SERVICE),
            azure_endpoint=self.config["endpoint_image"],
        )

    def _generate_image_data(self, prompt):
        image_size = self.config.get("image_size", DEFAULT_IMAGE_SIZE)
        image_quality = self.config.get("image_quality", DEFAULT_IMAGE_QUALITY)
        image_style = self.config.get("image_style", DEFAULT_IMAGE_STYLE)

        result = self.client.images.generate(
            model=self.config["model_image"],
            prompt=prompt,
            n=1,
            size=image_size,
            quality=image_quality,
            style=image_style
        )

        #print(result)
        return json.loads(result.model_dump_json())["data"][0]["url"]

    def _save_image(self, image_url, country_code):
        timestamp = datetime.now().strftime(FORMAT_TIME)
        filename = f"{self.config['model_image']}_{timestamp}.{FILE_IMAGE_EXT}"
        folder = os.path.join(DIR_IMAGES, country_code)

        os.makedirs(folder, exist_ok=True)

        image_path = os.path.join(folder, filename)

        try:
            generated_image = requests.get(image_url).content
            with open(image_path, "wb") as image_file:
                image_file.write(generated_image)
        except requests.RequestException as e:
            logging.error(f"Error downloading the image: {e}")
            return None

        return image_path

    def _display_image(self, image_path):
        try:
            image = Image.open(image_path)
            image.show()
        except Exception as e:
            logging.error(f"Error opening the image: {e}")

    def create(self, country_code, prompt):
        logging.info("Generating image...")

        image_url = self._generate_image_data(prompt)
        if image_url:
            image_path = self._save_image(image_url, country_code)
            if image_path:
                self._display_image(image_path)

        return image_path if image_path else None