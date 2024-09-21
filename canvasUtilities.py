import sys
from PIL import Image, ImageColor

def center_image_on_canvas(input_image_path, output_image_path, canvas_size=(4000, 4000)):
    """Centers an image on a transparent canvas of the specified size."""
    new_image = Image.new("RGBA", canvas_size, (0, 0, 0, 0))  # Fully transparent
    heatmap_image = Image.open(input_image_path)
    heatmap_width, heatmap_height = heatmap_image.size
    position = ((canvas_size[0] - heatmap_width) // 2, (canvas_size[1] - heatmap_height) // 2)
    new_image.paste(heatmap_image, position, heatmap_image)  # Use heatmap_image as mask for transparency
    new_image.save(output_image_path, format='PNG')  # Save the centered image
    return new_image  # Return the centered image

def scale_image(image, max_size):
    """Scales down an image to fit within the max size while maintaining aspect ratio."""
    image.thumbnail(max_size, Image.ANTIALIAS)
    return image  # Return the scaled image

def add_border(image, border_size=2, border_color=(255, 0, 0)):
    """Adds a border around the given image."""
    bordered_image = Image.new("RGBA", (image.width + border_size * 2, image.height + border_size * 2), border_color)
    bordered_image.paste(image, (border_size, border_size))  # Paste the original image in the center
    return bordered_image

def create_image_grid(image_paths, output_image_path, canvas_size=(4000, 4000), grid_size=(2, 2), border=None, border_size=2):
    """Arranges a list of images in a grid, saves the result, and checks dimensions."""
    
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

    # Adjust border size if needed
    if border_color is None or border_size == 0:
        border_size = 0
    
    # Load images and add borders if applicable
    if border_color:
        images = [add_border(Image.open(img), border_size, border_color) for img in image_paths]
    else:
        images = [Image.open(img) for img in image_paths]
    
    # Create a new image for the grid
    grid_width = sum(max(images[i + j * grid_size[0]].width for j in range(grid_size[1])) for i in range(grid_size[0]))
    grid_height = sum(max(images[i].height for i in range(j * grid_size[0], min((j + 1) * grid_size[0], len(images)) )) for j in range(grid_size[1]))

    grid_image = Image.new("RGBA", (grid_width, grid_height), (0, 0, 0, 0))  # Transparent background

    # Initialize offsets and heights
    y_offsets = [0] * grid_size[0]  # Track current height for each column

    for index, img in enumerate(images):
        col = index % grid_size[0]  # Determine the column
        row = index // grid_size[0]  # Determine the row

        # Determine the starting coordinates
        x_offset = col * (max(images[i].width for i in range(grid_size[0])) if col > 0 else 0)
        if row == 0:
            y_offset = 0  # First row starts at 0
        else:
            y_offset = y_offsets[col]  # Use the height of the tallest image in the column

        # Place the image
        grid_image.paste(img, (x_offset, y_offset))

        # Update the height tracker for the column
        y_offsets[col] += img.height

    # Save the grid image before checking size
    grid_image.save(output_image_path, format='PNG')
    print(f"Grid image saved to {output_image_path}")

    # Check if the grid image is smaller than the canvas size
    if grid_image.size[0] < canvas_size[0] or grid_image.size[1] < canvas_size[1]:
        # Center the grid image on a larger canvas
        centered_image = center_image_on_canvas(output_image_path, output_image_path, canvas_size)
    else:
        # If it's too large, scale it down
        scaled_image = scale_image(grid_image, canvas_size)
        scaled_image.save(output_image_path, format='PNG')
        print(f"Scaled image saved to {output_image_path}")
