import os
import cv2
import albumentations as A
import shutil

# input dataset
input_img_dir = "images/"
input_json_dir = "labelme_json/"
output_dir = "dataset/"
os.makedirs(output_dir, exist_ok=True)

# Transform 1: ทำให้สว่างขึ้น
transform_bright = A.Compose([
    A.RandomBrightnessContrast(brightness_limit=(0.15, 0.5), contrast_limit=0.2, p=1.0)
])

# Transform 2: ทำให้มืดลง
transform_dark = A.Compose([
    A.RandomBrightnessContrast(brightness_limit=(-0.5, -0.2), contrast_limit=0.2, p=1.0)
])

for filename in os.listdir(input_img_dir):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        img_path = os.path.join(input_img_dir, filename)
        image = cv2.imread(img_path)

        # -------------------
        # 1) copy ไฟล์ต้นฉบับ
        # -------------------
        shutil.copy(img_path, os.path.join(output_dir, filename))

        json_name = os.path.splitext(filename)[0] + ".json"
        json_in_path = os.path.join(input_json_dir, json_name)
        if os.path.exists(json_in_path):
            shutil.copy(json_in_path, os.path.join(output_dir, json_name))

        # -------------------
        # 2) ภาพสว่างขึ้น
        # -------------------
        aug_bright = transform_bright(image=image)["image"]
        aug_img_name_bright = os.path.splitext(filename)[0] + "_bright.jpg"
        cv2.imwrite(os.path.join(output_dir, aug_img_name_bright), aug_bright)

        if os.path.exists(json_in_path):
            shutil.copy(json_in_path, os.path.join(output_dir, os.path.splitext(filename)[0] + "_bright.json"))

        # -------------------
        # 3) ภาพมืดลง
        # -------------------
        aug_dark = transform_dark(image=image)["image"]
        aug_img_name_dark = os.path.splitext(filename)[0] + "_dark.jpg"
        cv2.imwrite(os.path.join(output_dir, aug_img_name_dark), aug_dark)

        if os.path.exists(json_in_path):
            shutil.copy(json_in_path, os.path.join(output_dir, os.path.splitext(filename)[0] + "_dark.json"))
