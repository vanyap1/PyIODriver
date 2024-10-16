from threading import Thread
from smbus2 import SMBus, i2c_msg
import time

    
class IO:
    def __init__(self, boardNum: int, portNum: int, pinNum: int, pinDir: int):
        self.boardNum = boardNum
        self.portNum = portNum
        self.pinNum = pinNum
        self.pinDir = pinNum

class DIR:
    OUTPUT: int = 1
    INPUT: int = 0 

class BOARD:
    PF575 = [0x27,"PF575"]
    PCF8574 = [0x27,"PCF8574"]

    def __init__(self, boardType):
        self.addr = boardType[0]
        self.type = boardType[1]

class I2CConfig:
    def __init__(self, i2c_address, controller_type):
        self.i2c_address = i2c_address
        self.controller_type = controller_type

class I2CGPIOController(Thread):
    def __init__(self, i2c_config, i2c_bus):
        self.bus = SMBus(i2c_bus)
        self.i2c_address = i2c_config.i2c_address
        self.controller_type = i2c_config.controller_type
        self.portStatus = [0 , 0]
        Thread.__init__(self)
        self.daemon = True
        self.start()

    def pinInit(self, io: IO, initState: bool):
        self.pinWrite(io, initState)
        return True
    
    """
    Writing new pin value
    Eneble pull up if pin configuret as input or logic level when output
    """
    def pinWrite(self, io: IO, value: bool):
        if value not in (0, 1):
            raise ValueError("Value must be either 0 or 1")        
        if value == 1:
            self.portStatus[io.portNum] |= (1 << io.pinNum) 
        else:
            self.portStatus[io.portNum] &= ~(1 << io.pinNum)

    """
    Get current pin logic level 
    """
    def pinRead(self, io: IO):
        return self.portStatus[io.portNum] & (1 << io.pinNum)

    """
    Reset all accessible registers in the board
    """
    def resetBoard(self):
        for i in range(0, len(self.portStatus)):
            self.portStatus[i] = 0
        
    def run(self):
        while(True):
            if self.controller_type == "PF575":
                #self.bus.write_byte_data(self.i2c_address, self.portStatus[0], self.portStatus[1])
                write = i2c_msg.write(self.i2c_address, self.portStatus)
                self.bus.i2c_rdwr(write)
                #print(f"{self.controller_type}, port {self.portStatus[0]}, {self.portStatus[1]}, {self.i2c_address}, {self.controller_type}")
            elif self.controller_type == "PCF8574":
                print(f"{self.controller_type}, port {self.portStatus[0]}, {self.portStatus[1]}, {self.i2c_address}, {self.controller_type}")
            else:
                print("Undefined board")
           
            time.sleep(.1)
             



