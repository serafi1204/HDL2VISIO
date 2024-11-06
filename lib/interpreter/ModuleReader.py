import os
import copy
from .. import Module, debug

class ModuleReader:
    def __init__(self):
        interpreter = None
        lib = {}
    
    def getFileList(self, filename):
        temp = filename.split('.')
        if (len(temp) == 1):
            for fname in os.listdir(filename):
                return [filename + '/' + fname for fname in os.listdir(filename) if (fname.split('.')[-1] == 'v')]
        elif (temp[-1] == self.extension):
            return [filename]
        else:
            print("Input a right path or filename.")
            return []


    def read(self, fileList):
        # Read file(folder)
        sources = [open(fname, 'r').read() for fname in fileList]
        
        # Run interpreter
        self.lib = self.interpreter(sources)
        debug.printDict(self.lib)
        # Get module from source
        modules = []
        for name, l in self.lib.items():
            if (l['isRoot'] == False): continue
            
            paras = {key: eval(value) for key, value in l['paras'].items()}
            module = self.getModule(name, l, paras)
            module.checked = True
            modules.append(module)
            
        return modules
    
    def eval(self, paras, eq):
        for para, value in paras.items():
            eq = eq.replace(para, value)
        
        return eval(eq)

    def getModule(self, name:str, base:dict, paras:dict={}):
        # Make Module
        module = Module.Module(name)
        
        paras = base['paras']
        
        # Port
        for name, p in base['ports'].items():
            module.addPort(
                p[0]=='input',
                name,
                abs(self.eval(paras, p[1])-self.eval(paras, p[2]))+1
            )
            
        # Submodules
        for moduleName, sub in base['innerModules'].items():
            # Update parameters
            subparas = copy.deepcopy(self.lib[sub['module']]['paras'])
            for k, v in sub['paras'].items():
                subparas[k] = v
            subparas = {key: self.eval(value) for key, value in sub['paras']}
            # Make Module
            module.submodule.append(self.getModule(sub['title'], self.lib[sub['module']], subparas))
            
        # Wire
        wires = {}
        for i, port in enumerate(module.ports):
            if (port.isInput == False): continue
            wires[port.name] = [(0, i), [], port.bitWidth]
        for i, (moduleName, sub) in enumerate(base['innerModules'].items()):
            for j, (port, wire) in enumerate(sub['ports'].items()):
                p = self.lib[moduleName]['ports'][port]
                if (p[0] == 'input'): continue
                wires[wire] = [(i+1, j), [], self.eval(paras, p[1])+1]
                
        for i, port in enumerate(module.ports):
            if (port.isInput == True): continue
            if (port.name not in wires.keys()): continue
            wires[port.name][1].append((0, i))  
        for i, (moduleName, sub) in enumerate(base['innerModules'].items()):
            name = sub['title']
            for j, (port, wire) in enumerate(sub['ports'].items()):
                if (self.lib[moduleName]['ports'][port][0] == 'output'): continue
                if (wire not in wires.keys()): continue
                wires[wire][1].append((i+1, j))
        
        for name, wire in wires.items():
            module.addWire(name, wire[2], wire[0], wire[1])
                    
        return module