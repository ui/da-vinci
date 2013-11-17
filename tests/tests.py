import os
import unittest

from da_vinci import images
from da_vinci.utils import calculate_dimensions, parse_dimension


class UtilsTest(unittest.TestCase):

    def test_calculate_dimensions_auto_width_height(self):
        """
        In this test we need to:
        1. Make sure proper image dimensions are generated
        2. Width/height returned are always in int
        """
        # Square original image
        kwargs = {
            'original_width': 10,
            'original_height': 10,
        }
        dimensions = calculate_dimensions(width=2, height=None, **kwargs)
        self.assertEqual(dimensions, (2, 2))
        self.assertIsInstance(dimensions[0], int)
        self.assertIsInstance(dimensions[1], int)
        
        dimensions = calculate_dimensions(width=None, height=2, **kwargs)
        self.assertEqual(dimensions, (2, 2))
        self.assertIsInstance(dimensions[0], int)
        self.assertIsInstance(dimensions[1], int)

        # Landscape original image
        kwargs = {
            'original_width': 20,
            'original_height': 10,
        }
        dimensions = calculate_dimensions(width=2, height=None, **kwargs)
        self.assertEqual(dimensions, (2, 1))
        self.assertIsInstance(dimensions[0], int)
        self.assertIsInstance(dimensions[1], int)

        dimensions = calculate_dimensions(width=None, height=2, **kwargs)
        self.assertEqual(dimensions, (4, 2))
        self.assertIsInstance(dimensions[0], int)
        self.assertIsInstance(dimensions[1], int)

        # Portrait original image
        kwargs = {
            'original_width': 10,
            'original_height': 20,
        }
        dimensions = calculate_dimensions(width=2, height=None, **kwargs)
        self.assertEqual(dimensions, (2, 4))
        self.assertIsInstance(dimensions[0], int)
        self.assertIsInstance(dimensions[1], int)
        
        dimensions = calculate_dimensions(width=None, height=2, **kwargs)
        self.assertEqual(dimensions, (1, 2))
        self.assertIsInstance(dimensions[0], int)
        self.assertIsInstance(dimensions[1], int)
    
    def test_calculate_dimensions_aspect_ratio(self):
        # Square original image
        kwargs = {
            'original_width': 10,
            'original_height': 10,
        }
        self.assertEqual(
            calculate_dimensions(2, 1, method='stretch', **kwargs),
            (2, 1)
        )
        self.assertEqual(
            calculate_dimensions(2, 1, method='fit', **kwargs),
            (1, 1)
        )
        self.assertEqual(
            calculate_dimensions(2, 1, method='fill', **kwargs),
            (2, 2)
        )

        # Landscape sized image
        kwargs = {
            'original_width': 20,
            'original_height': 10,
        }
        self.assertEqual(
            calculate_dimensions(1, 1, method='stretch', **kwargs),
            (1, 1)
        )
        self.assertEqual(
            calculate_dimensions(2, 2, method='fit', **kwargs),
            (2, 1)
        )
        self.assertEqual(
            calculate_dimensions(2, 4, method='fit', **kwargs),
            (2, 1)
        )
        self.assertEqual(
            calculate_dimensions(2, 2, method='fill', **kwargs),
            (4, 2)
        )
        self.assertEqual(
            calculate_dimensions(2, 4, method='fill', **kwargs),
            (8, 4)
        )

         # Portrait sized image
        kwargs = {
            'original_width': 10,
            'original_height': 20,
        }
        self.assertEqual(
            calculate_dimensions(1, 1, method='stretch', **kwargs),
            (1, 1)
        )
        self.assertEqual(
            calculate_dimensions(2, 2, method='fit', **kwargs),
            (1, 2)
        )
        self.assertEqual(
            calculate_dimensions(4, 2, method='fit', **kwargs),
            (1, 2)
        )
        self.assertEqual(
            calculate_dimensions(2, 2, method='fill', **kwargs),
            (2, 4)
        )
        self.assertEqual(
            calculate_dimensions(4, 2, method='fill', **kwargs),
            (4, 8)
        )

    def test_parse_dimension(self):
        self.assertEqual(parse_dimension(2, 10), 2)
        self.assertEqual(parse_dimension('2', 10), 2)
        self.assertEqual(parse_dimension('10%', 10), 1)


class ImageTest(unittest.TestCase):

    def test_saving_image_from_url(self):
        image = images.from_url('http://stamps.co.id/static/merchants/img/logo.png')
        self.assertEqual(image._format, 'PNG')
        image.save()
        os.remove(image.filename)

    def test_save(self):
        """
        Ensure that these works:
        - image.save(filename='alice.jpg')
        - image.filename = 'bob.jpg'; image.save()
        """
        image = images.from_file('tests/10x10.jpg')
        self.assertEqual(image._format, 'JPEG')
        new_filename = 'tests/save.jpg'
        image.save(new_filename)
        self.assertEqual(image.filename, new_filename)
        self.assertTrue(os.path.exists(new_filename))
        os.remove(new_filename)

        new_filename = 'tests/save2.jpg'
        image.filename = new_filename
        image.save()
        self.assertTrue(os.path.exists(new_filename))
        os.remove(new_filename)

    def test_rotate(self):
        image = images.from_file('tests/10x20.jpg')
        self.assertEqual(image.width, 10)
        self.assertEqual(image.height, 20)
        image.rotate(90)
        self.assertEqual(image.width, 20)
        self.assertEqual(image.height, 10)
        image.rotate(-90)
        self.assertEqual(image.width, 10)
        self.assertEqual(image.height, 20)

    def test_format_getter_setter(self):
        image = images.from_file('tests/10x20.jpg')
        image.format = 'JPG'
        self.assertEqual(image.format, 'JPEG')
        image.format = 'png'
        self.assertEqual(image.format, 'PNG')

    def test_get_filename(self):
        # get_filename return its original filename if there's no changes
        image = images.from_file('tests/10x20.jpg')
        self.assertEqual(image.get_filename(), 'tests/10x20.jpg')
        # get_filename returns the right filename if format is changed
        image.set_format('png')
        self.assertEqual(image.get_filename(), 'tests/10x20.png')
        # get_filename falls back to self.name 
        image.filename = None
        self.assertEqual(image.get_filename(), '10x20.png')
