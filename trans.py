import json
import numpy as np
import cv2
import os

# กำหนดการจับคู่ชื่อคลาสกับ ID และสีที่แสดงใน label image
class_to_id = {
    "drivable Area": 0,
    "traffic cone": 1,
    "car": 2,
    "person": 3,
    "slidewalk": 4,
    "parking": 5,
    "crosswalk": 6,
    "vegetation": 7,
    "golf cart": 8
}

# กำหนดสีที่ใช้สำหรับแต่ละ class (สี RGB)
id_to_color = {
    0: [0, 255, 0],      # green for drivable Area (RGB)
    1: [255, 0, 0],      # red for traffic cone (RGB)
    2: [128, 0, 128],    # purple for car (RGB)
    3: [0, 0, 255],      # blue for person (RGB)
    4: [192, 192, 192],  # gray for slidewalk (RGB)
    5: [0, 255, 255],    # cyan for parking (RGB)
    6: [255, 0, 255],    # magenta for crosswalk (RGB)
    7: [0, 128, 0],      # dark green for vegetation (RGB)
    8: [0, 0, 0]         # black for golf cart (RGB)
}
    
# ฟังก์ชันในการแปลงไฟล์ label.png จาก json
def convert_label_to_class_id(json_path, label_output_folder):
    # อ่านข้อมูลจากไฟล์ json
    with open(json_path, 'r') as f:
        label_data = json.load(f)
        
    # สร้างภาพ label ที่จะเก็บผลลัพธ์ (ภาพขนาดเหมือนกับภาพต้นฉบับ)
    img_size = (label_data["imageWidth"], label_data["imageHeight"])
    label_img = np.zeros((img_size[1], img_size[0], 3), dtype=np.uint8)  # 3 ช่อง RGB
    
    # วาดแต่ละ shape ลงใน label image
    for shape in label_data["shapes"]:
        class_name = shape["label"]
        class_id = class_to_id.get(class_name)
        
        if class_id is not None:
            # สร้าง mask ที่มี class ID ตามที่กำหนด
            points = np.array(shape["points"], dtype=np.int32)
            color = id_to_color.get(class_id, [0, 0, 0])  # กำหนดสีตาม ID
            
            # แปลงสีจาก RGB เป็น BGR สำหรับ OpenCV
            bgr_color = [color[2], color[1], color[0]]  # แปลง RGB เป็น BGR
            
            cv2.fillPoly(label_img, [points], bgr_color)  # เติมสีใน mask
    
    # สร้างชื่อไฟล์ output
    base_name = os.path.splitext(os.path.basename(json_path))[0]
    label_output_path = os.path.join(label_output_folder, f"{base_name}_label.png")
        
    # บันทึก label image (OpenCV จะบันทึกในรูปแบบ BGR)
    cv2.imwrite(label_output_path, label_img)
    print(f"✅ แปลง label และบันทึกที่: {label_output_path}")

# โฟลเดอร์ที่เก็บไฟล์ .json
json_folder = "labelme_jsons"  # เปลี่ยนชื่อโฟลเดอร์ให้ตรงกับโฟลเดอร์ของคุณ
label_output_folder = "converted_labels"  # โฟลเดอร์สำหรับบันทึกผลลัพธ์

# สร้างโฟลเดอร์สำหรับเก็บ label หากยังไม่มี
os.makedirs(label_output_folder, exist_ok=True)

# ลูปแปลงทุกไฟล์ .json ในโฟลเดอร์
for filename in os.listdir(json_folder):
    if filename.endswith(".json"):
        json_path = os.path.join(json_folder, filename)
        convert_label_to_class_id(json_path, label_output_folder)

print("\n🎉 เสร็จสิ้น: แปลงไฟล์ทั้งหมดในโฟลเดอร์แล้ว")