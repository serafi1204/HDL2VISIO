# Make New VSD file

    win32com.client.gencache.EnsureDispatch("Visio.Application")
    visapp = win32com.client.Dispatch("Visio.Application") # Class visio funcions
    visapp.Visible = 1 # Open visio program

# Page, Shapes control

    # Move shaps to center
    page.CenterDrawing()

### Group
    visapp.ActiveWindow.Select(shape0, constants.visSelect)
    visapp.ActiveWindow.Select(shape1, constants.visSelect)
    visapp.ActiveWindow.Selection.Group()

# Block

    #1. Load stencil
    VORO = constants.visOpenRO
    VID = constants.visOpenRO
    stencildoc = visapp.Documents.OpenEx("basic_u.vss" , VORO | VID)

    #2. Declare master
    masterRect = stencildoc.Masters.ItemU("rectangle")
    masterRRect = stencildoc.Masters.ItemU("rounding rectangle")
    masterCircle = stencildoc.Masters.ItemU("circle")
    masterConnector = stencildoc.Masters.ItemU("dynamic connector")

    #3. Drop on your page
    shape = page.Drop(masterRect, 0, 0)
    connector = page.Drop(masterConnector, 0, 0)

### Edit

    # Para
    VSO = constants.visSectionObject
    VRXFO = constants.visRowXFormOut
    VXFW = constants.visXFormWidth
    VXFH = constants.visXFormHeight

    # Drop shape
    shape = page.Drop(masterRect, 0, 0)

    # Resize
    shape.CellsSRC(VSO, VRXFO, VXFW).FormulaU = "100 mm"
    shape.CellsSRC(VSO, VRXFO, VXFH).FormulaU = "100 mm"

### Style

    # Text
    VSC = constants.visSectionCharacter
    VCS = constants.visCharacterSize
    VCSY = constants.visCharacterStyle

    shape.Characters.Text = 'Hello world!'
    shape.CellsSRC(VSC, 0, VCS).FormulaU = '17pt'
    shape.CellsSRC(VSC, 0, VCSY).FormulaU = 17 # 17 - 굵게 / 34 - 기울임 / 4 - 밑줄

    # Text alignment
    VSP = constants.visSectionParagraph
    VHA = constants.visHorzAlign

    shape.CellsSRC(VSP, 0, VHA).FormulaU = "0" # 0 - left / 1 - center / 2 - right

    # Color
    VCC = constants.visCharacterColor
    VRL = constants.visRowLine
    VLC = constants.visLineColor
    VRF = constants.visRowFill
    VFF = constants.visFillForegnd
    VSO = constants.visSectionObject

    shape.CellsSRC(VSC, 0, VCC).FormulaU = "RGB(100,100,100)" # Text
    shape.CellsSRC(VSO, VRL, VLC).FormulaU = "RGB(100,100,100)" # line
    shape.CellsSRC(VSO, VRF, VFF).FormulaU = "RGB(100,100,100)" # Filling
    

# Wiring

    # para
    VSO = constants.visSectionObject
    VRL = constants.visRowLine
    VLBA = constants.visLineBeginArrow
    VLEA = constants.visLineEndArrow

    # Drop wire
    shape = page.Drop(masterRect, 0, 0)
    wire = page.Drop(masterConnector, 0, 0)

    # Add arrow
    wire.CellsSRC(VSO, VRL, VLEA).FormulaU = "13" # 0 - None / 13 - arrow
    wire.CellsSRC(VSO, VRL, VLBA).FormulaU = "13" # 0 - None / 13 - arrow

    # Glue to center of edge (It's ok just one of X or Y)
    # rect.CellsSRC(7, {location}, 0)
    # {location}: 0 - bottm / 1 - right / 2 - top / 3 - left / 4 - center
    wire.CellsU("BeginX").GlueTo(rect.CellsSRC(7, 0, 0))
    #wire.CellsU("BeginY").GlueTo(rect.CellsSRC(7, 0, 0))

    # Glue to vertex
    # rect.Cells("Geometry1.X{location}")
    # {location}: 1 - bottm,left / 2 - bottom,right / 3 - top,right / 4 - top,left
    wire.CellsU("EndX").GlueTo(rect.Cells("Geometry1.X1"))
    wire.CellsU("EndY").GlueTo(rect.Cells("Geometry1.Y1"))

### Add connect pin on shape

    # para
    VSCP = constants.visSectionConnectionPts
    VRL = constants.visRowLast
    VTCP = constants.visTagCnnctPt
    VCTI = constants.visCnnctTypeInward 

    # Declare pin
    pinIndex = rect.AddRow(VSCP, VRL, VTCP)
    pin = rect.Section(VSCP).Row(pinIndex)

    # Locate
    pin.Cell(constants.visCnnctX).FormulaU = "Width*1" # 0~1 (left~right)
    pin.Cell(constants.visCnnctY).FormulaU = "Height*0.6" # 0~1 (bottom~top)
