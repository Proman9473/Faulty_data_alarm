
# Object Detection Fault Detection Script

This is a Python script for identifying faulty bounding boxes in an object detection dataset. The script goes through XML files which contain the bounding box coordinates and calculates the bounding box area. It compares this area with a threshold based on the average bounding box area in a reference directory.

If the bounding box area is significantly larger than the average area, the script considers the bounding box (and its corresponding image) as faulty. It copies the faulty image and its XML file to a separate directory for further examination. It also draws the bounding box on the faulty image for easy visualization.

## Requirements

The script uses the following Python packages:

- os
- cv2 (OpenCV)
- xml.etree.ElementTree
- shutil
- numpy

Make sure you have them installed in your Python environment.

## Usage

You need to set the following directories at the beginning of the script:

- `img_dir`: The directory containing your images.
- `xml_dir`: The directory containing the XML files for the images.
- `ref_dir`: A reference directory containing XML files used to calculate the average bounding box area.
- `faulty_dir`: The directory where the script will put the faulty images and their XML files.

The script will create the `faulty_dir` directory if it doesn't exist.

Run the script using a Python interpreter. The script will print a message for each faulty image it finds, and it will copy the faulty image and its XML file to the `faulty_dir` directory. It will also create a new image in the `faulty_dir` directory with the bounding box drawn on the faulty image.


