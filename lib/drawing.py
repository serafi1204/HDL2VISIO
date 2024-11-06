from . import Module
from .visio import style, Shape, Visio, Page, Group, Line, makeGroup

# DrawBitLabel
# Draw label of wire.
def DrawBitLabel(page, pin, name:str, bitWidth:int, x:int, y:int, side:int, wireSize:float=1, offset:float=0.5):
    sideDot = -1 if (side == -1) else 0
    contents = f'{int(bitWidth)}b  ' if bitWidth != 1 else ''
    contents += name
    group = []
    
    w = max(5, len(contents)/5)
    h = style.fontSizeSub/10 + wireSize/4
    wireSize *= style.pinInterval*style.pt2mm
    
    if (bitWidth!=1):
        wire = Line(page)
        wire.staightLine(-wireSize, wireSize, wireSize, -wireSize)
        group.append(wire)
    
    label = Shape(page,Visio.masterRect)
    label.onlyText()
    label.pos(w/2-wireSize, h/2-wireSize)
    label.size(w, h)
    label.style(fontAlign=0, fontSize=style.fontSizeSub, colorFillClear=True, lineClear=True)
    label.visioObject.Characters.Text = contents
    group.append(label)
    
    w += wireSize/2
    group = Group(group)
    group.pos(x+sideDot*w+side*offset+wireSize, y)
    return group
    

def DrawBlock(page, baseModule:Module):
    maxN = max(baseModule.NportInput, baseModule.NportOutput)
    h = maxN+1
    w = style.h2w(h)
    
    # Body
    shape = Shape(page, Visio.masterRect)
    shape.size(w, h)
    shape.innerText(baseModule.name)
    shape.style(fontSize=style.fontSizeMain)
    
    # port
    for port in baseModule.ports:
        side = -1 if (port.isInput==True) else 1
        align = 0 if (port.isInput==True) else 2
        pinLoc = 3 if (port.isInput==True) else 1
        
        p = Shape(page, Visio.masterRect)
        p.size(w/2, h/maxN)
        p.pos(w/4 * side, h/2 - (port.n+1))
        p.onlyText()
        p.innerText(port.name)
        p.style(fontSize=style.fontSizeSub, fontAlign=align)
        
        shape.addPin(0 if (port.isInput==True) else 1, 1-1/h*(port.n+1))
        shape.children.append(p)
    
    group = makeGroup(shape.children+[shape])
    shape.children = []
    shape.visioObject = group
    
    return shape
    
def DrawModule(page, baseModule:Module, alartWindow = None, root = True):
    labelStack = []
    unconnectedWireStack = []
    # Draw submodules
    subModules = []
    for sub in baseModule.submodule:
        if (sub.checked == True):
            m, l, w = DrawModule(page, sub, alartWindow, root=False) 
            labelStack += l
            unconnectedWireStack += w
        else: 
            m = DrawBlock(page, sub) 
        subModules.append(m)
    
    # init
    maxN = max(baseModule.NportInput, baseModule.NportOutput)
    H = max([sub.h+sub.y/2 for sub in subModules]) - min([-sub.h/2+sub.y for sub in subModules])+4 if len(subModules) > 0 else 0
    W = max([sub.w+sub.x/2 for sub in subModules]) - min([-sub.w/2+sub.x for sub in subModules])+8 if len(subModules) > 0 else 0
    X = sum([sub.x for sub in subModules])/len(subModules) if len(subModules) > 0 else 0
    Y = sum([sub.y for sub in subModules])/len(subModules) if len(subModules) > 0 else 0
    h = max(maxN+1, H)
    w = max(style.h2w(h), W)
    
    # Body
    module = Shape(page, Visio.masterRect)
    module.size(w, h)
    module.style(fontSize=style.fontSizeMain, colorFillClear=True) 
    
    # Body title
    moduleTitle = Shape(page, Visio.masterRect)
    moduleTitle.size(w, style.fontSizeMain/10)
    moduleTitle.pos(0, h/2 + style.fontSizeMain/20)
    moduleTitle.onlyText()
    moduleTitle.innerText(baseModule.name)
    moduleTitle.style(fontSize=style.fontSizeMain, fontAlign=0)
    
    module.children.append(moduleTitle) # Append children for selecting
    module.pos(X, Y)
    module.children += subModules
    #Group([module, moduleTitle])
    
    # Add port pin
      
    for port in baseModule.ports:
        side = -1 if (port.isInput==True) else 1
        xRate = 0 if (port.isInput==True) else 1
        yRate = 1-1/h*(port.n+1)
        
        port.pin = module.addPin(xRate, yRate)
        
        if(root==True):
            labelStack.append((port, port.pin, side)) # Stack port for post porcessing
        
    # Connections
    wires = []
    wiresData = []
    modules = [module] + subModules
    for wire in baseModule.wires:
        beginModule = wire.begin[0]
        beginPort = wire.begin[1]
        
        for end in wire.end:
            endModule = end[0]
            endPort = end[1]
            
            ww = Line(page)
            ww.glueTo(modules[beginModule].pins[beginPort].visioObject, modules[endModule].pins[endPort].visioObject)
            
            wires.append(ww)
            wiresData.append((beginModule, beginPort, endModule, endPort))
            module.children.append(ww)  
    
    if (alartWindow() == -1): return 0
    ################################# post processing
    # Update recent position and size
    for sub in modules:
        sub.update()

    # wiring
    i = 0
    for wire in baseModule.wires:
        beginModule = wire.begin[0]
        beginPort = wire.begin[1]
        
        labelStack.append((wire, modules[beginModule].pins[beginPort], 1))
        
        if (len(wire.end) == 0):
            unconnectedWireStack.append((False, modules[beginModule].pins[beginPort], 5))
            
    # port
    wireLen = max([len(port.name)/2 for port in baseModule.ports])
    if (root == True):  
        for port in baseModule.ports:
            unconnectedWireStack.append((port.isInput, port.pin, wireLen))
            
    if (root == True):
        for t, pin, leng in unconnectedWireStack:
            ww = Line(page)
            
            if (t==True):
                ww.glueTo(end=pin.visioObject)
                ww.setBegin(pin.x-wireLen)
            else:
                ww.glueTo(begin=pin.visioObject)
                ww.setEnd(pin.x+wireLen)
                
        for port, pin, side in labelStack:
            p = DrawBitLabel(page, pin, port.name, port.bitWidth, pin.x, pin.y, side)
        
        return 0
    else:
        return module, labelStack, unconnectedWireStack