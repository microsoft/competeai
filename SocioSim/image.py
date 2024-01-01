from dataclasses import dataclass

@dataclass
class Image:
    owner: str
    content: str
    description: str


class ImagePool():
    """
    A class for managing images.
    """

    def __init__(self): 
        self._images = []

    def reset(self):
        """
        Clear the image pool.
        """
        self._images = []

    def append_image(self, image: Image):
        """
        Append an image to the pool.

        Parameters:
            image (Image): The image to be added to the pool.
        """
        self._images.append(image)
        # print(f"[ImagePool]: {image.description}")

    def print(self):
        """
        Print all the images in the pool.
        """
        for image in self._images:
            print(f"[ImagePool]: {image.description}")
    
    def get_visible_images(self, restaurant_name: str, step_name: str = None):
        """
        Get all the images that are visible to a given role.

        Parameters:
            visible_to (str): The role that the images are visible to.

        Returns:
            List[Image]: A list of images that are visible to the given role.
        """
        if not restaurant_name:
            return []
        if restaurant_name == "All":
            return self._images
        else:
            return [image for image in self._images if (image.owner == restaurant_name and image.description == step_name)]
