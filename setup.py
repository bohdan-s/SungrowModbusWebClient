import setuptools

exec(open('SungrowModbusWebClient/version.py').read())

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="SungrowModbusWebClient",
    version=__version__,
    author="Bohdan Flower",
    author_email="github@bohdan.net",
    description="A ModbusWebClient wrapper for talking to Sungrow WiNet-S Dongle via HTTP API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bohdan-s/SungrowModbusWebClient",
    packages=setuptools.find_packages(),
    install_requires=[
        'pymodbus>=2.3.0',
        'websocket-client>=1.2.1',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5.0',
)
