"""
FutureReady-KB 安装配置
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="futureready-kb",
    version="0.1.0",
    author="FutureReady-KB Team",
    author_email="contact@futureready-kb.dev",
    description="企业知识基础设施，为下一代 AI Agent 准备",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/FutureReady-KB",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.9",
    install_requires=[
        "numpy>=1.24.0",
        "pandas>=2.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.12.0",
            "mypy>=1.8.0",
        ],
        "full": [
            "openai>=1.0.0",
            "anthropic>=0.18.0",
            "PyPDF2>=3.0.0",
            "python-docx>=1.0.0",
            "openpyxl>=3.1.0",
            "beautifulsoup4>=4.12.0",
            "fastapi>=0.109.0",
            "uvicorn>=0.27.0",
        ],
    },
)
