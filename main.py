# Author: Walker Jackson, MD
# email gwjackson53@gmail.com
# from source material listed in code files
# initial commit - 06/22,2026

# now the main backup before refactoring


import wx
import wx.html2 as wv       # webview



class MainFrame(wx.Frame):
    def __init__(self):
        super().__init__(None,
                         title="Clinical Screening for Adults with Acute Appendicitis",
                         size=(680, 730),
                         style=wx.DEFAULT_FRAME_STYLE | wx.RESIZE_BORDER)

        self.gbf_panel = wx.Panel(self)
        frame_sizer = wx.BoxSizer(wx.VERTICAL)



        ## build sections for each part of the GUI
        self._build_menu()
        fgbs_grid = self._build_fbgs_grid(self.gbf_panel)
        bottom_buttons = self._build_button_row(self)


        frame_sizer.Add(fgbs_grid, 0, flag=wx.EXPAND | wx.ALL, border=5)
        frame_sizer.Add(bottom_buttons, 0, flag=wx.EXPAND | wx.ALL, border=5)

        frame_sizer.SetSizeHints(self)
        self.SetSizer(frame_sizer)

        self.Centre()
        self.Show()

    # -----------------------------------------------------------------------------------------------
    ##### on_click stuff #####
    # -----------------------------------------------------------------------------------------------

    obj_links = {}
    """
    As there are 8 options for the scoring system that are the same; this is a dictionary to cross link the checkboxes 
    with their counter parts (if they exist) in the alternate scoring system
    {obj clicked : linked obj,}
    The value could be a list of linked objects, but that is not needed here.
    Here all the linked objects just happen to be checkboxes and are 1 : 1  
    the objects are appended to the dict at the object's definition time
    
    obj_link is the source object and the dic obj_links{source, target}
    So obj_links{} is acting as an object registry 
    obj_links{} is built at run time by the object creation responsibility thus not have
    to remember to update the object links  when changes made to the GUI   
    """
    def obj_link(self, src_name, value):
        """
        helper function to do the lookup on obj_links
        :param src_name: calling / clicked - object name
        :param value: Event - state
        :return: None, causes change of state to target object
        """
        print(self.obj_links)
        if src_name in self.obj_links:
            target_name = self.obj_links[src_name]
            target = self.gbf_panel.FindWindowByName(target_name)
            target.SetValue(value)

    def on_alvleuk(self, event):
        self.obj_link('alvckbxwbc', event.IsChecked())

    def on_ripleuk(self, event):
        self.obj_link('ripchbxwbc', event.IsChecked())

    def on_alvfever(self, event):
        self.obj_link('alvchbxfever', event.IsChecked())

    def on_ripfever(self, event):
        self.obj_link('ripchbxfever', event.IsChecked())

    def on_exit(self, event):
        self.Close()

    #-----------------------------------------------------------------------------------------------
    ##### gridbagsizer #####
    #-----------------------------------------------------------------------------------------------
    """
    TODO: add the code for the user selections
    All I have now is just the layout
    """
    def _build_fbgs_grid(self, gbf_panel):
        self.fgbs = wx.GridBagSizer(2, 2)

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

        self.fgbs.Add(one_line_text(self.gbf_panel, "Category", one_char=True),
                 (0,0), flag=idxflags, border=2)
        self.fgbs.Add(one_line_text(self.gbf_panel, "Alvarado (points)", one_char=True),
                 (0,1), flag=idxflags, border=2)
        self.fgbs.Add(one_line_text(self.gbf_panel, "RIPASA (points)", one_char=True),
                 (0,2), flag=idxflags, border=2)

        # table first column
        self.fgbs.Add(one_line_text(self.gbf_panel, "Demographics"),
                 (1, 0), flag=idxflags, border=2)
        self.fgbs.Add(one_line_text(self.gbf_panel, "Laboratory findings"),
                 (2, 0), flag=idxflags, border=2)
        self.fgbs.Add(one_line_text(self.gbf_panel, "Signs"),
                 (3, 0), flag=idxflags, border=2)
        self.fgbs.Add(one_line_text(self.gbf_panel, "Symptoms"),
                 (4, 0), flag=idxflags, border=2)
        self.fgbs.Add(one_line_text(self.gbf_panel, "Cutoff Score"),
                 (5, 0), flag=idxflags, border=2)


        # table second column
        self.fgbs.Add(one_line_text(self.gbf_panel, "- - -"),
                 (1, 1), flag=idxflags, border=2)

        alvchbxWBCsizer=wx.BoxSizer(wx.VERTICAL)
        self.alvleuk = wx.CheckBox(self.gbf_panel, -1, "Leukocytosis(2)", name='alvckbxwbc')
        alvchbxWBCsizer.Add(self.alvleuk)
        self.obj_links["alvckbxwbc"] = "ripchbxwbc"
        self.alvleuk.Bind(wx.EVT_CHECKBOX, self.on_alvleuk)

        alvchbxWBCsizer.Add(wx.CheckBox(self.gbf_panel, -1, "Left shift (1)", name='alvckbxleftshift'))
        self.fgbs.Add(alvchbxWBCsizer, (2, 1), flag=idxflags, border=2)

        alvchbxsgsizer = wx.BoxSizer(wx.VERTICAL)
        self.alvfever = wx.CheckBox(self.gbf_panel, -1, 'Fever (1)', name='alvchbxfever')
        alvchbxsgsizer.Add(self.alvfever)
        self.obj_links["alvchbxfever"] = "ripchbxfever"
        self.alvfever.Bind(wx.EVT_CHECKBOX, self.on_alvfever)

        alvchbxsgsizer.Add(wx.CheckBox(self.gbf_panel, -1, 'Rebound pain (1)', name='alvchbxrebound'))

        alvchbxsgsizer.Add(wx.CheckBox(self.gbf_panel, -1, 'RLQ tenderness(2)', name='alvchbxrlq'))

        self.fgbs.Add(alvchbxsgsizer, (3, 1), flag=idxflags, border=2)

        alvchbxsymsizer = wx.BoxSizer(wx.VERTICAL)
        alvchbxsymsizer.Add(wx.CheckBox(self.gbf_panel, -1, 'Anorexia (1)', name='alvchbxanorexia'))
        alvchbxsymsizer.Add(wx.CheckBox(self.gbf_panel, -1, 'Migration of pain (1)', name='alvchbxmig' ))
        alvchbxsymsizer.Add(wx.CheckBox(self.gbf_panel, -1, 'Nausea or vomiting (1)', name='alvchbxnausea'))
        self.fgbs.Add(alvchbxsymsizer, (4, 1), flag=idxflags, border=2)


        ##################
        # table third column

        riprbsizer = wx.BoxSizer(wx.VERTICAL)
        riprbsizer.Add(wx.RadioButton(self.gbf_panel, -1, "Age <= 40 (1)", style=wx.RB_GROUP, name='riprbage'))
        riprbsizer.Add(wx.RadioButton(self.gbf_panel, -1, "Age > 40 (0.5)", name='riprbage'))
        riprbsizer.Add(wx.StaticText(self.gbf_panel, -1, "- - - "))
        riprbsizer.Add(wx.RadioButton(self.gbf_panel, -1, "Gender: Female (0.5)", style=wx.RB_GROUP, name='riprbsex'))
        riprbsizer.Add(wx.RadioButton(self.gbf_panel, -1, "Gender: Male (1)", name='riprbsex'))
        self.fgbs.Add(riprbsizer,(1, 2), flag=idxflags, border=2)

        ripchbxwbcsizer = wx.BoxSizer(wx.VERTICAL)
        self.ripleuk = wx.CheckBox(self.gbf_panel, -1,  'Leucocytosis (1)', name="ripchbxwbc")
        ripchbxwbcsizer.Add(self.ripleuk)
        self.obj_links["ripchbxwbc"] = "alvckbxwbc"
        self.ripleuk.Bind(wx.EVT_CHECKBOX, self.on_ripleuk)

        ripchbxwbcsizer.Add(wx.StaticText(self.gbf_panel, -1,  '- - - '))
        ripchbxwbcsizer.Add(wx.CheckBox(self.gbf_panel, -1,  'Neg. Urinalysis (1)', name='uaWNL' ))
        self.fgbs.Add(ripchbxwbcsizer,(2, 2), flag=idxflags, border=2)

        ripchbxsgsizer = wx.BoxSizer(wx.VERTICAL)
        self.ripfever = wx.CheckBox(self.gbf_panel, -1, 'Fever (1)', name='ripchbxfever')
        ripchbxsgsizer.Add(self.ripfever)
        self.obj_links['ripchbxfever'] = 'alvchbxfever'
        self.ripfever.Bind(wx.EVT_CHECKBOX, self.on_ripfever)

        ripchbxsgsizer.Add(wx.CheckBox(self.gbf_panel, -1, 'Rebound pain (1)', name='ripchbxrebound'))

        ripchbxsgsizer.Add(wx.CheckBox(self.gbf_panel, -1, 'RLQ tenderness (2)', name='ripchbxsgrlq'))

        ripchbxsgsizer.Add(wx.CheckBox(self.gbf_panel, -1, 'Guarding (2)', name='ripchbxsggrd'))
        ripchbxsgsizer.Add(wx.CheckBox(self.gbf_panel, -1, 'Rovsing sign (2)', name='ripchbxsgrs'))
        self.fgbs.Add(ripchbxsgsizer, (3, 2), flag=idxflags, border=2)

        """
        fgbs.Add(wx.TextCtrl(self.gbf_panel, -1, "Anorexia 1\nMigration of pain 1\nNausea & Vomiting 1"
                                            "\nRLQ pain 0.5\nDurations of sx's <= 48hr 1"
                                            "Durations of sx's > 40hr 0.5",
                             style=wx.BORDER_SIMPLE | wx.TE_READONLY | wx.TE_NO_VSCROLL | wx.TE_MULTILINE),
                 (4, 2), flag=idxflags, border=2)
        """
        ripchbxsymsizer = wx.BoxSizer(wx.VERTICAL)
        ripchbxsymsizer.Add(wx.CheckBox(self.gbf_panel, -1, 'Anorexia (1)', name='ripchbxsymanorexia'))
        ripchbxsymsizer.Add(wx.CheckBox(self.gbf_panel, -1, 'Migration of pain (0.5)', name='ripchbxsymmig'))
        ripchbxsymsizer.Add(wx.CheckBox(self.gbf_panel, -1, 'Nausea or vomiting (1)', name='ripchbxsymnausea'))
        ripchbxsymsizer.Add(wx.CheckBox(self.gbf_panel, -1, 'RLQ pain (0.5)', name='ripchbxsymrlq'))
        ripchbxsymsizer.Add(wx.StaticText(self.gbf_panel, -1,  'Duration of symptoms:'))
        ripchbxsymsizer.Add(wx.RadioButton(self.gbf_panel, -1, "<= 48 hours (1)", style=wx.RB_GROUP, name='riprbsmdur'))
        ripchbxsymsizer.Add(wx.RadioButton(self.gbf_panel, -1, "> 48 hours (0.5)", name='riprbsmdur'))
        self.fgbs.Add(ripchbxsymsizer,(4, 2), flag=idxflags, border=2)

        self.fgbs.Add(one_line_text(self.gbf_panel, ">= 7"),
                 (5, 1), flag=idxflags, border=2)
        self.fgbs.Add(one_line_text(self.gbf_panel, ">= 7.5"),
                 (5, 2), flag=idxflags, border=2)
        #table last row
        self.fgbs.Add(wx.TextCtrl(self.gbf_panel, -1, "Note: \n-Leukocytosis is defined as a white bloood cell count > 10,000/ul, "
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

        self.fgbs.AddGrowableCol(0)
        self.fgbs.AddGrowableCol(1)
        self.fgbs.AddGrowableCol(2)
        self.fgbs.AddGrowableRow(6)
        self.fgbs.AddGrowableRow(0)

        self.gbf_panel.SetSizer(self.fgbs)

        return self.gbf_panel

    #-----------------------------------------------------------------------------------------------
    # MENU BAR
    #-----------------------------------------------------------------------------------------------
    def _build_menu(self):
        menu_bar = wx.MenuBar()
        about_menu = wx.Menu()
        citations_menu = wx.Menu()
        help_menu = wx.Menu()

        menu_bar.Append(about_menu, "&About")
        menu_bar.Append(citations_menu, "&Citations")
        menu_bar.Append(help_menu, "&Help")

        self.SetMenuBar(menu_bar)

    #-----------------------------------------------------------------------------------------------
    # bottom button bar
    #-----------------------------------------------------------------------------------------------
    def _build_button_row(self, panel):
        button_row_sizer = wx.BoxSizer(wx.HORIZONTAL)
        """
        button_row_sizer.Add(wx.Button(panel, label="OK"), 0, wx.RIGHT, 10)
        button_row_sizer.Add(wx.Button(panel, label="Cancel"), 0)
        """
        rbox = wx.StaticBox(panel, label="Reports")
        rbox_sizer = wx.StaticBoxSizer(rbox, wx.VERTICAL)

        rbox_sizer.Add(wx.Button(panel, label="Alvardo"), 0, wx.EXPAND, 0)
        rbox_sizer.Add(wx.Button(panel, label="RIPASA"), 0, wx.EXPAND, 0)
        rbox_sizer.Add(wx.Button(panel, label="Both"), 0, wx.EXPAND, 0)
        button_row_sizer.Add(rbox_sizer, 1, 5)

        obox = wx.StaticBox(panel, label="Options")
        obox_sizer = wx.StaticBoxSizer(obox, wx.VERTICAL)

        #obox_sizer = wx.BoxSizer(wx.VERTICAL)
        obox_sizer.Add(wx.Button(panel, label="Reset"), 0, wx.EXPAND, 0)
        obox_sizer.Add(0, 25)
        exit_but=wx.Button(panel, label="Exit")
        exit_but.Bind(wx.EVT_BUTTON, self.on_exit)
        obox_sizer.Add((exit_but), 0, wx.EXPAND, 0)
        button_row_sizer.Add(obox_sizer, 1, 5)

        return button_row_sizer


if __name__ == "__main__":
    app = wx.App()
    mainFrame = MainFrame()
    mainFrame.Show()
    app.MainLoop()
