A simple image manipulation library aiming to make common image/photo
manipulation tasks easy. This library is still under development,
API may also change at any time.

Requires PIL/Pillow.

Example usage::

    from da_vinci import Image

    image = Image('lena.jpg')
    image.flip('horizontal')
    image.resize(width=10, height=10)
    image.save()

    # Opening an image from URL, rotating and change it's format
    image = Image('http://stamps.co.id/static/merchants/img/logo.png')
    image.rotate(degrees=90)
    image.set(format='jpg', quality=85)
    image.save() # Creates a file logo.jpg

    # Manipulating saturation, brightness, contrast and sharpness
    # Accepts values range from -100 (decrease) to 100 (increase)
    image.adjust(saturation=-100)
    image.adjust(brightness=-75, contrast=50, sharpness=-20)


If you need more extensive manipulation, an escape hatch to PIL
is also available::

    image = image.from_file('a.jpg')
    pil_image = image.get_pil_image()
    # Do whatever you need to do with the pil image
    # And if you want to convert this back to a da_vinci image
    image.set_pil_image(pil_image)

Tests

To run tests::

    python -m unittest tests

Changelog
---------

Version 0.4.0
=============
* Support Pillow 10
* Preserve EXIF data when image is rotated

Version 0.3.0
=============
* Added webp extension support

Version 0.2.2
=============
* Added bmp extension support