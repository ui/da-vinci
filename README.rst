A simple image manipulation library aiming to make common image/photo
manipulation tasks easy. This library is still under heavy development,
API may also change at any time. Use at your own risk.

Requires PIL/Pillow.

Example usage::

    from da_vinci import Image

    image = Image('lena.jpg')
    image.flip('horizontal')
    image.resize(width=10, height=10)
    image.quality = 65
    image.save()

    # Opening an image from URL, rotating and change it's format
    image = Image('http://stamps.co.id/static/merchants/img/logo.png')
    image.rotate(degrees=90)
    image.format = 'jpg'
    image.save() # Creates a file logo.jpg

If you need to do more extensive manipulation, an escape hatch to PIL
is also available::

    image = image.from_file('a.jpg')
    pil_image = image.get_pil_image()
    # Do whatever you need to do with the pil image
    # And if you want to convert this back to a da_vinci image
    image.set_pil_image(pil_image)

Tests

To run tests::

    python -m unittest tests