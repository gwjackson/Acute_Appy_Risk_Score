# Author: Walker Jackson, MD
# email gwjackson53@gmail.com
# from source material listed in code files
# initial commit - 06/22,2026

# now the main backup before refactoring


import wx
import wx.html2 as wv       # webview
from wx._core import StaticText


class MainFrame(wx.Frame):
    def __init__(self):
        super().__init__(None,
                         title="Clinical Screening for Adults with Acute Appendicitis",
                         size=(680, 730),
                         style=wx.DEFAULT_FRAME_STYLE | wx.RESIZE_BORDER)

        gbf_panel = wx.Panel(self)
        frame_sizer = wx.BoxSizer(wx.VERTICAL)



        ## build sections for each part of the GUI
        #self._build_menu()
        fgbs_grid = self._build_fbgs_grid(gbf_panel)
        #bottom_buttons = self._build_button(panel)


        frame_sizer.Add(fgbs_grid, 0, flag=wx.EXPAND | wx.ALL, border=5)
        frame_sizer.SetSizeHints(self)
        self.SetSizer(frame_sizer)

        self.Centre()
        self.Show()


    #-----------------------------------------------------------------------------------------------
    ##### gridbagsizer #####
    #-----------------------------------------------------------------------------------------------
    """
    TODO: add the code for the user selections
    All I have now is just the layout
    """
    def _build_fbgs_grid(self, gbf_panel):
        fgbs = wx.GridBagSizer(2, 2)

        # table header
        # use helper to create a single line for the headers

        def one_line_text(parent, value="", one_char=False):
            txt = wx.TextCtrl(
                parent, -1, value,
                style=wx.BORDER_SIMPLE|wx.TE_CENTER|wx.TE_READONLY|wx.TE_NO_VSCROLL,
                )
            if one_char:
                txt.SetMinSize((-1, txt.GetCharHeight()))
            txt.SetMinSize(txt.GetBestSize())
            return txt

        idxflags = wx.EXPAND|wx.ALL

        fgbs.Add(one_line_text(gbf_panel, "Category", one_char=True),
                 (0,0), flag=idxflags, border=2)
        fgbs.Add(one_line_text(gbf_panel, "Alvarado (points)", one_char=True),
                 (0,1), flag=idxflags, border=2)
        fgbs.Add(one_line_text(gbf_panel, "RIPASA (points)", one_char=True),
                 (0,2), flag=idxflags, border=2)

        # table first column
        fgbs.Add(one_line_text(gbf_panel, "Demographics"),
                 (1, 0), flag=idxflags, border=2)
        fgbs.Add(one_line_text(gbf_panel, "Laboratory findings"),
                 (2, 0), flag=idxflags, border=2)
        fgbs.Add(one_line_text(gbf_panel, "Signs"),
                 (3, 0), flag=idxflags, border=2)
        fgbs.Add(one_line_text(gbf_panel, "Symptoms"),
                 (4, 0), flag=idxflags, border=2)
        fgbs.Add(one_line_text(gbf_panel, "Cutoff Score"),
                 (5, 0), flag=idxflags, border=2)


        # table second column
        fgbs.Add(one_line_text(gbf_panel, "- - -"),
                 (1, 1), flag=idxflags, border=2)

        alvchbxWBCsizer=wx.BoxSizer(wx.VERTICAL)
        alvchbxWBCsizer.Add(wx.CheckBox(gbf_panel, -1, "Leukocytosis(2)", name='alvckbxwbc'))
        alvchbxWBCsizer.Add(wx.CheckBox(gbf_panel, -1, "Left shift (1)", name='alvckbxleftshift'))
        fgbs.Add(alvchbxWBCsizer, (2, 1), flag=idxflags, border=2)

        alvchbxsgsizer = wx.BoxSizer(wx.VERTICAL)
        alvchbxsgsizer.Add(wx.CheckBox(gbf_panel, -1, 'Fever (1)', name='alvchbxfever'))
        alvchbxsgsizer.Add(wx.CheckBox(gbf_panel, -1, 'Rebound pain (1)', name='alvchbxrebound'))
        alvchbxsgsizer.Add(wx.CheckBox(gbf_panel, -1, 'RLQ tenderness(2)', name='alvchbxrlq'))
        fgbs.Add(alvchbxsgsizer, (3, 1), flag=idxflags, border=2)

        alvchbxsymsizer = wx.BoxSizer(wx.VERTICAL)
        alvchbxsymsizer.Add(wx.CheckBox(gbf_panel, -1, 'Anorexia (1)', name='alvchbxanorexia'))
        alvchbxsymsizer.Add(wx.CheckBox(gbf_panel, -1, 'Migration of pain (1)', name='alvchbxmig' ))
        alvchbxsymsizer.Add(wx.CheckBox(gbf_panel, -1, 'Nausea or vomiting (1)', name='alvchbxnausea'))
        fgbs.Add(alvchbxsymsizer, (4, 1), flag=idxflags, border=2)


        ##################
        # table third column

        riprbsizer = wx.BoxSizer(wx.VERTICAL)
        riprbsizer.Add(wx.RadioButton(gbf_panel, -1, "Age <= 40 (1)", style=wx.RB_GROUP, name='riprbage'))
        riprbsizer.Add(wx.RadioButton(gbf_panel, -1, "Age > 40 (0.5)", name='riprbage'))
        riprbsizer.Add(wx.StaticText(gbf_panel, -1, "- - - "))
        riprbsizer.Add(wx.RadioButton(gbf_panel, -1, "Gender: Female (0.5)", style=wx.RB_GROUP, name='riprbsex'))
        riprbsizer.Add(wx.RadioButton(gbf_panel, -1, "Gender: Male (1)", name='riprbsex'))
        fgbs.Add(riprbsizer,(1, 2), flag=idxflags, border=2)

        ripchbxwbcsizer = wx.BoxSizer(wx.VERTICAL)
        ripchbxwbcsizer.Add(wx.CheckBox(gbf_panel, -1,  'Leucocytosis (1)', name="ripchbxtwbc"))
        ripchbxwbcsizer.Add(wx.StaticText(gbf_panel, -1,  '- - - '))
        ripchbxwbcsizer.Add(wx.CheckBox(gbf_panel, -1,  'Neg. Urinalysis (1)', name='uaWNL' ))
        fgbs.Add(ripchbxwbcsizer,(2, 2), flag=idxflags, border=2)

        ripchbxsgsizer = wx.BoxSizer(wx.VERTICAL)
        ripchbxsgsizer.Add(wx.CheckBox(gbf_panel, -1, 'Fever (1)', name='ripchbxsg'))
        ripchbxsgsizer.Add(wx.CheckBox(gbf_panel, -1, 'Rebound pain (1)', name='ripchbxrebound'))
        ripchbxsgsizer.Add(wx.CheckBox(gbf_panel, -1, 'RLQ tenderness (2)', name='ripchbxsgrlq'))
        ripchbxsgsizer.Add(wx.CheckBox(gbf_panel, -1, 'Guarding (2)', name='ripchbxsggrd'))
        ripchbxsgsizer.Add(wx.CheckBox(gbf_panel, -1, 'Rovsing sign (2)', name='ripchbxsgrs'))
        fgbs.Add(ripchbxsgsizer, (3, 2), flag=idxflags, border=2)

        """
        fgbs.Add(wx.TextCtrl(gbf_panel, -1, "Anorexia 1\nMigration of pain 1\nNausea & Vomiting 1"
                                            "\nRLQ pain 0.5\nDurations of sx's <= 48hr 1"
                                            "Durations of sx's > 40hr 0.5",
                             style=wx.BORDER_SIMPLE | wx.TE_READONLY | wx.TE_NO_VSCROLL | wx.TE_MULTILINE),
                 (4, 2), flag=idxflags, border=2)
        """
        ripchbxsymsizer = wx.BoxSizer(wx.VERTICAL)
        ripchbxsymsizer.Add(wx.CheckBox(gbf_panel, -1, 'Anorexia (1)', name='ripchbxsymanorexia'))
        ripchbxsymsizer.Add(wx.CheckBox(gbf_panel, -1, 'Migration of pain (0.5)', name='ripchbxsymmig'))
        ripchbxsymsizer.Add(wx.CheckBox(gbf_panel, -1, 'Nausea or vomiting (1)', name='ripchbxsymnausea'))
        ripchbxsymsizer.Add(wx.CheckBox(gbf_panel, -1, 'RLQ pain (0.5)', name='ripchbxsymrlq'))
        ripchbxsymsizer.Add(StaticText(gbf_panel, -1,  'Duration of symptoms:'))
        ripchbxsymsizer.Add(wx.RadioButton(gbf_panel, -1, "<= 48 hours (1)", style=wx.RB_GROUP, name='riprbsmdur'))
        ripchbxsymsizer.Add(wx.RadioButton(gbf_panel, -1, "> 48 hours (0.5)", name='riprbsmdur'))
        fgbs.Add(ripchbxsymsizer,(4, 2), flag=idxflags, border=2)

        fgbs.Add(one_line_text(gbf_panel, ">= 7"),
                 (5, 1), flag=idxflags, border=2)
        fgbs.Add(one_line_text(gbf_panel, ">= 7.5"),
                 (5, 2), flag=idxflags, border=2)
        #table last row
        fgbs.Add(wx.TextCtrl(gbf_panel, -1, "Note: \n-Leukocytosis is defined as a white bloood cell count > 10,000/ul, "
                             "\n-and a left shift is defined as > 75% neutrophils.\n"
                                            "Alvarado: Score:\n"
                                            "\t< 4 suggests appendicitis unlikely\n"
                                            "\t4 - 6 possible acute appendicits and imaging recommended\n"
                                            "\t>=7 suggests need for early surgical consultation\n"
                                            "\nRIPASA of >= 7.5 suggest prompt surgical consultations\n"
                                            "\nSee citations",
                        style=wx.BORDER_SIMPLE|wx.TE_READONLY|wx.VSCROLL|wx.TE_MULTILINE|wx.TE_WORDWRAP),
                 (6, 0), span=(1,3), flag=wx.EXPAND|wx.ALL, border=2)
        """     copilot suggested that i needed these but get the results in layout I want without 
                but the cells are not expanding w/the window size ? 
        """

        fgbs.AddGrowableCol(0)
        fgbs.AddGrowableCol(1)
        fgbs.AddGrowableCol(2)
        fgbs.AddGrowableRow(6)
        fgbs.AddGrowableRow(0)

        gbf_panel.SetSizer(fgbs)

        return gbf_panel

    #-----------------------------------------------------------------------------------------------
    # MENU BAR
    #-----------------------------------------------------------------------------------------------
    def _build_mmenu(self):
        pass

     #return menu_bar

def outprint():
    print(f"Hello; wxPython version!, {wx.__version__}")
    return

outprint()


if __name__ == "__main__":
    app = wx.App()
    mainFrame = MainFrame()
    mainFrame.Show()
    app.MainLoop()
