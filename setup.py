from setuptools import setup

setup(name='frozphonpy',
      version='0.1',
      description='Small package for setting up frozen-phonon calcs.',
      url='',
      author='Jonah B. Haber',
      author_email='',
      license='MIT',
      packages=['frozphonpy'],
      install_requires = ['phonopy', 'monty==1.0.4'], #, 'repo @ https://github.com/BerkeleyGW/BGWpy/tarball/master#egg=BGWpy'],
      dependency_links = ['git+https://github.com/BerkeleyGW/BGWpy/tarball/master#egg=BGWpy'],
      zip_safe=False)
