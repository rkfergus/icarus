import sys
from PIL import Image

def center_image_on_canvas(input_image_path, output_image_path, canvas_size=(4000, 4000)):
    """Centers an image on a transparent canvas of the specified size.

    Args:
        input_image_path (str): Path to the input image to center.
        output_image_path (str): Path where the centered image will be saved.
        canvas_size (tuple): Size of the canvas (width, height). Default is (4000, 4000).
    """
    # Create a new transparent image (canvas)
    new_image = Image.new("RGBA", canvas_size, (0, 0, 0, 0))  # Fully transparent

    # Open the heatmap image
    heatmap_image = Image.open(input_image_path)

    # Calculate the position to center the heatmap image
    heatmap_width, heatmap_height = heatmap_image.size
    position = ((canvas_size[0] - heatmap_width) // 2, (canvas_size[1] - heatmap_height) // 2)

    # Paste the heatmap image onto the center of the new image
    new_image.paste(heatmap_image, position, heatmap_image)  # Use heatmap_image as mask for transparency

    # Save the new image
    new_image.save(output_image_path, format='PNG')
    print(f"Centered image saved to {output_image_path}")

