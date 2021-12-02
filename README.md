<div id="top"></div>

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![GPL3 License][license-shield]][license-url]

<br />
<div align="center">

<h2 align="center">SungrowModbusWebClient</h3>

  <p align="center">
    Drop in replacement for SungrowModbusTCPClient/ModbusTCPClient that uses Websockets and HTTP API requests to work around Sungrow disabling Modbus requests on WiNet-S Dongle. 
    <br />
    <br />
    <a href="https://github.com/bohdan-s/SungrowModbusWebClient/issues">Report Bug</a>
    ·
    <a href="https://github.com/bohdan-s/SungrowModbusWebClient/issues">Request Feature</a>
  </p>
</div>

<!-- ABOUT THE PROJECT -->
## About The Project
Access Modbus RTU via HTTP API call to Sungrow WiNet-S. 

This uses HTTP requests to retrieve Modbus packets, add a header and then pass to PyModbus to parse like a standard Modbus RTU message

Class based on pymodbus.ModbusTcpClient, completely interchangeable, just replace ModbusTcpClient() or SungrowModbusTcpClient() with SungrowModbusTcpClient()

<p align="right">(<a href="#top">back to top</a>)</p>

### Built With

* [Python3](https://www.python.org/)

### Requires
* [pymodbus>=2.4.0](https://pypi.org/project/pymodbus/)
* [websocket-client>=1.2.1](https://pypi.org/project/websocket-client/)

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

Install via PIP, then if replace ModbusTcpClient() or SungrowModbusTcpClient() with SungrowModbusWebClient()

### Installation

1. Install with PIP
   ```sh
   pip install SungrowModbusWebClient
   ```

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

For Solariot, open solariot.py

Add to the top: from SungrowModbusWebClient import SungrowModbusWebClient

Replace SungrowModbusTcpClient with SungrowModbusWebClient near lines 100 & 101

<p align="right">(<a href="#top">back to top</a>)</p>


## Tested
* SG7.0RT with WiNet-S Dongle

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- LICENSE -->
## License

Distributed under the GPL3 License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- CONTACT -->
## Contact

Project Link: [https://github.com/bohdan-s/SungrowModbusWebClient](https://github.com/bohdan-s/SungrowModbusWebClient)

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [solariot](https://github.com/meltaxa/solariot)
* [Sungrow-Modbus](https://github.com/rpvelloso/Sungrow-Modbus)
* [modbus4mqtt](https://github.com/tjhowse/modbus4mqtt)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/bohdan-s/SungrowModbusWebClient.svg?style=for-the-badge
[contributors-url]: https://github.com/bohdan-s/SungrowModbusWebClient/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/bohdan-s/SungrowModbusWebClient.svg?style=for-the-badge
[forks-url]: https://github.com/bohdan-s/SungrowModbusWebClient/network/members
[stars-shield]: https://img.shields.io/github/stars/bohdan-s/SungrowModbusWebClient.svg?style=for-the-badge
[stars-url]: https://github.com/bohdan-s/SungrowModbusWebClient/stargazers
[issues-shield]: https://img.shields.io/github/issues/bohdan-s/SungrowModbusWebClient.svg?style=for-the-badge
[issues-url]: https://github.com/bohdan-s/SungrowModbusWebClient/issues
[license-shield]: https://img.shields.io/github/license/bohdan-s/SungrowModbusWebClient.svg?style=for-the-badge
[license-url]: https://github.com/bohdan-s/SungrowModbusWebClient/blob/main/LICENSE.txt