from setuptools import setup

setup(
    name="psman",
    packages=["psman"],
    version="1.1.0.0",
    description="Toolbox for process manipulating",
    author="Chesham",
    author_email="c.moweb@gmail.com",
    url="https://github.com/Chesham/psman",
    keywords=["os", "process", "utility"],
    classifiers=[],
    install_requires=["psutil>=5.9.2"],
    python_requires=">=3.10",
    entry_points={
        "console_scripts": ["psman = psman:main"]
    },
)
