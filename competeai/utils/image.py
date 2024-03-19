# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import os
import base64
import requests
from io import BytesIO
from PIL import Image
from tenacity import retry, stop_after_attempt, wait_random_exponential


try:
    # from openai import OpenAI
    import openai
except ImportError:
    is_openai_available = False
    # logging.warning("openai package is not installed")
else:
    openai_api_key = os.environ.get("OPENAI_KEY")
    openai.api_key = openai_api_key
    
    if openai_api_key is None:
        is_openai_available = False
    else:
        is_openai_available = True

# Default config follows the OpenAI playground
DEFAULT_MODEL = "dall-e-3"
DEFAULT_SIZE = '1024x1024'
DEFAULT_QUALITY = "standard"
DEFAULT_RES_FORMAT = "url"

convert_img_to_base64 = lambda img_path: base64.b64encode(open(img_path, 'rb').read()).decode('utf-8')

def generate_image(prompt: str, filepath: str,  size: str = DEFAULT_SIZE, 
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
            # FIXME: v 1.0.0
            # client = OpenAI(api_key=openai_api_key)
            # response = client.images.generate(
            
            # v 0.28.1
            response = openai.Image.create(
                model=model,
                prompt=prompt,
                size=size,
                quality=quality,
                response_format=response_format,
                n=1,
            ) 
            return response['data']

        # @retry(stop=stop_after_attempt(3), wait=wait_random_exponential(min=1, max=60))
        def save_picture(data, filename):
            # get out all the images in API return, whether url or base64
            # note the use of pydantic "model.data" style reference and its model_dump() method
            image_url_list = []
            image_data_list = []
            # FIXME: v 1.0.0
            # for image in data:
            #     image_url_list.append(image.model_dump()["url"])
            #     image_data_list.append(image.model_dump()["b64_json"])
            
            # v 0.28.1
            for image in data:
                if "url" in image:
                    image_url_list.append(image["url"])
                if "b64_json" in image:
                    image_data_list.append(image["b64_json"])

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

        # return response.data[0].url

def combine_images(input_paths, output_path, target_size=(1024, 1024)):
    # 打开第一张图片获取原始长宽
    first_image = Image.open(input_paths[0])

    # 缩小图片为512x512
    resized_images = [Image.open(image_path).resize((128, 128)) for image_path in input_paths]

    # 计算目标图像的长宽
    max_horizontal_images = min(len(input_paths), 4)  # 水平方向最多显示4张图片
    target_width = 128 * max_horizontal_images
    target_height = 128 * ((len(input_paths) - 1) // max_horizontal_images + 1)

    # 创建一个空白的目标图像
    result_image = Image.new("RGB", (target_width, target_height), (255, 255, 255))

    # 计算每张图片在目标图像中的位置
    image_width = target_width // max_horizontal_images
    image_height = target_height // max((len(input_paths) - 1) // max_horizontal_images + 1, 1)

    for i, resized_image in enumerate(resized_images):
        # 将当前图片粘贴到目标图像中的正确位置
        x_position = (i % max_horizontal_images) * image_width
        y_position = (i // max_horizontal_images) * image_height
        result_image.paste(resized_image, (x_position, y_position))

    # 将目标图像保存到文件
    result_image.save(output_path)
    
    # convert to base64
    img_str = convert_img_to_base64(output_path)
    return img_str


# Test function: generate_picture
prompt = """Dish name': 'Coq au Vin', 'price': 30, 'description': 'Classic French stew in which chicken is braised slowly in red wine and a little brandy to yield a supremely rich sauce."""
if __name__ == "__main__":
    generate_image(prompt, filepath="test")


# Test function: combine_pictures
# path = "competeai/logs/test_pic"
# menus = [1, 2, 3, 4]
# input_paths = [f"{path}/menu_{menu}.png" for menu in menus]
# combine_pictures(input_paths, f"{path}/menu.png")