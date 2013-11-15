A simple image manipulation library built on top of PIL/Pillow aiming to
make common tasks easy. This library is still under heavy development,
API may also change at any time. Use at your own risk.

Requires PIL/Pillow.

Example usage::

    from da_vinci import images

    image = image.from_file('a.jpg')
    image.flip('horizontal')
    image.resize(width=10, height=10)
    image.save()

    # Opening an image from URL
    image = images.from_url('http://stamps.co.id/static/merchants/img/logo.png')
    image.rotate(degrees=90)
    image.save('b.png')

Tests

To run tests::

    python -m unittest tests