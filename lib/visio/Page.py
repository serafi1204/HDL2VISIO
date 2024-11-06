from . import Visio

def addPage(title = 'untitled'):
    if (Visio.pageN == 0): 
        page = Visio.visapp.ActiveDocument.Pages.ItemU("Page-1")
    else:
        page = Visio.visapp.ActiveDocument.Pages.Add()
        
    #page.PageSheet.CellsSRC(Visio.constants.visSectionObject, Visio.constants.visRowPage, Visio.constants.visPageScale).FormulaU = "1 pt"
    #page.PageSheet.CellsSRC(Visio.constants.visSectionObject, Visio.constants.visRowPage, Visio.constants.visPageDrawingScale).FormulaU = "1 pt"
    Visio.pageN += 1
    page.Name = f"{title}-{Visio.pageN}"
    return page 