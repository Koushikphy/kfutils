import os
from setuptools import setup




setup(
    name='kutils',
    version='0.0.1',
    description='Installer for the ADT_Program_Package.',
    author='Koushik Naskar',
    author_email='koushik.naskar9@gmail.com',
    license = "MIT",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: Implementation :: CPython'
    ],
    keywords='File Operations',
    project_urls={'Source Code':'https://github.com/Koushikphy/kutils'},
    zip_safe=True,
    # install_requires=['numpy >=1.13.0'],
    extras_require={
        'h5':  ["h5py"]
    },
    python_requires='>=2.7',
    entry_points={
        'console_scripts': [
            'futils = src.futils:main',
        ],
    }
)