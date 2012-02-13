from setuptools import setup, find_packages

setup(
    name='VCSTodo',
    version='0.1',
    author='Kevin Samuel',
    author_email='kevin@yeleman.com',
    packages=find_packages(),
    license='GNU General Public License (GPL), Version 2',
    long_description=open('README.rst').read(),
    provides=['tdo'],
    description='Text based but human and VCS friendly task manager',
    url='http://github.com/yeleman/VCSTodo',
    keywords="task manager",
    include_package_data=True,
    scripts=['bin/tdo'],
    classifiers=[
        'Development Status :: 0.1',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GPL2',
        'Programming Language :: Python',
        'Operating System :: OS Independent',
    ],
)