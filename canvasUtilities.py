import sys
from PIL import Image, ImageColor
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S')



def center_image_on_canvas(input_image_path, output_image_path, canvas_size=(4000, 4000)):
    """
    Centers an image on a transparent canvas of the specified size.

    Args:
        input_image_path (str): Path to the input image file.
        output_image_path (str): Path to save the output image file.
        canvas_size (tuple): Size of the canvas as (width, height). Default is (4000, 4000).

    Returns:
        Image: The centered image on the canvas.
    """
    new_image = Image.new("RGBA", canvas_size, (0, 0, 0, 0))  # Fully transparent
    heatmap_image = Image.open(input_image_path)
    heatmap_width, heatmap_height = heatmap_image.size
    position = ((canvas_size[0] - heatmap_width) // 2, (canvas_size[1] - heatmap_height) // 2)
    new_image.paste(heatmap_image, position, heatmap_image)  # Use heatmap_image as mask for transparency
    new_image.save(output_image_path, format='PNG')  # Save the centered image
    return new_image  # Return the centered image

def scale_image(image, max_size):
    """
    Scales down an image to fit within the max size while maintaining aspect ratio.

    Args:
        image (Image): The image to be scaled.
        max_size (tuple): The maximum size as (width, height).

    Returns:
        Image: The scaled image.
    """
    image.thumbnail(max_size, Image.ANTIALIAS)
    return image  # Return the scaled image

def add_border(image, border_size=2, border_color=(255, 0, 0)):
    """
    Adds a border around the given image.

    Args:
        image (Image): The image to add a border to.
        border_size (int): The size of the border. Default is 2.
        border_color (tuple): The color of the border as an (R, G, B) tuple. Default is red (255, 0, 0).

    Returns:
        Image: The image with the border added.
    """
    bordered_image = Image.new("RGBA", (image.width + border_size * 2, image.height + border_size * 2), border_color)
    bordered_image.paste(image, (border_size, border_size))  # Paste the original image in the center
    return bordered_image

def create_image_grid(image_paths, output_image_path, canvas_size=(4000, 4000), grid_size=(2, 2), border=None, border_size=2):
    """
    Arranges a list of images in a grid, saves the result, and checks dimensions.

    Args:
        image_paths (list): List of paths to the image files.
        output_image_path (str): Path to save the output image file.
        canvas_size (tuple): Size of the canvas as (width, height). Default is (4000, 4000).
        grid_size (tuple): Number of images in the grid as (rows, columns). Default is (2, 2).
        border (bool/str/tuple): Border color or flag. Can be True (default red), False (no border), 
                                 "transparent" (fully transparent), or an (R, G, B) tuple.
        border_size (int): The size of the border. Default is 2.

    Raises:
        ValueError: If an invalid border color is provided.

    Returns:
        None
    """
    
    # Handle border color and size logic
    if border is True:
        border_color = (255, 0, 0)  # Red by default
    elif border is False or border_size == 0:
        border_color = None
    elif isinstance(border, str):
        if border.lower() == "transparent":
            border_color = (0, 0, 0, 0)  # Fully transparent
        else:
            try:
                border_color = ImageColor.getrgb(border)  # Convert named color or hex to RGB
                border_color += (255,)  # Add full opacity
            except ValueError:
                raise ValueError(f"Invalid border color: {border}")
    elif isinstance(border, tuple):
        border_color = border
    else:
        border_color = None
    
    # Load images and add borders if applicable
    if border:
        images = [add_border(Image.open(img), border_size, border_color) for img in image_paths]
    else:
        images = [Image.open(img) for img in image_paths]
    
    # Create a new image for the grid
    grid_width = sum(max(images[i + j * grid_size[0]].width for j in range(grid_size[1])) for i in range(grid_size[0]))
    grid_height = sum(max(images[i].height for i in range(j * grid_size[0], min((j + 1) * grid_size[0], len(images)) )) for j in range(grid_size[1]))

    grid_image = Image.new("RGBA", (grid_width, grid_height), (0, 0, 0, 0))  # Transparent background


    # grid_offsets = [[(0, 0) for _ in range(grid_size[1])] for _ in range(grid_size[0])]

    row_heights = [0 for _ in range(grid_size[0])]
    col_widths = [0 for _ in range(grid_size[1])]
    print(row_heights, col_widths)

    for index, img in enumerate(images):
        col = index % grid_size[0]  # Determine the column
        row = index // grid_size[0]  # Determine the row

        # Determine the starting coordinates
        img_width, img_height = img.size
    
        logging.info(f"Image: {index}, Row: {row}, Col: {col}")
        logging.info(f"Image size: {img.size}")
    
        x = 0
        if col > 0:
            x = col_widths[col-1]
    
        y = 0
        if row > 0:
            y = row_heights[row-1]
    
        logging.info(f"X: {x}, Y: {y}")
        grid_image.paste(img, (x, y))
    
        if img_width > col_widths[col]:
            col_widths[col] = img_width # Update the max width in the column
    
        if img_height > row_heights[row]:
            row_heights[row] = img_height # Update the max height in the row
    
        logging.info(f"Row heights: {row_heights}, Col widths: {col_widths}")
    
        # Save the grid image before checking size
        grid_image.save(output_image_path, format='PNG')
        logging.info(f"Grid image saved to {output_image_path}")
    
        # Check if the grid image is smaller than the canvas size
        if grid_image.size[0] < canvas_size[0] or grid_image.size[1] < canvas_size[1]:
            # Center the grid image on a larger canvas
            centered_image = center_image_on_canvas(output_image_path, output_image_path, canvas_size)
        else:
            # If it's too large, scale it down
            scaled_image = scale_image(grid_image, canvas_size)
            scaled_image.save(output_image_path, format='PNG')
            logging.info(f"Scaled image saved to {output_image_path}")
