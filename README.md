# SungrowModbusWebClient
 Access Modbus RTU via API call to Sungrow WiNet-S

Class based on pymodbus.ModbusTcpClient, completely interchangeable, just replace ModbusTcpClient() with SungrowModbusTcpClient()

Install: pip install SungrowModbusWebClient

Example:
For Solariot, open solariot.py

Add to the top: from SungrowModbusWebClient import SungrowModbusWebClient

Replace SungrowModbusTcpClient with SungrowModbusWebClient near lines 100 & 101