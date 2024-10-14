from i2c_gpio import I2CConfig, I2CGPIOController, IO, DIR, BOARD
import time

switches = [IO(boardNum = 0, portNum = 0, pinNum = 0, pinDir=DIR.OUTPUT),
    IO(boardNum = 0, portNum = 0, pinNum = 1, pinDir=DIR.OUTPUT),
    IO(boardNum = 0, portNum = 0, pinNum = 2, pinDir=DIR.OUTPUT),
    IO(boardNum = 0, portNum = 0, pinNum = 3, pinDir=DIR.OUTPUT)
]



if __name__ == '__main__':
    
    board = BOARD(BOARD.PF575)
    gpio_config = I2CConfig(i2c_address=board.addr, controller_type=board.type)
    gpio = I2CGPIOController(gpio_config)
    for switch in switches:
        print(switch.pinNum)
        gpio.pinInit(switch)
  
    
    #gpio.startService()
    
    muxVal = True
    while(True):
        gpio.pinWrite(switches[3], muxVal)
        if gpio.pinRead(switches[3]):
            print("MUX ON")
        else:
            print("MUX OF")
        
        muxVal = not muxVal
        time.sleep(0.5)
    
    
