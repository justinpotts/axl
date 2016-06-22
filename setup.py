from setuptools import setup

setup(name='axl',
      version='0.2',
      description='Python package that generates web extensions for Firefox',
      url='http://github.com/justinpotts/axl',
      author='Justin Potts',
      author_email='justin@garblemasher.com',
      license='MPL',
      packages=['axl'],
      zip_safe=False,
      entry_points="""
        [console_scripts]
        axl = axl.axl:cli
    """)
