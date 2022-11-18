from setuptools import setup, find_packages

with open('./README.md') as f:
    txt = f.read()

setup(name='kfutils',
      version='0.0.8',
      description='A common file operation utility',
      long_description=txt,
      author='Koushik Naskar',
      author_email='koushik.naskar9@gmail.com',
      license="MIT",
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Environment :: Console', 'Intended Audience :: Science/Research',
          'Natural Language :: English',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: Implementation :: CPython',
          'Topic :: System :: Shells'
      ],
      keywords='File Operations',
      project_urls={'Source Code': 'https://github.com/Koushikphy/kutils'},
      zip_safe=True,
      python_requires='>=3.6',
      packages=find_packages(),
    extras_require={
        'csaps':  ["csaps"],
        'tabulate':  ["tabulate"]
    },
      entry_points={
          'console_scripts': [
              'kfutils = kfutils.cli:main',
          ],
      })
