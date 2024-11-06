class Port:
    def __init__(self, id:int, n:int, name:str, isInput:bool, bitWidth:int=0):
        self.id = id
        self.n = n
        self.name = name
        self.isInput = isInput
        self.bitWidth = bitWidth
        self.pin = None
        

class Wire:
    def __init__(self, name:str, bitwidth:int, begin:set, end:list):
        self.name = name
        self.bitWidth = bitwidth
        self.begin = begin
        self.end = end
        
class Module:    
    def __init__(self, name:str='untited'):
        self.ports = []
        self.wires = []
        self.NportInput = 0
        self.NportOutput = 0
        self.name = name
        self.submodule = []
        self.checked = False
        
    def addPort(self, isInput:bool, name:str, bitWidth:int=0):
        if (isInput):
            n = self.NportInput
            self.NportInput += 1
        else:
            n = self.NportOutput
            self.NportOutput += 1
            
        port = Port(len(self.ports), n, name, isInput, bitWidth)
        self.ports.append(port)
        
        return port
    
    def addWire(self, name:str, bitwidth:int, begin:set, end:list):
        wire = Wire(name, bitwidth, begin, end)
        self.wires.append(wire)
        
        return wire