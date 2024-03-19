# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

from competeai.utils import convert_img_to_base64, combine_images

import os

print(os.getcwd())

dish_ids = [0,1,2]
folder_path = f"./logs/test_pic/restaurant_design_9001"
img_paths = [f"{folder_path}/menu_{id}.png" for id in dish_ids]
img_base64_menu = combine_images(input_paths=img_paths, output_path=f"{folder_path}/menu.png")

# Restaurant image
img_base64_r = convert_img_to_base64(f"{folder_path}/basic_info_0.png")

print("success!")
