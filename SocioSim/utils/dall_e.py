import os
import base64
import requests
from io import BytesIO
from PIL import Image
from tenacity import retry, stop_after_attempt, wait_random_exponential


try:
    from openai import OpenAI
except ImportError:
    is_openai_available = False
    # logging.warning("openai package is not installed")
else:
    openai_api_key = os.environ.get("OPENAI_KEY")

    if openai_api_key is None:
        is_openai_available = False
    else:
        is_openai_available = True

# Default config follows the OpenAI playground
DEFAULT_MODEL = "dall-e-3"
DEFAULT_SIZE = '1024x1024'
DEFAULT_QUALITY = "standard"
DEFAULT_RES_FORMAT = "url"

def generate_picture(prompt: str, filepath: str,  size: str = DEFAULT_SIZE, 
                       quality: str = DEFAULT_QUALITY, model: str = DEFAULT_MODEL, response_format: str = DEFAULT_RES_FORMAT, 
                       **kwargs):
        """
        instantiate the DALLEChat backend
        args:
            size: the size of the picture
            quality: usually standard
            model: the model to use
        """
        assert is_openai_available, "openai package is not installed or the API key is not set"
    
        size = size
        quality = quality
        model = model
        response_format = response_format
    
        @retry(stop=stop_after_attempt(6), wait=wait_random_exponential(min=1, max=60))
        def _get_response(prompt):
            client = OpenAI(api_key=openai_api_key)
            response = client.images.generate(
                model=model,
                prompt=prompt,
                size=size,
                quality=quality,
                response_format=response_format,
                n=1,
            ) 
            return response

        @retry(stop=stop_after_attempt(3), wait=wait_random_exponential(min=1, max=60))
        def save_picture(response, filename):
            # get out all the images in API return, whether url or base64
            # note the use of pydantic "model.data" style reference and its model_dump() method
            image_url_list = []
            image_data_list = []
            for image in response.data:
                image_url_list.append(image.model_dump()["url"])
                image_data_list.append(image.model_dump()["b64_json"])

            # Initialize an empty list to store the Image objects
            image_objects = []

            # Check whether lists contain urls that must be downloaded or b64_json images
            if image_url_list and all(image_url_list):
                # Download images from the urls
                for i, url in enumerate(image_url_list):
                    print(f"getting URL: {url}")
                    response = requests.get(url)
                    response.raise_for_status()  # Raises stored HTTPError, if one occurred.

                    image_objects.append(Image.open(BytesIO(response.content)))  # Append the Image object to the list
                    filename = filename if i == 0 else f"{filename}_{i}"
                    image_objects[i].save(f"{filename}.png")
                    print(f"{filename}.png was saved")
            elif image_data_list and all(image_data_list):  # if there is b64 data
                # Convert "b64_json" data to png file
                for i, data in enumerate(image_data_list):
                    image_objects.append(Image.open(BytesIO(base64.b64decode(data))))  # Append the Image object to the list
                    filename = filename if i == 0 else f"{filename}_{i}"
                    image_objects[i].save(f"{filename}.png")
                    print(f"{filename}.png was saved")
            else:
                print("No image data was obtained. Maybe bad code?")
        
        
        response = _get_response(prompt)
        save_picture(response, filepath)

        return response.data[0].url


# prompt = """Dish name': 'Coq au Vin', 'price': 30, 'description': 'Classic French stew in which chicken is braised slowly in red wine and a little brandy to yield a supremely rich sauce."""
# if __name__ == "__main__":
#     generate_picture(prompt, filename="test")
