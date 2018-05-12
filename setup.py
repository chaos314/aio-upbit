from setuptools import setup

dependencies = [
    'aiohttp',
    'pyjwt'
]

version = '0.9.1'

setup(name='aio-upbit',
      version=version,
      packages=['aioupbit'],
      description='Python wrapper for the Upbit API',
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
          'Programming Language :: Python',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Development Status :: 3 - Alpha',
          'Topic :: Office/Business :: Financial',
      ],
)
