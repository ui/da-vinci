from __future__ import division


def calculate_dimensions(width, height, original_width, original_height,
                         keep_aspect_ratio=True, method='stretch'):
    if method not in ('stretch', 'fit', 'fill'):
        raise ValueError('Method must be "stretch", "fit" or "fill".')

    if width is not None:
        width = parse_dimension(width, original_width)

    if height is not None:
        height = parse_dimension(height, original_height)

    # If only one of width/height is specified, calculate
    # width/height based on current aspect ratio
    aspect_ratio = original_width / original_height
    if width is not None and height is None:
        height = width / aspect_ratio
    elif width is None and height is not None:
        width = height * aspect_ratio

    if method == "stretch":
        return (int(width), int(height))

    potential_width = width
    potential_height = potential_width / aspect_ratio

    # "fit" method means fit the entire image into the desired dimension,
    # preserving aspect ratio and without cropping the image
    if method == 'fit':
        if (potential_width <= width) and (potential_height <= height):
            return (int(potential_width), int(potential_height))
        else:
            return (int(height * aspect_ratio), int(height))
    # "fill" resizes the image to cover the entire dimension.
    # Aspect ratio is preserved
    elif method == 'fill':
        if (potential_width >= width) and (potential_height >= height):
            return (int(potential_width), int(potential_height))
        else:
            return (int(height * aspect_ratio), int(height))


def parse_dimension(value, original_dimension):
    """
    Returns an int dimension value from a string input (in number or percent).
    """
    try:
        return int(value)
    except ValueError:
        if value.rfind('%'):
            return int(int(value.split('%')[0]) * original_dimension / 100)
        raise
