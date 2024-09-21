import sys
sys.path.append("..")
import icarus.canvasUtilities as canvas
import icarus.constants as constants
import os

# Define the source folder where the images are located
source_folder = "sample-plots/"  # Update this path

# List of image names
image_names = [
    "paris_traffic_jointplot.png",
    "violinplot.png",
    "lineplot.png",
    "violinplot_fuel_comparison.png"
]

# Create full paths for each image
image_paths = [os.path.join(source_folder, image_name) for image_name in image_names]

# Define the output file for the grid image
print(image_paths)
output_file_grid = os.path.join(source_folder, "grid_image.png")

# Call the function to create the image grid
canvas.create_image_grid(image_paths, output_file_grid)
