"""
Setup script for PDF to Excel Converter.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README file
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

# Read requirements
requirements_file = Path(__file__).parent / "requirements.txt"
if requirements_file.exists():
    with open(requirements_file, 'r', encoding='utf-8') as f:
        requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]
else:
    requirements = [
        'pdfplumber>=0.10.0',
        'openpyxl>=3.1.2',
        'pandas>=2.1.0',
        'PyMuPDF>=1.23.14',
        'tabula-py>=2.8.2',
        'camelot-py[cv]>=0.11.0',
        'ttkbootstrap>=1.10.1',
        'pillow>=10.0.1',
        'python-bidi>=0.4.2',
        'unicodedata2>=15.1.0',
        'pathlib2>=2.3.7',
        'typing-extensions>=4.8.0',
    ]

setup(
    name="pdf-to-excel-converter",
    version="1.0.0",
    author="PDF to Excel Converter Team",
    author_email="",
    description="Convert PDF files to Excel format with Thai language support",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mymy3399/Dockerfile",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
        "Topic :: Office/Business",
        "Topic :: Text Processing",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "Natural Language :: English",
        "Natural Language :: Thai",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.3",
            "pytest-cov>=4.1.0",
            "black>=23.9.1",
            "flake8>=6.1.0",
        ],
        "test": [
            "pytest>=7.4.3",
            "pytest-cov>=4.1.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "pdf-to-excel=main:main",
            "pdf2excel=main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.txt", "*.md", "*.yml", "*.yaml"],
    },
    keywords=[
        "pdf", "excel", "converter", "thai", "language", 
        "spreadsheet", "table", "extraction", "automation"
    ],
    project_urls={
        "Bug Reports": "https://github.com/mymy3399/Dockerfile/issues",
        "Source": "https://github.com/mymy3399/Dockerfile",
        "Documentation": "https://github.com/mymy3399/Dockerfile/blob/main/README.md",
    },
)