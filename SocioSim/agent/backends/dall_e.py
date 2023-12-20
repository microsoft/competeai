import os
from tenacity import retry, stop_after_attempt, wait_random_exponential

from .base import IntelligenceBackend

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


class DALLEGen(IntelligenceBackend):
    """
    Interface to the DALLE style model
    """
    type_name = "dall_e"
    stateful = False
    
    def __init__(self, size: str = DEFAULT_SIZE, quality: str = DEFAULT_QUALITY,
                 model: str = DEFAULT_MODEL, response_format: str = DEFAULT_RES_FORMAT, **kwargs):
        """
        instantiate the DALLEChat backend
        args:
            size: the size of the picture
            quality: usually standard
            model: the model to use
        """
        assert is_openai_available, "openai package is not installed or the API key is not set"
        super().__init__(size=size, quality=quality, model=model, **kwargs)

        self.size = size
        self.quality = quality
        self.model = model
        self.response_format = response_format

    @retry(stop=stop_after_attempt(6), wait=wait_random_exponential(min=1, max=60))
    def _get_response(self, prompt):
        client = OpenAI(api_key=openai_api_key)
        response = client.images.generate(
            model=self.model,
            prompt=prompt,
            size=self.size,
            quality=self.quality,
            response_format=self.response_format,
            n=1,
        )
        if self.response_format == "url":
            image_url = response.data[0]
            return image_url
        elif self.response_format == "b64_json":
            pass # TODO

    def query(self, prompt: str, *args, **kwargs) -> str:
        """
        format the input and call the ChatGPT/GPT-4 API
        args:
            prompt: A text description of the desired image(s).
        """
        
        response = self._get_response(prompt, *args, **kwargs)

        return response
