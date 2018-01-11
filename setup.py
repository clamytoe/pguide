import os
from setuptools import setup, find_packages


# Utility function to read the README file.
# Used for the long_description.
#
# It's nice, because now
#   1) we have a top level README file and
#   2) it's easier to type in the README file than to put a raw string in below ...
def read(file_name):
    return open(os.path.join(os.path.dirname(__file__), file_name)).read()


requirements = read('requirements.txt').split()

setup(
    name="pguide",
    version="0.2.0",
    author="Martin Uribe",
    author_email="clamytoe@gmail.com",
    description="Parental Guide assistant for media on IMDb.",
    license="MIT",
    keywords="movie game show tv series parental guide assistant scrape",
    packages=find_packages(exclude=['test*', 'dist']),
    include_package_data=True,
    long_description=read('README.md'),
    url='github.com/clamytoe/pguide',
    classifiers=[
        "Development Status :: 1 - Alpha",
    ],
    install_requires=requirements,
    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'pytest-flake8'],
    entry_points={
        'console_scripts': ['pguide=pguide.pguide:main'],
    }
)
