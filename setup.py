from setuptools import setup

setup(name='sense-hat-graphics',
      version='0.0',
      description='Add graphics display options to the Sense Hat',
      url='https://github.com/PaleTomato/sense-hat-graphics',
      author='Patrick Leedham',
      author_email='ptl76@hotmail.co.uk',
      license='GPL-3.0',
      packages=['sense_graphics'],
      install_requires=[
          'sense_hat',
          'numpy'
      ])
