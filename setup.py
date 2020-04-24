import setuptools
import from app_info import *

with open("README.md") as readmeFile:
	longDescription = readmeFile.read()

setuptools.setup(
	name=APP_NAME,
	version=APP_VERSION,
	author='Robert Smiley',
	author_email='yarnoiser@gmail.com',
	description='Coral Data Visualization Tool',
	long_description=longDescription,
	long_description_content_type='text/markdown',
	url=''
	classifiers=[
		'Programming Language :: Python :: 3',
		'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
		'Operating System :: OS Independent',
	],
	python3_requires='>=3.6'
)
