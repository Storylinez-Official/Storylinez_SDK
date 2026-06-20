from setuptools import setup, find_packages
from pathlib import Path

# Get the long description from the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

setup(
    name='storylinez',
    version='1.0.0',
    license="MIT",
    author='Sayanti Chatterjee, Ranit Bhowmick',
    author_email='sayantichatterjee28@gmail.com, mail@ranitbhowmick.com',
    description='Storylinez: A modular library for narrative generation and story manipulation',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages('src', include=["storylinez", "storylinez.*"]),
    package_dir={'': 'src'},
    url='https://github.com/Storylinez-Official/Storylinez_SDK',
    install_requires=[
        'python-dotenv',
        'ultraprint>=3.4.0',
    ],
    extras_require={
        # Optional MCP server: pip install "storylinez[mcp]"
        'mcp': ['mcp[cli]>=1.2.0'],
    },
    entry_points={
        'console_scripts': [
            'storylinez-mcp = storylinez.mcp.server:main',
        ],
    },
    python_requires='>=3.6',
)
