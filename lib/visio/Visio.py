from win32com.client import constants
import win32com.client

# Visio app
visapp = win32com.client.gencache.EnsureDispatch("Visio.Application")
doc = visapp.Documents.Add('')
visapp.Visible = 1

# Stencil
stencildoc = visapp.Documents.OpenEx("basic_u.vss" , constants.visOpenRO | constants.visOpenDocked)
masterRect = stencildoc.Masters.ItemU('rectangle')
masterWire = visapp.ConnectorToolDataObject

# Manage pages
pageN = 0
