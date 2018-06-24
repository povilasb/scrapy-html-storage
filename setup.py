from setuptools import setup

setup(
    name='scrapy-html-storage',
    version='0.4.0',
    description='Scrapy downloader middleware that stores response HTML files to disk.',
    long_description=open('README.rst').read(),
    url='https://github.com/povilasb/scrapy-html-storage',
    author='Povilas Balciunas',
    author_email='balciunas90@gmail.com',
    license='MIT',
    packages=['scrapy_html_storage'],
    zip_safe=False
)
