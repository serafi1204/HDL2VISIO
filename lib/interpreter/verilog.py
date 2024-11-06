from . import ModuleReader
from ..Module import Module

class VerilogInterpreter(ModuleReader):
    def __init__(self):
        self.extension = 'v'
        self.lib = {}
        self.sources = {}

    def skip(self, source, i, key=' '):
        while (i < len(source)-3):
            if (source[i:i+2] == '/*'):
                i += 2
                while (source[i-1:i+1] != '*/'):
                    i += 1
                i += 1
                continue
            elif (source[i:i+2] == '//'):
                i += 1
                while (source[i] != '\n'):
                    i += 1
                i += 1
                continue
            elif (source[i] in ['\n', ' ', '\t', key]):
                i += 1
                continue

            break
        
        return i

    def getTitle(self, source, i=0):
        stack = ''

        while (i < len(source)):
            i = self.skip(source, i)
            c = source[i]

            if (stack == "module"): stack = ""
            if (c == '#' or c == '('):
                return i, stack

            stack += c
            i += 1

        return i, 'untitled'
    
    def getParameter(self, source, i):
        if (source[i] != '#'): return i, {}

        stack = ''
        paraName = ''
        paras = {}

        i -= 1
        while (i < len(source)):
            i = self.skip(source, i+1)
            c = source[i]

            if (stack in ['#','(', "parameter"]):
                stack = ''
                i -= 1 
                continue
            if (c == '='):
                paraName = stack
                stack = ''
                continue
            if (c == ',' or c == ')'):
                paras[paraName] = stack
                stack = ''
                if (c == ')'): 
                    i += 1
                    break
                else : continue

            stack += c


        return i, paras

    def getPort(self, source, i):
        stack = ''
        ports = {}
        portType = ''
        portWidthLeft = '0'
        portWidthRight = '0'

        i -= 1
        while (i < len(source)):
            i = self.skip(source, i+1)
            c = source[i]

            if (stack == "("): 
                stack = ''
                i -= 1
                continue
            if (stack in ['input', 'output'] and source[i-1] in [" ", '\t']):
                portWidthLeft = '0'
                portWidthRight = '0'
                portType = stack
                stack = ''
                i -= 1
                continue

            if (stack in ['signed', 'unsigned', 'wire', 'reg'] and source[i-1] in [" ", '\t']):
                stack = ''
                i -= 1
                continue

            if (c == '['):
                stack = ''
                i += 1
                while (source[i] != ':'):
                    stack += source[i]
                    i += 1
                portWidthLeft = stack

                stack = ''
                i += 1
                while (source[i] != ']'):
                    stack += source[i]
                    i += 1
                portWidthRight = stack
                
                stack = ''
                continue

            if (c == ',' or c == ')'):
                ports[stack] = [portType, portWidthLeft, portWidthRight]
                stack = ''

                if (c == ')'): 
                    while (source[i] != ';'):
                        i += 1
                    i += 1
                    break
                else : continue

            stack += c

        return i, ports

    def nextWord(self, source, i):
        temp = i
        while (source[i] not in [' ', '\n', '(', ')', ',']):
            i += 1

        return i, source[temp:i]
    
    def nextTO(self, key, source, i):
        while (source[i] not in list(key)):
            i += 1
        
        return i+1

    def getInnerParameter(self, source, i, base, key = '#'):
        if (source[i] != key): return i, base

        stack = ''
        paraName = ''
        index = 0

        i -= 1
        while (i < len(source)-1):
            if (source[i+1] == ';') : break
            i = self.skip(source, i+1)
            c = source[i]

            if (stack in ['#','(']):
                stack = '' 
                i -= 1
                continue
            if (c == '.'):
                i += 1
                ii=i
                i = self.nextTO('(', source, i)
                paraName = source[ii:i-1]
                ii = i
                i = self.nextTO(')', source, i)
                value = source[ii:i]
                i = self.nextTO(',)', source, i)
                
                i-=1
                base[paraName] = value
                continue

            if (c == ',' or c == ')'):
                base[list(base.keys())[index]] = stack
                index += 1
                stack = ''
                if (c == ')'): 
                    i += 1
                    break
                else : continue

            stack += c

        return i, base

    def getInnerModules(self, source, i):
        stack = ''
        inner = {}

        i -= 1
        while (i < len(source)-1):
            if (source[i+1] in [' ', '\n', ';', '\t']):
                stack = ''
                i += 1
                continue
            else: 
                i = self.skip(source, i+1)
                if (i == -1): break
            stack += source[i]

            if (stack not in self.lib.keys()): 
                continue
            if (source[i+1] not in [" ", '(']):
                continue

            module = stack
            stack = ''

            i -= 1
            i = self.skip(source, i+1)
            i, paras = self.getInnerParameter(source, i, {key:'' for key in self.lib[module]['paras']})

            
            i = self.skip(source, i+1)
            while (source[i] != '('):
                stack += source[i]
                i = self.skip(source, i+1)
            title = stack

            i = self.skip(source, i)
            i, ports = self.getInnerParameter(source, i, {key:'' for key in self.lib[module]['ports']}, '(')
            for k, v in ports.items():
                ports[k] = v[:v.find('[')]
            
            inner[title] = {}
            inner[title]['title'] = title
            inner[title]['module'] = module
            inner[title]['paras'] = paras
            inner[title]['ports'] = ports

        return inner

    def interpreter(self, sources):
        for s in sources: 
            i, title = self.getTitle(s)
            i, paras = self.getParameter(s, i)
            i, ports = self.getPort(s, i)
            
            self.sources[title] = s[i:]
            self.lib[title] = {}
            self.lib[title]['title'] = title
            self.lib[title]['paras'] = paras
            self.lib[title]['ports'] = ports
        
        keys = self.sources.keys()
        for moduleName in keys:
            innerModules = self.getInnerModules(self.sources[moduleName], 0)
            self.lib[moduleName]['innerModules'] = innerModules


        cnt = {}
        for moduleName in keys:
            cnt[moduleName] = 0
        for moduleName in keys:
            for innerModule in self.lib[moduleName]['innerModules']:
                cnt[innerModule] += 1
        for moduleName in keys:
            self.lib[moduleName]['isRoot'] = True if (cnt[moduleName] == 0) else False

        return self.lib


# vi = VerilogInterpreter()
# mr = ModuleReader(vi)
# prtVar.prt(mr.read('example base code/verilog/FFT'))

