from __future__ import division

import io
import os

from PIL import Image as PILImage
from PIL import ImageEnhance, ImageOps

from . import formats
from .compat import string_types, urlopen, urlparse
from .utils import (calculate_dimensions, convert_to_pil_factor,
                    get_box_dimensions, parse_dimension)


class Image(object):

    def __init__(self, path_or_url):
        """
        "filename" refers to image's file name on disk. If an image is opened
        from a URL, it doesn't have a filename until save() is called
        """
        if isinstance(path_or_url, string_types):
            result = urlparse(path_or_url)
        else:
            result = None
        # If we receive a URL, use urllib to open the image
        # else, assume it's a filename or file like object
        if result is not None and result.scheme in ('http', 'https'):
            file = io.BytesIO(urlopen(path_or_url).read())
            self._pil_image = PILImage.open(file)
            self.filename = None
            self.name = os.path.basename(path_or_url)
        else:
            self._pil_image = PILImage.open(path_or_url)
            self.filename = self._pil_image.filename if self._pil_image.filename else path_or_url.name
            self.name = os.path.basename(self.filename)

        self._format = self._pil_image.format
        self._pil_image = ImageOps.exif_transpose(self._pil_image)
        self._quality = None

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

    def _set_format(self, format):
        if isinstance(format, string_types):
            format = format.lower()
        self._format = formats.MAPPING[format]

    def _get_format(self):
        return self._format

    format = property(_get_format, _set_format)

    def _get_quality(self):
        return self._quality

    def _set_quality(self, quality):
        self._quality = quality

    quality = property(_get_quality, _set_quality)

    def set(self, format=None, quality=None):
        """Converts image to specified kwargs. Supports format and quality.

            image.set(format='jpg')
            image.set(quality=85)  # In percent
        """
        if format is not None:
            self._set_format(format)
        if quality is not None:
            self._set_quality(quality)

    def get_filename(self):
        """Generates a suitable filename based on image name and format."""
        name = self.filename or self.name
        filename, extension = os.path.splitext(name)
        return '%s.%s' % (filename, formats.EXTENSIONS[self.format])

    def show(self):
        """Displays the image, mainly for debugging purposes.
        This simply calls PIL's image.show()"""
        return self._pil_image.show()

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

    def save(self, filename=None, file=None):
        """Saves the image to disk. If image doesn't have a filename, it's
        assigned one.
        """
        if filename:
            self.filename = filename

        self.filename = self.get_filename()
        kwargs = {
            'format': self._format,
            'fp': file or self.filename,
        }
        if self.quality is not None:
            kwargs['quality'] = self.quality

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
        try:
            resample = PILImage.ANTIALIAS
        except AttributeError:
            resample = PILImage.LANCZOS

        self._pil_image = self._pil_image.resize(
            calculate_dimensions(width, height, self.width, self.height,
                                 method=method),
            resample=resample
        )

    def crop(self, width, height, center=('50%', '50%'),
             shape='rectangle'):
        center = (
            parse_dimension(center[0], self.width),
            parse_dimension(center[1], self.height)
        )
        self._pil_image = self._pil_image.crop(
            get_box_dimensions(
                width, height,
                self.width, self.height,
                center=center,
            )
        )

    def adjust(self, sharpness=0, brightness=0, saturation=0, contrast=0):
        """
        Adjusts image's sharpness, brightness, saturation (color in PIL)
        and contrast. Accepted scale is from -100 to 100. (0 means unchanged).
        """

        # Image will lose transparency info when saturation/contrast
        # is changed, see https://github.com/jdriscoll/django-imagekit/issues/64
        if saturation:
            enhancer = ImageEnhance.Color(self._pil_image)
            self._pil_image = enhancer.enhance(convert_to_pil_factor(saturation))
        
        if sharpness:
            enhancer = ImageEnhance.Sharpness(self._pil_image)
            self._pil_image = enhancer.enhance(convert_to_pil_factor(sharpness))
        
        if brightness:
            enhancer = ImageEnhance.Brightness(self._pil_image)
            self._pil_image = enhancer.enhance(convert_to_pil_factor(brightness))
        
        if contrast:
            enhancer = ImageEnhance.Contrast(self._pil_image)
            self._pil_image = enhancer.enhance(convert_to_pil_factor(contrast))


def from_file(path_or_file):
    """Returns an image from a given filename or file object."""
    return Image(path_or_file)


def from_url(url):
    """Returns an image from a URL e.g: http://example.com/food.jpg."""
    return Image(url)
