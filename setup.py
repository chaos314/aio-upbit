from setuptools import setup

dependencies = [
    'aiohttp',
    'pyjwt'
]

version = '1.0.0'

setup(name='aioupbit',
      version=version,
      packages=['aioupbit'],
      description='Asynchronous wrapper for the Upbit API',
      url='https://github.com/chaos314/aio-upbit',
      author='Seokhwan Cheon',
      author_email='chaos314@gmail.com',
      license='MIT',
      install_requires=dependencies,
      keywords=['upbit', 'crypto', 'bitcoin'],
      classifiers=[
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 3.6',
          'Topic :: Office/Business :: Financial',
      ],
)
