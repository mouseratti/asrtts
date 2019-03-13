from distutils.core import setup
from setuptools import find_packages
from datetime import datetime
setup(
    name='s_o',
    version='0.0.1_{}'.format(datetime.now()),
    packages=find_packages(where="src/"),
    package_dir={'s_o': 'src/s_o'},
    url='santehnika-online.ru',
    license='',
    author='mkoshel',
    author_email='mouseratti@gmail.com',
    description=''
)
