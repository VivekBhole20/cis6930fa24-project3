from setuptools import setup, find_packages

setup(
	name='project3',
	version='1.0',
	author='Vivek Jitendra Bhole',
	author_email='vbhole@ufl.edu',
	packages=find_packages(exclude=('tests', 'docs', 'resources')),
	setup_requires=['pytest-runner'],
	tests_require=['pytest']
)