from . import Module

def printDict(var, deep = 0):
    if type(var) is dict:
        if (len(var) != 0):
            for k, v in var.items():
                print('\n' + "    "*deep + ("└ " if deep != 0 else "") + f"{k}: ", end='')
                printDict(v, deep+1)
        else:
            print(f" empty dict", end='')
    else :
        print(f" {var}", end='')
       
def print2DList(map:list, pStr=False):
    print('\n')
    for row in map:
        for v in row:
            if (pStr):
                print(f"{v if type(v) is str else '·'} ", end = '')
            else:
                print(f"{v if v!=10**9 else '_'} ", end = '')
        print("")
'''        
def printModule(module:Module.Module):
    prt = 'name: ' + module.name
    
    prt += 'port:\n'
    for p in module.ports: prt += f'{p.id}. ({'input' if p.isInput else 'output'}){p.name}[{p.bitWidth-1}:0]\n'
    
    pot += 'submodules:\n'
    for i, s in enumerate(module.submodule): prt += f'{i}. {s.name}\n'
'''