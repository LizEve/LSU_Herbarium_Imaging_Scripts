
# C:\Python26\python.exe C:\PNWHerbaria\Scripts\renameimage.pyw C:\PNWHerbaria\Images\NewImages\WWB_000015.CR2

import sys
import os
import wx
import pickle

#---------------------------------------------------------------------------

class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(880,500))
        
        self.CreateStatusBar() # A Statusbar in the bottom of the window
        self.portal = ''
        # Creat menu objects

        # Set up the menu:
        filemenu = wx.Menu()

        # add separator at the end of the menu. idk what that means
        filemenu.AppendSeparator()
        # standard ID's like exit will add exit icon and shortcut, specify name of menu item, and message that shoes on status bar
        menuExit = filemenu.Append(wx.ID_EXIT,"E&xit"," Terminate the program")
        
        # Create a help menu
        helpmenu = wx.Menu()
        menuAbout = helpmenu.Append(wx.ID_HELP, "&About"," Information about this program")
        menuDocumentation = helpmenu.Append(wx.ID_ABOUT, "&Documentation"," Help and Documentation")
        
        # Create portal menu bar
        portalmenu = wx.Menu()
        menuAlg = portalmenu.Append(wx.ID, "&Algae", 'happy')
        '''
        menuBry = portalmenu.Append(wx.ID, 'Bryophyte')
        menuFun = portalmenu.Append(wx.ID, 'Fungi')
        menuLic = portalmenu.Append(wx.ID, 'Lichen')
        menuVas = portalmenu.Append(wx.ID, 'Vascular')
        '''
        # Create the help menu bar and append menus:
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu,"&File") # Adding the "filemenu" to the menu bar
        menuBar.Append(portalmenu,"&Portal")
        menuBar.Append(helpmenu,"&Help") # Adding the "helpmenu" to the menu bar
        self.SetMenuBar(menuBar)  # Adding the menu bar to the Frame content.
        
        
        # Bind the selection of menu items ot functions that will be defined below
        # Set events:
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.Bind(wx.EVT_MENU, self.OnDocumentation, menuDocumentation)
        self.Bind(wx.EVT_MENU, self.OnAlg, menuAlg)
        '''
        self.Bind(wx.EVT_MENU, self.OnBry, menuBry)
        self.Bind(wx.EVT_MENU, self.OnFun, menuFun)
        self.Bind(wx.EVT_MENU, self.OnLic, menuLic)
        self.Bind(wx.EVT_MENU, self.OnVas, menuVas)
        '''
    def OnAlg(self, event):
        self.portal = "A"
    '''    
    def OnBry(self, event):
        self.portal = "B"

    def OnFun(self, event):
        self.portal = "F"
        
    def OnLic(self, event):
        self.portal = "L"
        
    def OnVas(self, event):
        self.portal = "V"
    '''
    def OnExit(self,e):
        self.Close(True)  # Close the frame.

    def OnAbout(self, event):
        description = """lalala"""

        licence = """lalalal"""

        info = wx.AboutDialogInfo()

        info.SetIcon(wx.Icon('C:\\PNWHerbaria\\Scripts\\Icons\\icon.png', wx.BITMAP_TYPE_PNG))
        info.SetName('Rename Image, PNW Herbaria')
        #info.SetVersion('1.0')
        info.SetDescription(description)
        info.SetCopyright('(C) 2010 Ben Legler')
        info.SetWebSite('http://www.pnwherbaria.org/')
        info.SetLicence(licence)

        wx.AboutBox(info)

    def OnDocumentation(self, e):
        # Start a file with it's associate application
        os.startfile(documentationPath)


#---------------------------------------------------------------------------

'''
class PopUp(wx.Panel):
    def __init__(self,parent):
        # delcare things
http://zetcode.com/wxpython/dialogs/
'''     

#---------------------------------------------------------------------------
class MainPanel(wx.Panel):
    def __init__(self, parent):
        
        # Declare some variables for later use:
        self.oldNamePath = ""
        self.oldNameDir = ""
        self.oldName = ""
        self.fileType = ""
        self.newName = ""
        self.newNamePath = ""
        self.dbEntry = ""
        self.inDB = ""
        
        # Had these in a function. don't really need that. can define here. 
        self.p = "/mnt/c/Users/Image/Desktop/db.pkl"
        self.db = pickle.load(open(self.p,'rb'))
        
        # def OpenDB(self):
        # someday make this a drop down window to select which database file to input 
        # hard code where db is and what it's called. FIX 

        
        wx.Panel.__init__(self, parent)

        # create some sizers
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        # This does some size creation, making a relative grid 
        grid1 = wx.GridBagSizer(hgap=5, vgap=5)

        # Old image name: get old name from text file where we wrote it to 
        self.oldName = self.GetOldName()
        self.oldNameLabel = wx.StaticText(self, label="Old name:")
        # position is (horizontal, vertical)
        grid1.Add(self.oldNameLabel, pos=(1,0))
        self.oldNameField = wx.StaticText(self, label=self.oldName)
        grid1.Add(self.oldNameField, pos=(1,1))
        
        #Refresh button
        self.refreshBtn = wx.Button(self, label="Refresh")
        grid1.Add(self.refreshBtn, pos=(1,3))
        ## In the EVENT that refreshBtn is pushed, run Refresh function.
        self.Bind(wx.EVT_BUTTON, self.Refresh, self.refreshBtn)
        
        # New image name (barcode):
        self.newNameLabel = wx.StaticText(self, label="New Name:")
        grid1.Add(self.newNameLabel, pos=(2,0))
        
        # text control allows text to be displayed and edited, then add to grid 
        self.newNameField = wx.TextCtrl(self, value='', size=(150,-1))
        grid1.Add(self.newNameField, pos=(2,1))
        
        ## A focus event is when a windows focus changes
        ## I have no idea what this one does. 
        #self.newNameField.Bind(wx.EVT_KILL_FOCUS, self.Rename)
        
        ## Rename button:
        self.renameBtn = wx.Button(self, label="Rename")
        grid1.Add(self.renameBtn, pos=(2,3))
        ## In the EVENT that renameBtn is pushed, run Rename function.
        self.Bind(wx.EVT_BUTTON, self.Rename, self.renameBtn)
        
        self.newNameHint = wx.StaticText(self, label="(don't include file extension)")
        grid1.Add(self.newNameHint, pos=(3,1))
        
        # add a spacer between the button and the instructions:
        grid1.Add((10, 10), pos=(4,0))
        
        self.instructions1 = wx.StaticText(self, label="  INSTRUCTIONS:")
        self.instructions2 = wx.StaticText(self, label="    1) Double-check that the cursor is in the New Name field.")
        self.instructions3 = wx.StaticText(self, label="    2) Then use the barcode reader to scan the barcode.")
        self.instructions4 = wx.StaticText(self, label="    3) If you need to add a suffix, use the keyboard to manually edit the new name.")
        self.instructions5 = wx.StaticText(self, label="    4) Then click the Rename button to rename the image and close this window.")
        
        mainSizer.Add(grid1, 0, wx.ALL, 5)
        
        mainSizer.Add(self.instructions1, 0, wx.ALIGN_LEFT)
        mainSizer.Add(self.instructions2, 0, wx.ALIGN_LEFT)
        mainSizer.Add(self.instructions3, 0, wx.ALIGN_LEFT)
        mainSizer.Add(self.instructions4, 0, wx.ALIGN_LEFT)
        mainSizer.Add(self.instructions5, 0, wx.ALIGN_LEFT)
        
        self.SetSizerAndFit(mainSizer)
    

    '''
    def SearchDB(self):
        # searches database for barcode
        # returns nothing or entry matching the barcode 
        try:
            self.dbEntry=self.db[self.newName]
            return(self.dbEntry) 
        except KeyError:
            return("")
    
    #def SearchDB(self):
        # search for new name. self.newname self.db
        # return list of all matches 
        # if len(matches) > 0
            # open pop up window with results and two buttons 
            # write over = do nothing, close window
            # delete current file = delete current file 
    '''        
    
    def GetOldName(self):
        # gets old name from file instead of input 
        # Reads first line of file 
        try:
            with open(os.path.join(os.getcwd(),"incoming_img_default_names.txt"), "r") as the_man:
                for line in the_man.readlines():
                    self.oldNamePath = line
                the_man.close()
        except:
            return ""
        head, tail = os.path.split(self.oldNamePath) # split off only file name 
        self.oldNameDir = head
        self.oldName = tail
        self.fileType = tail.split(".")[1]
        return tail
        
    def Refresh(self, event):   
        # setlabel is a built in function, change name of variables
        # get old name function, and put into oldnamefield
        self.oldNameField.SetLabel(self.GetOldName())
    
    def Rename(self, event):
        # If there is not image in folder
        if self.oldNamePath == "":
            dial = wx.MessageDialog(None, 'ERROR: there is no image to rename (old name is blank), retake photo', 'Error', wx.OK | wx.ICON_ERROR)
            # Makes the parent window accessable even when dialog window is open
            dial.ShowModal()
            # Resets focus back to field where not barcode pops up
            self.newNameField.SetFocus()
            self.newNameField.SetSelection(-1,-1)
            #wx.Exit()
            return
        # If old file dissapears before renaming is complete
        if os.path.exists(self.oldNamePath) == False:
            dial = wx.MessageDialog(None, 'ERROR: No image file exists for the old name. Check images folder if file was already renamed.', 'Error', wx.OK | wx.ICON_ERROR)
            dial.ShowModal()
            self.newNameField.SetFocus()
            self.newNameField.SetSelection(-1,-1)
            #wx.Exit()
            return
        # Gets contents of the control (?)
        # Grabs text from newNameField box. 
        self.newName = self.newNameField.GetValue()
        #### HERE put in database checker. 
        '''
        # Search database for new barcode 
        self.inDB = SearchDB()
        
        # if there is an entry for the barcode aka newname 
        if len(self.inDB) > 0:
            dial = wx.MessageDialog(None, 'ERROR:'+self.inDB, 'Error', wx.OK | wx.ICON_ERROR)
            # Makes the parent window accessable even when dialog window is open
            dial.ShowModal()
            # Resets focus back to field where not barcode pops up
            self.newNameField.SetFocus()
            self.newNameField.SetSelection(-1,-1)
            #wx.Exit()
            return
        # is newName in hardcoded database 
        
        # if yes - bring up error message with 
        '''
        
        # Set up new file path for renamed image 
        self.newNamePath = os.path.join(self.oldNameDir, self.newName + "." + self.fileType)
        if self.newName == "":
            dial = wx.MessageDialog(None, 'ERROR: new name is blank.  Image was not renamed.', 'Error', wx.OK | wx.ICON_ERROR)
            dial.ShowModal()
            self.newNameField.SetFocus()
            return
        renameImage = True
        if os.path.exists(self.newNamePath):
            renameImage = False
            dial = wx.MessageDialog(None, 'An image with this file name already exists.  Do you want to overwrite it?', 'Warning', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_EXCLAMATION)
            dialInput = dial.ShowModal()
            if dialInput == wx.ID_YES:
                renameImage = True
        if renameImage == True:
            if os.path.exists(self.newNamePath) and self.oldNamePath != self.newNamePath:
                os.remove(self.newNamePath)
            if os.path.exists(self.oldNamePath) and self.oldNamePath != self.newNamePath:
                os.rename(self.oldNamePath, self.newNamePath)
            
            self.oldNameField.SetLabel("Click Refresh AFTER taking photo")
            self.newNameField.SetLabel('')
            #wx.Exit()
            return
        else:
            self.newNameField.SetFocus()
            self.newNameField.SetSelection(-1,-1)


class SingleApp(wx.App):
    """
    first time, runs with instance=False
    checks if another instance of this program is running, using some magic built in functions
    returns True, so another call of this program, writes to file, doesnt open new window. 
    refresh gets old name from file 
    """
    def OnInit(self):
        self.name = "SingleApp-%s" % wx.GetUserId()
        self.instance = wx.SingleInstanceChecker(self.name)
        # Not 100% sure what this does 
        if self.instance.IsAnotherRunning():
            panel = MainPanel(frame)
        frame = MainWindow(None, "Rename Image, PNW Herbaria")
        panel = MainPanel(frame)
        frame.Show()
        return True
        

# Make a file to pass name of picture just taken 
f_path = os.path.join(os.getcwd(),"incoming_img_default_names.txt")
# Take input from EOS camera program and write to file 
with open(f_path, "w") as the_man:
    the_man.write(sys.argv[1])
    the_man.close()
    

# Assign variable to class instance 
app = SingleApp(redirect=False)
# Once app is run one, redirect value gets sets to True, by OnInit function within SingleApp class 
app.MainLoop()
