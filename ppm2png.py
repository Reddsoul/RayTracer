import os
from PIL import Image

def convert_ppm_to_png(input_folder, output_folder):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Iterate through all .ppm files in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith('.ppm'):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, os.path.splitext(filename)[0] + '.png')
            
            # Open the .ppm file and convert it to .png
            with Image.open(input_path) as img:
                img.save(output_path, 'PNG')
            print(f"Converted {filename} to {output_path}")

# Input and output folder paths
input_folder = './output'  # Folder containing .ppm files
output_folder = './output_png'  # Destination folder for .png files

# Convert .ppm to .png
convert_ppm_to_png(input_folder, output_folder)