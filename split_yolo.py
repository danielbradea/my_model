import argparse
import os
import sys
import shutil
import random

def main():
    parser = argparse.ArgumentParser(description="Split YOLO images and labels")
    parser.add_argument("-di", "--dir-images", required=True, help="Folder containing images.")
    parser.add_argument("-dl", "--dir-labels", required=True, help="Folder containing labels.")
    parser.add_argument("-s", "--split", type=float, required=False, default=0.8, help="Fraction of dataset for training (e.g., 0.8 = 80%% train, 20%% validation).")
    parser.add_argument("-o", "--output", required=False, default="./dataset", help="Folder where images and labels are split. Default: ./dataset")
    args = parser.parse_args()

    # Validate arguments
    if not os.path.isdir(args.dir_images):
        print(f"Error: '{args.dir_images}' is not a valid directory.")
        sys.exit(1)

    if not os.path.isdir(args.dir_labels):
        print(f"Error: '{args.dir_labels}' is not a valid directory.")
        sys.exit(1)

    if not (0 < args.split < 1):
        print("Error: Split value must be between 0 and 1.")
        sys.exit(1)

    # Create output folders
    train_images_dir = os.path.join(args.output, "train", "images")
    val_images_dir = os.path.join(args.output, "val", "images")
    train_labels_dir = os.path.join(args.output, "train", "labels")
    val_labels_dir = os.path.join(args.output, "val", "labels")
    
    os.makedirs(train_images_dir, exist_ok=True)
    os.makedirs(val_images_dir, exist_ok=True)
    os.makedirs(train_labels_dir, exist_ok=True)
    os.makedirs(val_labels_dir, exist_ok=True)

    image_extensions = {".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff"}
    
    images = [f.name for f in os.scandir(args.dir_images) 
              if f.is_file() and os.path.splitext(f.name)[1].lower() in image_extensions]
    
    random.shuffle(images)
    split_index = int(len(images) * args.split)
    train_images = images[:split_index]
    val_images = images[split_index:]

    def move_files(files, src_dir, dest_dir, label_src, label_dest):
        for file in files:
            img_src_path = os.path.join(src_dir, file)
            img_dest_path = os.path.join(dest_dir, file)
            shutil.copy(img_src_path, img_dest_path)

            label_file = os.path.splitext(file)[0] + ".txt"
            label_src_path = os.path.join(label_src, label_file)
            label_dest_path = os.path.join(label_dest, label_file)

            if os.path.exists(label_src_path):
                shutil.copy(label_src_path, label_dest_path)

    move_files(train_images, args.dir_images, train_images_dir, args.dir_labels, train_labels_dir)
    move_files(val_images, args.dir_images, val_images_dir, args.dir_labels, val_labels_dir)

    print(f"Dataset split completed: {len(train_images)} training images, {len(val_images)} validation images.")

if __name__ == "__main__":
    main()