from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="hermes-notifier",
    version="1.2.0",
    author="Rafael Batista",
    author_email="raphab33@hotmail.com",
    description="Python/Django plugin for Hermes notifications system with SSE and push notification support",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/raphab3/plugin-hermes-notifier-python",
    project_urls={
        "Bug Reports": "https://github.com/raphab3/plugin-hermes-notifier-python/issues",
        "Source": "https://github.com/raphab3/plugin-hermes-notifier-python",
        "Documentation": "https://github.com/raphab3/plugin-hermes-notifier-python#readme",
        "Changelog": "https://github.com/raphab3/plugin-hermes-notifier-python/blob/main/CHANGELOG.md",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Framework :: Django",
        "Framework :: Django :: 3.2",
        "Framework :: Django :: 4.0",
        "Framework :: Django :: 4.1",
        "Framework :: Django :: 4.2",
        "Framework :: Django :: 5.0",
        "Topic :: Communications",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.25.0",
    ],
    extras_require={
        "django": [
            "Django>=3.2",
        ],
        "dev": [
            "pytest>=6.0",
            "pytest-django>=4.0",
            "black>=22.0",
            "flake8>=4.0",
            "mypy>=0.950",
            "python-dotenv>=0.19.0",
        ],
        "all": [
            "Django>=3.2",
            "python-dotenv>=0.19.0",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords="notifications, django, hermes, sse, real-time, push, fcm, apns, websocket",
)