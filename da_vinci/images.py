from __future__ import division

import io
import os
import urllib

from PIL import Image as PILImage

from .utils import calculate_dimensions, get_box_dimensions, parse_dimension


class Image(object):

    def __init__(self, path_or_file=None, url=None):
        """
        "filename" refers to image's file name on disk. If an image is opened
        from a URL, it doesn't have a filename until save() is called
        """
        if path_or_file is None and url is None:
            raise ValueError('"path_or_file" or "url" argument is needed')

        if path_or_file is not None:
            self._pil_image = PILImage.open(path_or_file)
            self.filename = self._pil_image.filename
            self.name = os.path.basename(self.filename)
        elif url is not None:
            file = io.BytesIO(urllib.urlopen(url).read())
            self._pil_image = PILImage.open(file)
            self.filename = None
            self.name = os.path.basename(url)
        self.format = self._pil_image.format

    @property
    def width(self):
        return self._pil_image.size[0]

    @property
    def height(self):
        return self._pil_image.size[1]

    @property
    def aspect_ratio(self):
        return self.width / self.height

    @property
    def info(self):  # Should this be renamed to metadata?
        return self._pil_image.info

    @property
    def mode(self):
        return self._pil_image.mode

    def get_pil_image(self):
        """Returns the underlying PIL image for more extensive manipulation."""
        return self._pil_image

    def set_pil_image(self, pil_image):
        self._pil_image = pil_image

    def flip(self, direction):
        """Flips an image, horizontally or vertically."""
        if direction == 'horizontal':
            self._pil_image = self._pil_image.transpose(PILImage.FLIP_LEFT_RIGHT)
        elif direction == 'vertical':
            self._pil_image = self._pil_image.transpose(PILImage.FLIP_TOP_BOTTOM)
        else:
            raise ValueError('Direction must be "horizontal" or "vertical"')

    def rotate(self, degrees):
        """Rotates image by specified number of degrees."""
        self._pil_image = self._pil_image.rotate(degrees)

    def save(self, filename=None, format=None, quality=None):
        """Saves the image to disk. If image doesn't have a filename, it's
        assigned one.
        """
        if filename is None:
            filename = self.filename or self.name
        self.filename = filename
        
        kwargs = {
            'format': format or self.format,
            'fp': filename,
        }
        if quality is not None:
            kwargs['quality'] = quality

        self._pil_image.save(**kwargs)

    # Should this accept percentages for width and height?
    def resize(self, width=None, height=None, method='stretch'):
        """Resizes image to specified width/height. Behavior depends on method:
        - "stretch" resizes the whole image to the specified dimension,
          regardless of aspect ratio
        - "fit" resizes image to the largest size such that both its width
          and height fit inside the specified dimension, keeps aspect ratio.
        - "fill" resizes image to be as large as possible so that the specified
          dimension is completely covered. Aspect ratio is preserved, parts of
          the image may not be within the specified dimension.
        """
        self._pil_image = self._pil_image.resize(
            calculate_dimensions(width, height, self.width, self.height, method),
            resample=PILImage.ANTIALIAS
        )

    def crop(self, width, height, center_offset=('50%', '50%'),
             shape='rectangle'):
        center_offset = (
            parse_dimension(center_offset[0], self.width),
            parse_dimension(center_offset[1], self.height)
        )
        self._pil_image = self._pil_image.crop(
            get_box_dimensions(
                width, height,
                self.width, self.height,
                center_offset=center_offset,
            )
        )


def from_file(path_or_file):
    """Returns an image from a given filename or file object."""
    return Image(path_or_file=path_or_file)


def from_url(url):
    """Returns an image from a URL e.g: http://example.com/food.jpg."""
    return Image(url=url)
