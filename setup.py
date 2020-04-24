import setuptools

with open("README.md") as readmeFile:
	longDescription = readmeFile.read()

setuptools.setup(
	name='coral_light',
	version='0.0',
	author='Robert Smiley',
	author_email='yarnoiser@gmail.com',
	description='Coral Data Visualization Tool',
	long_description=longDescription,
	long_description_content_type='text/markdown',
	url='https://github.com/rsmiles/CoralLight',
	classifiers=[
		'Programming Language :: Python :: 3',
		'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
		'Operating System :: OS Independent',
	],
	packages=setuptools.find_packages(),
	python3_requires='>=3.6',
	include_package_data=True,
)

