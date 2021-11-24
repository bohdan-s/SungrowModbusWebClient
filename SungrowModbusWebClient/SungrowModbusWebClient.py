from pymodbus.client.sync import BaseModbusClient
from pymodbus.transaction import ModbusSocketFramer, ModbusBinaryFramer
from pymodbus.factory import ClientDecoder
from pymodbus.exceptions import ConnectionException
from websocket import create_connection

import websocket
import requests
import logging
import json
import time

# --------------------------------------------------------------------------- #
# Modbus Web Client Transport Implementation for Sungrow WiNet-S Dongle
# Drop in replacement for ModbusTcpClient
# --------------------------------------------------------------------------- #

class SungrowModbusWebClient(BaseModbusClient):
    """ Implementation of a modbus over Sungrow HTTP client
    """

    # See: Appendix 6、Device Information
    model_codes = {
        "9264": "SG5.0RT",
        "9276": "SG7.0RT"
    }

    def __init__(self, host='127.0.0.1', port=8082,
        framer=ModbusSocketFramer, **kwargs):
        """ Initialize a client instance
        :param host: The host to connect to (default 127.0.0.1)
        :param port: The websocket port to connect to (default 8082)
        :param timeout: The timeout to use for this socket (default 5)
        :param framer: The modbus framer to use (default ModbusSocketFramer)
        .. note:: The host argument will accept ipv4 and ipv6 hosts
        """

        self.dev_host = host
        self.ws_port = port
        self.ws_socket = None
        self.timeout = kwargs.get('timeout',  '5')
        BaseModbusClient.__init__(self, framer(ClientDecoder(), self), **kwargs)
        
        self.ws_endpoint = "ws://" + str(self.dev_host) + ":" + str(self.ws_port) + "/ws/home/overview"
        self.ws_token = ""
        self.dev_type = ""
        self.dev_procotol = ""
        self.dev_code = ""

    def connect(self):
        """ Connect via WebSocket to Dongle, retrieve Device details and Token
        :returns: True if connection succeeded, False otherwise
        """
        
        if self.ws_token:
            return True
        
        self.ws_socket = create_connection(self.ws_endpoint)
        logging.debug("Connection to websocket server established: " + self.ws_endpoint)
        
        self.ws_socket.send(json.dumps({ "lang": "en_us", "token": self.ws_token, "service": "connect" }))
        result =  self.ws_socket.recv()
        payload_dict = json.loads(result)
        logging.debug(payload_dict)
        
        if payload_dict['result_msg'] == 'success':
            self.ws_token = payload_dict['result_data']['token']
            logging.info("Token Retrieved: " + self.ws_token)
        else:
            self.ws_token = ""
            logging.info("Connection Failed", payload_dict['result_msg'] )
            raise ConnectionException(self.__str__())
        
        logging.info("Requesting Device Information")
        self.ws_socket.send(json.dumps({ "lang": "en_us", "token": self.ws_token, "service": "runtime" }))
        result =  self.ws_socket.recv()
        payload_dict = json.loads(result)
        logging.debug(payload_dict)
        
        if payload_dict['result_msg'] == 'success':
            # Device Type, 21 = Inverter?
            self.dev_type = payload_dict['result_data']['list'][0]['dev_type']      
            # Device model, see Appendix 6            
            self.dev_code = next(s for s in self.model_codes if self.model_codes[s] == payload_dict['result_data']['list'][0]['dev_model'])
            logging.info("Retrieved: dev_type = " + str(self.dev_type) + ", dev_code = " + str(self.dev_code))
        else:
            logging.info("Connection Failed", payload_dict['result_msg'] )
            raise ConnectionException(self.__str__())
        
        return self.ws_socket is not None

    def close(self):
        """ We dont really have a connection, so we just invalidate the token
        """
        return self.ws_socket is None

    def _send(self, request):
        """ Sends data on the underlying socket
        :param request: The encoded request to send
        :return: The number of bytes written
        """
        
        self.header = request
        
        """ param_type should be:
            0 = 4x read-only 
            1 = 3x holding 
        """
        if str(request[7]) == '4':
            param_type=0
        elif str(request[7]) == '3':
            param_type=1
        
        address = (256*request[8]+request[9]) + 1
        count = 256*request[10]+request[11]
        dev_id = str(request[6])
        
        logging.info("param_type: " + str(param_type) + ", start_address: " + str(address) + ", count: " + str(count) + ", dev_id: " +str(dev_id))       
        
        logging.debug(f'Calling: http://{str(self.dev_host)}/device/getParam?dev_id={dev_id}&dev_type={str(self.dev_type)}&dev_code={str(self.dev_code)}&type=3&param_addr={address}&param_num={count}&param_type={str(param_type)}&token={self.ws_token}&lang=en_us&time123456={str(int(time.time()))}')
        r =requests.get(f'http://{str(self.dev_host)}/device/getParam?dev_id={dev_id}&dev_type={str(self.dev_type)}&dev_code={str(self.dev_code)}&type=3&param_addr={address}&param_num={count}&param_type={str(param_type)}&token={self.ws_token}&lang=en_us&time123456={str(int(time.time()))}')

        if str(r.status_code) == '200':
            logging.info("Connection Sucsessful: Status code - " + str(r.status_code))
            self.payload_dict = json.loads(str(r.text))
            logging.debug("Payload Dict: " + str(self.payload_dict))
            modbus_data = self.payload_dict['result_data']['param_value'].split(' ')
            modbus_data.pop() # remove null on the end
            data_len = int(len(modbus_data) + 3) # length of data + header
            logging.info("Data length: " + str(data_len))
            self.payload_modbus = ['00', format(request[1], '02x'), '00', '00', '00', format(data_len, '02x'), format(request[6], '02x'), format(request[7], '02x'), format(int(len(modbus_data)), '02x')]
            self.payload_modbus.extend(modbus_data)
            logging.debug("Modbus Header: " + str(self.payload_modbus))
            logging.debug("Modbus Data: " + str(modbus_data))
            #logging.debug("Modbus RTU: " + str(self.payload_modbus))
            return self.payload_modbus

        else:
            logging.info("Connection Failed: Status code - " + str(r.status_code))
            self.ws_token = ""
            return None
        
        if not self.ws_socket:
            raise ConnectionException(self.__str__())
        if self.state == ModbusTransactionState.RETRYING:
            data = self._check_read_buffer()
            if data:
                return data

        if request:
            return self.ws_socket.send(request)
        return 0

    def _recv(self, size):
        """ This doesn't actually recieve any data.
            This will process the data already returned in the HTTP response in _send()
        """

        if not self.payload_modbus:
            raise ConnectionException(self.__str__())

        # If size isn't specified read up to 4096 bytes at a time.
        if size is None:
            recv_size = 4096
        else:
            recv_size = size

        data = []
        counter = 0
        time_ = time.time()

        logging.debug("Modbus payload: " + str(self.payload_modbus))

        for temp_byte in self.payload_modbus:
            if temp_byte:
                data.append(bytes.fromhex(temp_byte))
                time_ = time.time()
                
            counter+=1            
            if counter == recv_size:
                break
        
        # remove the data from the existing payload (pyModbus retrieves 8 byte header first, then data)
        del self.payload_modbus[0:counter]

        logging.info("Requested Size: " + str(size) + ", Returned Size: " + str(counter))
        logging.debug("Returned Data: " + str(data))

        if  int(counter) < int(size):
            return self._handle_abrupt_socket_close(size, data, time.time() - time_)

        return b"".join(data)

    def is_socket_open(self):
        return True if self.ws_socket is not None else False

    def __str__(self):
        """ Builds a string representation of the connection
        :returns: The string representation
        """
        return "SungrowModbusWebClient(%s:%s)" % (self.dev_host, self.ws_port)

    def __repr__(self):
        return (
            "<{} at {} socket={self.ws_socket}, ipaddr={self.dev_host}, "
            "port={self.ws_port}, timeout={self.timeout}>"
        ).format(self.__class__.__name__, hex(id(self)), self=self)