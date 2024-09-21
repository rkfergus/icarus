import sys
sys.path.append("..")
import icarus.canvasUtilities as canvas
import icarus.constants as constants
import os

# Define the source folder where the images are located
source_folder = "sample-plots/grid-board-tests"  # Update this path

# List of image names
image_names = [
    "paris_traffic_jointplot.png",
    "violinplot.png",
    "lineplot.png",
    "violinplot_fuel_comparison.png"
]

# Create full paths for each image
image_paths = [os.path.join(source_folder, image_name) for image_name in image_names]

# Define the different test cases
test_cases = {
    "no_border": {"border": False},
    "red_border": {"border": True},
    "custom_border": {"border": (0, 255, 0), "border_size": 3},  # Green border
    "zero_border": {"border": True, "border_size": 0},
    "border_false": {"border": False}
}

# Loop to create output file names and run each test case
for test_name, params in test_cases.items():
    output_file = os.path.join(source_folder, f"grid_image_{test_name}.png")
    print(f"Generating {output_file} with params: {params}")
    canvas.create_image_grid(image_paths, output_file, **params)

print("All test images generated.")
