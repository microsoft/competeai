# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

from .image import ImagePool

NAME2PORT = {}
PORT2NAME = {}
BASE_PORT = 9000
DELIMITER = "<<FORMAT>>"
EXP_NAME = None
image_pool = ImagePool()