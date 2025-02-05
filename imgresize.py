import argparse
import os
import re
from PIL import Image

def apply_exif_orientation(image):
    try:
        # Check if the image has EXIF data
        exif = image._getexif()
        if exif:
            # Get the orientation tag (ID 274 in EXIF)
            orientation = exif.get(274)
            if orientation:
                # Rotate the image based on the orientation tag
                if orientation == 3:
                    image = image.rotate(180, expand=True)
                elif orientation == 6:
                    image = image.rotate(270, expand=True)
                elif orientation == 8:
                    image = image.rotate(90, expand=True)
    except (AttributeError, KeyError, IndexError):
        # No EXIF data or orientation tag found
        pass
    return image

def rename(input_path, file_name):
    ext = os.path.splitext(input_path)[-1]
    if file_name is None:
        # Extract the filename with extension from input_path
        file_name = os.path.basename(input_path)
        return file_name
    return file_name+ext

def resize_image(input_path, output_path, name, width, height):
   
    with Image.open(input_path) as img:
        img = apply_exif_orientation(img)
        resized_img = img.resize((width,height),Image.Resampling.LANCZOS)
        resized_img.save(output_path+'/'+rename(input_path,name))
       
    
   

def main():
    
    parser = argparse.ArgumentParser(description="Resize one or more images.")
    parser.add_argument("-i", "--input", required=True, help="Path to the input image or folder containing images.")
    parser.add_argument("-s", "--size", required=False, default="600x600", help="New size of the image (e.g., 600x600). Default is 600x600.")
    parser.add_argument("-d", "--destination", required=False, default="./resize", help="Output directory to save resized images. Default is './resize'.")
    parser.add_argument("-n", "--name", required=False, default=None, help="Name of the output image. For multiple images, this will be used as a prefix (e.g., name_1.png, name_2.png).")
    args = parser.parse_args()
    
    input = args.input
    size = args.size
    destination = args.destination
    name = args.name
    
    
    
    
    if os.path.exists(destination):
        # Check if the directory is not empty
        if os.listdir(destination):
            raise ValueError(f"The directory '{destination}' is not empty.")
    else:
        try:
            # Create the directory (and parent directories if needed)
            os.makedirs(destination)
        except OSError as e:
            raise OSError(f"Failed to create directory '{destination}'. Reason: {e}")
        
    pattern_size = r"^\d+x\d+$"
    
    if not re.match(pattern_size, size):
        raise ValueError(f"Bad format '{size}'. ex: 600x600")
    
    
    width, height = map(int, size.split('x'))
    
    print("Waiting ...")

    if os.path.isfile(input):
        resize_image(input, destination,name, width, height)
    else:
        paths = os.listdir(input)
        file_nr=0
        for file in paths:
            file_path = os.path.join(input, file)
            if os.path.isfile(file_path) and file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff')):
                if name is None:
                    resize_image(file_path, destination,name, width, height)
                else:
                    NAME = name + "_" + str(file_nr)
                    resize_image(file_path, destination,NAME, width, height)
                    file_nr += 1

    print("Done")
                
if __name__ == "__main__":
    main()