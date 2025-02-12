from setuptools import setup, find_packages

setup(
    name='local-web-fileshare',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'Flask>=2.2.0'
    ],
    entry_points={
        'console_scripts': [
            'file-share=file_server.server:main',
        ],
    },
    description='A simple Python-based file-sharing server with a web UI',
    author='Your Name',
    author_email='your_email@example.com',
    url='https://github.com/yourname/local-web-fileshare',  # Optional
)
