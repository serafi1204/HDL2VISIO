from . import Visio
from . import style

class Pin:
    def __init__(self, visioObject):
        self.x = 0
        self.y = 0
        self.xRate = 0
        self.yRate = 0
        self.name = 'unnamed'
        self.bitwidth = 1
        self.isInput = False
        self.visioObject = visioObject
        
        
            
    def DrawBitLabel(self, name:str, bitWidth:int, x:int, y:int, side:int, wireSize:float=1, offset:float=0.5):
        sideDot = -1 if (side == -1) else 0
        contents = f'{int(bitWidth)}b  ' if bitWidth != 1 else ''
        contents += name
        group = []
        
        w = len(contents)/3.5
        h = style.fontSizeSub/10 + wireSize/4
        wireSize *= style.pinInterval*style.pt2mm
        
        if (bitWidth!=1):
            wire = Line(self.page)
            wire.staightLine(-wireSize, wireSize, wireSize, -wireSize)
            group.append(wire)
        
        label = Shape(self.page,Visio.masterRect)
        label.pos(w/2-wireSize, h/2-wireSize)
        label.size(w, h)
        label.style(fontAlign=0, fontSize=style.fontSizeSub, colorFillClear=True, lineClear=True)
        label.visioObject.Characters.Text = contents
        group.append(label)
        
        w += wireSize/2
        group = Group(group)
        group.pos(x+sideDot*w+side*offset+wireSize, y)
        return group
    
class Shape:
    def __init__(self, page, master):
        self.visioObject = page.Drop(master, 0, 0)
        self.style()
        self.shape = ''
        self.x, self.y = 0, 0
        self.w, self.h = 0, 0
        self.pins = []
        self.children = []
        
    def select(self, acc=False):
        if (acc == False): Visio.visapp.ActiveWindow.DeselectAll()
        
        Visio.visapp.ActiveWindow.Select(self.visioObject, Visio.constants.visSelect)
        for i in self.children:
            i.select(True)
    
    def onlyText(self):
        self.visioObject.TextStyle = "Normal"
        self.visioObject.LineStyle = "Text Only"
        self.visioObject.FillStyle = "Text Only"
        self.visioObject.CellsSRC(Visio.constants.visSectionObject, Visio.constants.visRowMisc, Visio.constants.visLOFlags).FormulaForceU = "1"
        self.visioObject.CellsSRC(Visio.constants.visSectionObject, Visio.constants.visRowShapeLayout, Visio.constants.visSLOPermY).FormulaForceU = "FALSE"
        self.visioObject.CellsSRC(Visio.constants.visSectionObject, Visio.constants.visRowShapeLayout, Visio.constants.visSLOPermeablePlace).FormulaForceU = "FALSE"
    
    def innerText(self, text):
        self.visioObject.Characters.Text = text
    
    def update(self):
        self.select()
        self.x = float(self.visioObject.Cells("PinX").Result(Visio.constants.visMillimeters))/style.pinInterval
        self.y = float(self.visioObject.Cells("PinY").Result(Visio.constants.visMillimeters))/style.pinInterval
        
        self.w = float(self.visioObject.CellsSRC(Visio.constants.visSectionObject, Visio.constants.visRowXFormOut, Visio.constants.visXFormWidth).FormulaU.replace("mm", ""))/style.pinInterval
        self.h = float(self.visioObject.CellsSRC(Visio.constants.visSectionObject, Visio.constants.visRowXFormOut, Visio.constants.visXFormHeight).FormulaU.replace("mm", ""))/style.pinInterval
        
        for pin in self.pins:
            pin.x = self.x + (pin.xRate-0.5) * self.w
            pin.y = self.y + (pin.yRate-0.5) * self.h
            
        for sub in self.children:
            if (type(sub) is Shape):
                sub.update()
        
    
    def pos(self, x = None, y = None):
        self.select()
        if (x != None): 
            Visio.visapp.ActiveWindow.Selection.Move(x*style.pinInterval*style.pt2mm, 0)
        if (y != None): 
            Visio.visapp.ActiveWindow.Selection.Move(0, y*style.pinInterval*style.pt2mm)
            
        dx, dy = x-self.x, y-self.y
        self.x, self.y = x, y
        for pin in self.pins:
            pin.x += dx
            pin.y += dy
            
    def size(self, width = 0, height = 0):
        w = width*style.pinInterval
        h = height*style.pinInterval
        
        if (width != 0): 
            self.visioObject.CellsSRC(Visio.constants.visSectionObject, Visio.constants.visRowXFormOut, Visio.constants.visXFormWidth).FormulaU = f"{w} mm"
            self.w = width
        if (height != 0): 
            self.visioObject.CellsSRC(Visio.constants.visSectionObject, Visio.constants.visRowXFormOut, Visio.constants.visXFormHeight).FormulaU = f"{h} mm"
            self.h = height

    def style(self, 
              # Line
              lineWidth=style.lineWidth, lineClear=False,
              # Font
              fontSize=style.fontSizeMain, fontAlign = -1,
              # Filling
              colorFill=style.fillingColor, colorFillClear=False
            ):
        
        # Line
        if (lineClear):
            self.visioObject.CellsSRC(Visio.constants.visSectionObject, Visio.constants.visRowLine, Visio.constants.visLinePattern).FormulaU = "0"
        self.visioObject.CellsSRC(Visio.constants.visSectionObject, Visio.constants.visRowLine, Visio.constants.visLineWeight).FormulaU = f'{lineWidth}pt'
        # Text
        self.visioObject.CellsSRC(Visio.constants.visSectionCharacter, 0, Visio.constants.visCharacterSize).FormulaU = f'{fontSize}pt'
        if (fontAlign != -1): self.visioObject.CellsSRC(Visio.constants.visSectionParagraph, 0, Visio.constants.visHorzAlign).FormulaU = fontAlign
        # Color
        if (colorFillClear):
            self.visioObject.CellsSRC(Visio.constants.visSectionObject, Visio.constants.visRowFill, Visio.constants.visFillPattern).FormulaU = "0"
            self.visioObject.CellsSRC(Visio.constants.visSectionObject, Visio.constants.visRowShapeLayout, Visio.constants.visSLOPermX).FormulaForceU = "TRUE"
            self.visioObject.CellsSRC(Visio.constants.visSectionObject, Visio.constants.visRowShapeLayout, Visio.constants.visSLOPermY).FormulaForceU = "TRUE"
        self.visioObject.CellsSRC(Visio.constants.visSectionObject, Visio.constants.visRowFill, Visio.constants.visFillForegnd).FormulaU = colorFill
    
    def addPin(self, xRate:float, yRate:float):
        if (type(self.visioObject) is list): return
        
        pinIndex = self.visioObject.AddRow(Visio.constants.visSectionConnectionPts, Visio.constants.visRowLast, Visio.constants.visTagCnnctPt)
        pin = self.visioObject.Section(Visio.constants.visSectionConnectionPts).Row(pinIndex)

        # Locate
        pin.Cell(Visio.constants.visCnnctX).FormulaU = f"Width*{xRate}" # 0~1 (left~right)
        pin.Cell(Visio.constants.visCnnctY).FormulaU = f"Height*{yRate}" # 0~1 (bottom~top)
        
        pinObject = Pin(self.visioObject.CellsSRC(7, pinIndex, 0))
        pinObject.x = self.w*xRate - self.w/2 + self.x
        pinObject.y = self.h*yRate - self.h/2 + self.y
        pinObject.xRate = xRate
        pinObject.yRate = yRate
        
        self.pins.append(pinObject)
        return pinObject
        
class Group:
    def __init__(self, children:list):
        self.children = children
        self.visioObject = self.__makeGroup()
        self

    def __makeGroup(self):
        for child in self.children:
            child.select(True)
        
        return Visio.visapp.ActiveWindow.Selection.Group()
    
    def select(self, acc=False):
        if (acc == False): Visio.visapp.ActiveWindow.DeselectAll()
        
        Visio.visapp.ActiveWindow.Select(self.visioObject, Visio.constants.visSelect)

    def pos(self, x = 0, y = 0):
        self.select()
        x *= style.pinInterval*style.pt2mm
        y *= style.pinInterval*style.pt2mm
        if (x != 0): Visio.visapp.ActiveWindow.Selection.Move(x, 0)
        if (y != 0): Visio.visapp.ActiveWindow.Selection.Move(0, y)


class Line:
    def __init__(self, page):
        self.page = page
        self.visioObject = page.Drop(Visio.masterWire, 0, 0)
        self.componentConstant = Visio.constants.visSectionFirstComponent
        self.setInitialNode(False)
        self.endGlued = False
        
    def select(self, acc=False):
        if (acc == False): Visio.visapp.ActiveWindow.DeselectAll()
        
        Visio.visapp.ActiveWindow.Select(self.visioObject, Visio.constants.visSelect)
        
        
    def __tempComponent2Set(self):
        self.visioObject.CellsSRC(Visio.constants.visSectionFirstComponent, 0, 2).FormulaForceU = "TRUE"
        self.visioObject.CellsSRC(Visio.constants.visSectionObject, Visio.constants.visRowXFormOut, Visio.constants.visXFormWidth).FormulaForceU = "GUARD(EndX-BeginX)"
        self.visioObject.CellsSRC(Visio.constants.visSectionObject, Visio.constants.visRowXFormOut, Visio.constants.visXFormHeight).FormulaForceU = "GUARD(EndY-BeginY)"
        
        self.visioObject.AddSection(Visio.constants.visSectionFirstComponent+1)
        self.visioObject.AddRow(Visio.constants.visSectionFirstComponent+1, Visio.constants.visRowComponent, Visio.constants.visTagComponent)
        self.visioObject.AddRow(Visio.constants.visSectionFirstComponent+1, Visio.constants.visRowVertex, Visio.constants.visTagLineTo)
        self.visioObject.AddRow(Visio.constants.visSectionFirstComponent+1, Visio.constants.visRowVertex, Visio.constants.visTagMoveTo)
        self.visioObject.CellsSRC(Visio.constants.visSectionFirstComponent+1, 0, 0).FormulaForceU = "TRUE"  
        self.visioObject.CellsSRC(Visio.constants.visSectionFirstComponent+1, 0, 1).FormulaForceU = "FALSE"   
        self.visioObject.CellsSRC(Visio.constants.visSectionFirstComponent+1, 0, 2).FormulaForceU = "FALSE"  
        self.visioObject.CellsSRC(Visio.constants.visSectionFirstComponent+1, 0, 3).FormulaForceU = "FALSE"  
        self.visioObject.CellsSRC(Visio.constants.visSectionFirstComponent+1, 0, 5).FormulaForceU = "FALSE" 
        self.visioObject.CellsSRC(Visio.constants.visSectionFirstComponent+1, 1, 0).FormulaU = f"0"    
        self.visioObject.CellsSRC(Visio.constants.visSectionFirstComponent+1, 1, 1).FormulaU = f"0" 
        
        self.componentConstant += 1
        
    def staightLine(self, beginX:int, beginY:int, endX:int, endY:int):
        self.select()
        Visio.visapp.ActiveWindow.Selection.Delete()
        
        coord = [c*style.pinInterval*style.pt2mm for c in [beginX, beginY, endX, endY]]        
        self.visioObject = self.page.DrawLine(coord[0], coord[1], coord[2], coord[3])
        
        return self.visioObject
        
    
    def setInitialNode(self, reverse):
        self.visioObject.CellsSRC(Visio.constants.visSectionObject, Visio.constants.visRowXFormOut, Visio.constants.visXFormWidth).FormulaForceU = "GUARD(EndX-BeginX)"
        self.visioObject.CellsSRC(Visio.constants.visSectionObject, Visio.constants.visRowXFormOut, Visio.constants.visXFormHeight).FormulaForceU = "GUARD(EndY-BeginY)"
        self.visioObject.CellsSRC(Visio.constants.visSectionObject, Visio.constants.visRowLine, Visio.constants.visLineWeight).FormulaU = f"{style.lineWidth} pt"
        self.visioObject.CellsSRC(Visio.constants.visSectionObject, Visio.constants.visRowShapeLayout, Visio.constants.visSLOConFixedCode).FormulaU = "3"
        self.visioObject.CellsSRC(Visio.constants.visSectionObject, Visio.constants.visRowShapeLayout, Visio.constants.visSLOJumpCode).FormulaU = "2"
        self.visioObject.CellsSRC(Visio.constants.visSectionObject, Visio.constants.visRowShapeLayout, Visio.constants.visSLOJumpStyle).FormulaU = "1"
        self.visioObject.CellsSRC(Visio.constants.visSectionObject, Visio.constants.visRowShapeLayout, Visio.constants.visSLOLineRouteExt).FormulaU = "1"
        if (reverse==False):
            self.visioObject.CellsSRC(Visio.constants.visSectionObject, Visio.constants.visRowLine, Visio.constants.visLineBeginArrow).FormulaU = '0'
            self.visioObject.CellsSRC(Visio.constants.visSectionObject, Visio.constants.visRowLine, Visio.constants.visLineEndArrow).FormulaU = '13'
        else:
            self.visioObject.CellsSRC(Visio.constants.visSectionObject, Visio.constants.visRowLine, Visio.constants.visLineBeginArrow).FormulaU = '13'
            self.visioObject.CellsSRC(Visio.constants.visSectionObject, Visio.constants.visRowLine, Visio.constants.visLineEndArrow).FormulaU = '0'
           
    
    def glueTo(self, begin=None, end=None): # TODO: route
        if (begin is not None):
            self.visioObject.CellsU("BeginX").GlueTo(begin)
        if (end is not None):
            self.visioObject.CellsU("EndX").GlueTo(end)
            self.endGlued = True
            
    def setBegin(self, x=None, y=None):
        if (x is not None):
            self.visioObject.CellsSRC(Visio.constants.visSectionObject, Visio.constants.visRowXForm1D, Visio.constants.vis1DBeginX).FormulaU = f"{x/5}"
            self.visioObject.CellsSRC(Visio.constants.visSectionObject, Visio.constants.visRowXForm1D, Visio.constants.vis1DBeginY).FormulaU = self.visioObject.CellsSRC(Visio.constants.visSectionObject, Visio.constants.visRowXForm1D, Visio.constants.vis1DEndY).FormulaU
        if (y is not None):
            self.visioObject.CellsSRC(Visio.constants.visSectionObject, Visio.constants.visRowXForm1D, Visio.constants.vis1DBeginX).FormulaU = self.visioObject.CellsSRC(Visio.constants.visSectionObject, Visio.constants.visRowXForm1D, Visio.constants.vis1DEndX).FormulaU
            self.visioObject.CellsSRC(Visio.constants.visSectionObject, Visio.constants.visRowXForm1D, Visio.constants.vis1DBeginY).FormulaU = f"{y/5}" 
                 
    def setEnd(self, x=None, y=None):
        if (x is not None):
            self.visioObject.CellsSRC(Visio.constants.visSectionObject, Visio.constants.visRowXForm1D, Visio.constants.vis1DEndX).FormulaU = f"{x/5}"
            self.visioObject.CellsSRC(Visio.constants.visSectionObject, Visio.constants.visRowXForm1D, Visio.constants.vis1DEndY).FormulaU = self.visioObject.CellsSRC(Visio.constants.visSectionObject, Visio.constants.visRowXForm1D, Visio.constants.vis1DBeginY).FormulaU
        if (y is not None):
            self.visioObject.CellsSRC(Visio.constants.visSectionObject, Visio.constants.visRowXForm1D, Visio.constants.vis1DEndX).FormulaU = self.visioObject.CellsSRC(Visio.constants.visSectionObject, Visio.constants.visRowXForm1D, Visio.constants.vis1DBeginX).FormulaU
            self.visioObject.CellsSRC(Visio.constants.visSectionObject, Visio.constants.visRowXForm1D, Visio.constants.vis1DEndY).FormulaU = f"{y/5}" 
                 
    def followRoute(self, route:list, reverse=False):
        self.setInitialNode(reverse)
        #self.__tempComponent2Set()       
        self.visioObject.CellsSRC(self.componentConstant, 1, 0).FormulaForceU = f"0"    
        self.visioObject.CellsSRC(self.componentConstant, 1, 1).FormulaForceU = f"0"   
        for i in range(0, len(route)):
            x, y = route[i]
            self.visioObject.CellsSRC(self.componentConstant, i+2, 0).FormulaForceU = f"{x/5}"    
            self.visioObject.CellsSRC(self.componentConstant, i+2, 1).FormulaForceU = f"{y/5}" 
        
        return


def makeGroup(children):
    for child in children:
        child.select(True)
        
    return Visio.visapp.ActiveWindow.Selection.Group()