from setuptools import setup, find_packages

with open('./README.md') as f:
    txt = f.read()


setup(
    name='koutils',
    version='0.0.4',
    description='A common file operation utility',
    long_description=txt,
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
    python_requires='>=2.7',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'koutils = koutils.cli:main',
        ],
    }
)