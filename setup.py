from setuptools import setup

setup(
    name='map_stitcher',
    description='Download and stitch tiles from Google Maps into one large image',
    version='1.2.0',
    packages=['map_stitcher'],
    install_requires=[
        'gevent==1.0.2',
        'greenlet==0.4.7',
        'grequests==0.3.0',
        'Pillow==2.8.2',
        'requests==2.7.0',
        'wheel==0.24.0',
        'progress==1.2',
    ],
    entry_points={
        'console_scripts': [
            'map_stitcher=map_stitcher.main:main',
        ]
    },
)
