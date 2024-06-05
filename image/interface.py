"""
Module: interface.py
Description: Define an abstract base class for image services.
"""
from abc import ABC, abstractmethod

class ImageInterface(ABC):
    """An abstract base class for image services."""
    @abstractmethod
    def create(self, country_code, text):
        """
        Create an image on with the text is written

        Parameters:
        - text (str): The text an image to be created with

        Returns:
        ....
        """