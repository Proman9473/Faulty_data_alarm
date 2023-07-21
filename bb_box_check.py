import os
import cv2
import xml.etree.ElementTree as ET
import shutil
import numpy as np

# Directories
img_dir = 'img_dir'
xml_dir = 'xml_dir'
ref_dir = 'ref_dir'
faulty_dir = 'faulty_dir'

# Create the faulty directory if it doesn't exist
os.makedirs(faulty_dir, exist_ok=True)

# Calculate average bounding box area from the reference directory
areas = []
for dirpath, dirnames, filenames in os.walk(ref_dir):
    for file in filenames:
        base_name, ext = os.path.splitext(file)
        if ext.lower() != '.xml':
            continue

        xml_path = os.path.join(dirpath, file)

        # Parse XML and get bounding box
        xml_root = ET.parse(xml_path).getroot()
        for object in xml_root.findall('object'):
            bndbox = object.find('bndbox')
            xmin = float(bndbox.find('xmin').text)
            ymin = float(bndbox.find('ymin').text)
            xmax = float(bndbox.find('xmax').text)
            ymax = float(bndbox.find('ymax').text)

            area = (xmax - xmin) * (ymax - ymin)
            areas.append(area)

average_area = np.mean(areas)
threshold = 7 * average_area

# Check XML files and corresponding images
for dirpath, dirnames, filenames in os.walk(xml_dir):
    for file in filenames:
        base_name, ext = os.path.splitext(file)
        if ext.lower() != '.xml':
            continue

        xml_path = os.path.join(dirpath, file)
        img_path = os.path.join(img_dir, base_name + '.jpg')

        # Parse XML and get bounding box
        xml_root = ET.parse(xml_path).getroot()
        for object in xml_root.findall('object'):
            bndbox = object.find('bndbox')
            xmin = int(float(bndbox.find('xmin').text))
            ymin = int(float(bndbox.find('ymin').text))
            xmax = int(float(bndbox.find('xmax').text))
            ymax = int(float(bndbox.find('ymax').text))

            bbox_area = (xmax - xmin) * (ymax - ymin)

            if bbox_area > threshold:
                print(f"Bounding box in {file} is larger than expected")

                # Create a unique filename using the base name and the name of the parent directory
                unique_filename = f"{base_name}_{dirpath.split(os.sep)[-1]}"

                # Copy the faulty image and XML file to the faulty directory
                shutil.copy(img_path, os.path.join(faulty_dir, f"{unique_filename}.jpg"))
                shutil.copy(xml_path, os.path.join(faulty_dir, f"{unique_filename}.xml"))

                # Draw bounding box
                img = cv2.imread(img_path)
                cv2.rectangle(img, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
                cv2.imwrite(os.path.join(faulty_dir, f"{unique_filename}_bbox.jpg"), img)
                break
