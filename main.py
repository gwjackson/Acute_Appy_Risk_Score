# Author: Walker Jackson, MD
# email gwjackson53@gmail.com
# from source material listed in code files
# https://www.aafp.org/afp/2026/0600/pocg-acute-appendicitis-clinical-scoring-systems
# initial commit - 06/22,2026
import webbrowser

# now the main backup before refactoring


import wx
import re
from functools import partial
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
        #print(self.obj_links)
        if src_name in self.obj_links:
            target_name = self.obj_links[src_name]
            target = self.gbf_panel.FindWindowByName(target_name)
            target.SetValue(value)

    # the lists of risk options for each of the 2 scoring systems Alvarado / RIPASA
    alv_list = ['alvleuk', 'alvleft', 'alvfever', 'alvrebound', 'alvrlq', 'alvanorexia', 'alvmig', 'alvnausea']
    rip_list = [
        'riprble40', 'riprbgt40', 'riprbfemale', 'riprbmale',
        'ripleuk', 'ripua', 'ripfever', 'riprebound',
        'riprlq', 'ripgrd', 'riprs', 'ripanorexia', 'ripmig',
        'ripnausea', 'riplrq2', 'riprblt48', 'riprbgt48'
    ]

    # this is just linking common GUI objects where both scoring systems share the same clinical feature
    # no business logic here - see the report function(s) for that
    def on_alvleuk(self, event):
        self.obj_link('alvckbxwbc', event.IsChecked())

    def on_ripleuk(self, event):
        self.obj_link('ripchbxwbc', event.IsChecked())

    def on_alvfever(self, event):
        self.obj_link('alvchbxfever', event.IsChecked())

    def on_ripfever(self, event):
        self.obj_link('ripchbxfever', event.IsChecked())

    def on_alvrebound(self, event):
        self.obj_link('alvchbxrebound', event.IsChecked())

    def on_riprebound(self, event):
        self.obj_link('ripchbxrebound', event.IsChecked())

    def on_alvrlq(self, event):
        self.obj_link('alvchbxrlq', event.IsChecked())

    def on_riprlq(self, event):
        self.obj_link('ripchbxrlq', event.IsChecked())

    def on_alvanorexia(self, event):
        self.obj_link('alvchbxanorexia', event.IsChecked())

    def on_ripanorexia(self, event):
        self.obj_link('ripchbxanorexia', event.IsChecked())

    def on_alvmig(self, event):
        self.obj_link('alvchbxmig', event.IsChecked())

    def on_ripmig(self, event):
        self.obj_link('ripchbxmig', event.IsChecked())

    def on_alvnausea(self, event):
        self.obj_link('alvchbxnausea', event.IsChecked())

    def on_ripnausea(self, event):
        self.obj_link('ripchbxnausea', event.IsChecked())


    # the business logic to collect the score values.
    # following ar RIPASA (points)
    # not using this - will delete these in the near future (tired just now)

    # ?? rename the on_rb_xxx as not really gone to read on click but on report generation ??
    def on_rb_age(self, event):
        radio_selected = event.GetEventObject()
        if "<=" in radio_selected.GetLabel():
            self.rb_age_value = 1
        else:
            self.rb_age_value = 0.5
        print(f'RB age clicked {radio_selected.GetLabel()} and value is {self.rb_age_value}')

    def on_rb_sex(self, event):
        radio_selected = event.GetEventObject()
        if 'Male' in radio_selected.GetLabel():
            self.rb_sex_value = 1
        else:
            self.rb_sex_value = 0.5
        print(f'RB sex clicked {radio_selected.GetLabel()} and value is {self.rb_sex_value}')

    def on_rb_time(self, event):
        radio_selected = event.GetEventObject()
        if ">" in radio_selected.GetLabel():
            self.rb_time_value = 0.5
        else:
            self.rb_time_value = 1
        print(f'RB duration clicked {radio_selected.GetLabel()} and value is {self.rb_time_value}')

    # -----------------------------------------------------------------------------------------------
    ##### generic report -  #####
    # -----------------------------------------------------------------------------------------------
    def risk_score_report(self,list_of_objs, report_name, show_msgbox = True, event=None):
        """
        Generic for the risk reports
        :param list_of_objs: a list of the GUI objects the user clicks created with the creation of each object
        :param report_name: Name of the report Alvarado or RIPASA
        :param event: the click even
        :return: risk_report
        """
        self.targets_list = list_of_objs
        self.risk_report = f'{report_name} Adult Acute Appendicitis Score\nThe Patients risk points are: \n'
        self.risk_score = 0

        for target in self.targets_list:
            widget = getattr(self, target)

            # .GetValue() returns True if checkbox or radiobutton checked / selected
            if widget and widget.GetValue():
                label_text = widget.GetLabel()
                self.risk_report = self.risk_report + label_text + '\n'

                # (?<=\() means "must start with ("
                # (?=\)) means "must end with )"
                # It only captures the number in between them
                match = re.search(r'(?<=\()(\d+\.\d+|\d+)(?=\))', label_text)
                if match:
                    self.risk_score += float(match.group(0))
        self.risk_report = self.risk_report + (f'The Patients risk score is: {self.risk_score}\n'
                                               f'The cutoff score is: {">=7" if report_name == "Alvarado" else ">= 7.5"}\n')

        # Define a helper function to simulate hitting the 'Enter' key
        def timeout_close():
            sim = wx.UIActionSimulator()
            sim.Char(wx.WXK_RETURN)  # Simulates pressing the Enter key


        # copy to the clipboard
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(wx.TextDataObject(self.risk_report))
            wx.TheClipboard.Close()

        if show_msgbox:
            msgbox = wx.RichMessageDialog(self, self.risk_report, f'{report_name} Risk Report', wx.OK| wx.ICON_INFORMATION)

            # Plan to add wx.CallLater to put in an automatic timeout for the messagebox
            msgbox_timer = wx.CallLater(3000,timeout_close)
            msgbox_result = msgbox.ShowModal()

            # Clean up the timer if the user clicked OK manually before 3 seconds
            if msgbox_timer.IsRunning():
                msgbox_timer.Stop()

            msgbox.Destroy()

        return self.risk_report


    # -----------------------------------------------------------------------------------------------
    ##### report - combo -Alvarado / RIPASA #####
    # -----------------------------------------------------------------------------------------------
    def combo_report(self, event=None):
        """
        This just calls the report_score_function twice
        and copies the concatenation of both reports to the clipboard
        :param event: ignored
        :return: None
        """

        self.combo_report = self.risk_score_report(self.rip_list, 'RIPASA', show_msgbox=False)
        self.combo_report = self.combo_report + "\n" + self.risk_score_report(self.alv_list, 'Alvarado', show_msgbox=False)

        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(wx.TextDataObject(self.combo_report))
            wx.TheClipboard.Close()


        # Define a helper function to simulate hitting the 'Enter' key
        def timeout_close():
            sim = wx.UIActionSimulator()
            sim.Char(wx.WXK_RETURN)  # Simulates pressing the Enter key

        msgbox = wx.RichMessageDialog(self, self.combo_report, f'Combo - Risk Report', wx.OK | wx.ICON_INFORMATION)

        # Plan to add wx.CallLater to put in an automatic timeout for the messagebox
        msgbox_timer = wx.CallLater(3000, timeout_close)
        msgbox_result = msgbox.ShowModal()

        # Clean up the timer if the user clicked OK manually before 3 seconds
        if msgbox_timer.IsRunning():
            msgbox_timer.Stop()

        msgbox.Destroy()

    # -----------------------------------------------------------------------------------------------
    ##### menu selection actions #####
    # sadly most of these require a user key
    # reference 1; https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0275427
    # reference 2; https://www.americanjournalofsurgery.com/article/S0002-9610(24)00675-5/abstract
    # reference 3; https://www.annemergmed.com/article/S0196-0644(86)80993-3/abstract
    # reference 4: https://www.sciencedirect.com/science/article/abs/pii/S0735675706004153
    # reference 5; http://www.smj.org.sg/sites/default/files/5103/5103a4.pdf
    # -----------------------------------------------------------------------------------------------

    def on_primary_reference(self, event):
        webbrowser.open('https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0275427')

    def on_reference_1(self, event):
        webbrowser.open('https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0275427')

    def on_reference_2(self, event):
        webbrowser.open('https://www.americanjournalofsurgery.com/article/S0002-9610(24)00675-5/abstract')

    def on_reference_3(self, event):
        webbrowser.open('https://www.annemergmed.com/article/S0196-0644(86)80993-3/abstract')

    def on_reference_4(self, event):
        webbrowser.open('https://www.sciencedirect.com/science/article/abs/pii/S0735675706004153')

    def on_reference_5(self, event):
        webbrowser.open('http://www.smj.org.sg/sites/default/files/5103/5103a4.pdf')



    # -----------------------------------------------------------------------------------------------
    ##### Options buttons #####
    # -----------------------------------------------------------------------------------------------

    def on_reset(self, event=None ):
        print('Reset and start over')

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

        self.alvleft = wx.CheckBox(self.gbf_panel, -1, "Left shift (1)", name='alvckbxleftshift')
        alvchbxWBCsizer.Add(self.alvleft)

        self.fgbs.Add(alvchbxWBCsizer, (2, 1), flag=idxflags, border=2)

        alvchbxsgsizer = wx.BoxSizer(wx.VERTICAL)
        self.alvfever = wx.CheckBox(self.gbf_panel, -1, 'Fever (1)', name='alvchbxfever')
        alvchbxsgsizer.Add(self.alvfever)
        self.obj_links["alvchbxfever"] = "ripchbxfever"
        self.alvfever.Bind(wx.EVT_CHECKBOX, self.on_alvfever)


        self.alvrebound = wx.CheckBox(self.gbf_panel, -1, 'Rebound pain (1)', name='alvchbxrebound')
        alvchbxsgsizer.Add(self.alvrebound)
        self.obj_links["alvchbxrebound"] = "ripchbxrebound"
        self.alvrebound.Bind(wx.EVT_CHECKBOX, self.on_alvrebound)

        self.alvrlq = wx.CheckBox(self.gbf_panel, -1, 'RLQ tenderness(2)', name='alvchbxrlq')
        alvchbxsgsizer.Add(self.alvrlq)
        self.obj_links["alvchbxrlq"] = "ripchbxrlq"
        self.alvrlq.Bind(wx.EVT_CHECKBOX, self.on_alvrlq)

        self.fgbs.Add(alvchbxsgsizer, (3, 1), flag=idxflags, border=2)

        alvchbxsymsizer = wx.BoxSizer(wx.VERTICAL)

        self.alvanorexia = wx.CheckBox(self.gbf_panel, -1, 'Anorexia (1)', name='alvchbxanorexia')
        alvchbxsymsizer.Add(self.alvanorexia)
        self.obj_links['alvchbxanorexia'] = 'ripchbxanorexia'
        self.alvanorexia.Bind(wx.EVT_CHECKBOX, self.on_alvanorexia)

        self.alvmig = wx.CheckBox(self.gbf_panel, -1, 'Migration of pain (1)', name='alvchbxmig' )
        alvchbxsymsizer.Add(self.alvmig)
        self.obj_links['alvchbxmig'] = 'ripchbxmig'
        self.alvmig.Bind(wx.EVT_CHECKBOX, self.on_alvmig)

        self.alvnausea = wx.CheckBox(self.gbf_panel, -1, 'Nausea or vomiting (1)', name='alvchbxnausea')
        alvchbxsymsizer.Add(self.alvnausea )
        self.obj_links['alvchbxnausea'] = 'ripchbxnausea'
        self.alvnausea.Bind(wx.EVT_CHECKBOX, self.on_alvnausea)

        self.fgbs.Add(alvchbxsymsizer, (4, 1), flag=idxflags, border=2)


        ##################
        # table third column

        riprbsizer = wx.BoxSizer(wx.VERTICAL)
        self.riprble40 = wx.RadioButton(self.gbf_panel, -1, "Age <= 40 (1)", style=wx.RB_GROUP, name='riprble40')
        riprbsizer.Add(self.riprble40)
        self.riprble40.Bind(wx.EVT_RADIOBUTTON, self.on_rb_age)


        self.riprbgt40 = wx.RadioButton(self.gbf_panel, -1, "Age > 40 (0.5)", name='riprbgt40')
        riprbsizer.Add(self.riprbgt40)
        self.riprbgt40.Bind(wx.EVT_RADIOBUTTON, self.on_rb_age)

        riprbsizer.Add(wx.StaticText(self.gbf_panel, -1, "- - - "))

        self.riprbfemale = wx.RadioButton(self.gbf_panel, -1, "Gender: Female (0.5)", style=wx.RB_GROUP, name='riprbfemale')
        riprbsizer.Add(self.riprbfemale )
        self.riprbfemale.Bind(wx.EVT_RADIOBUTTON, self.on_rb_sex)

        self.riprbmale = wx.RadioButton(self.gbf_panel, -1, "Gender: Male (1)", name='riprbmale')
        riprbsizer.Add(self.riprbmale)
        self.riprbmale.Bind(wx.EVT_RADIOBUTTON, self.on_rb_sex)

        self.fgbs.Add(riprbsizer,(1, 2), flag=idxflags, border=2)

        ripchbxwbcsizer = wx.BoxSizer(wx.VERTICAL)
        self.ripleuk = wx.CheckBox(self.gbf_panel, -1,  'Leukocytosis (1)', name="ripchbxwbc")
        ripchbxwbcsizer.Add(self.ripleuk)
        self.obj_links["ripchbxwbc"] = "alvckbxwbc"
        self.ripleuk.Bind(wx.EVT_CHECKBOX, self.on_ripleuk)

        ripchbxwbcsizer.Add(wx.StaticText(self.gbf_panel, -1,  '- - - '))

        self.ripua = wx.CheckBox(self.gbf_panel, -1,  'Neg. Urinalysis (1)', name='uaWNL')
        ripchbxwbcsizer.Add(self.ripua)
        self.fgbs.Add(ripchbxwbcsizer,(2, 2), flag=idxflags, border=2)

        ripchbxsgsizer = wx.BoxSizer(wx.VERTICAL)
        self.ripfever = wx.CheckBox(self.gbf_panel, -1, 'Fever (1)', name='ripchbxfever')
        ripchbxsgsizer.Add(self.ripfever)
        self.obj_links['ripchbxfever'] = 'alvchbxfever'
        self.ripfever.Bind(wx.EVT_CHECKBOX, self.on_ripfever)

        self.riprebound = wx.CheckBox(self.gbf_panel, -1, 'Rebound pain (1)', name='ripchbxrebound')
        ripchbxsgsizer.Add(self.riprebound)
        self.obj_links['ripchbxrebound'] = 'alvchbxrebound'
        self.riprebound.Bind(wx.EVT_CHECKBOX, self.on_riprebound)

        self.riprlq = wx.CheckBox(self.gbf_panel, -1, 'RLQ tenderness (2)', name='ripchbxrlq')
        ripchbxsgsizer.Add(self.riprlq)
        self.obj_links['ripchbxrlq'] = 'alvchbxrlq'
        self.riprlq.Bind(wx.EVT_CHECKBOX, self.on_riprlq)

        self.ripgrd = wx.CheckBox(self.gbf_panel, -1, 'Guarding (2)', name='ripchbxgrd')
        ripchbxsgsizer.Add(self.ripgrd)

        self.riprs =  wx.CheckBox(self.gbf_panel, -1, 'Rovsing sign (2)', name='ripchbxrs')
        ripchbxsgsizer.Add(self.riprs)

        self.fgbs.Add(ripchbxsgsizer, (3, 2), flag=idxflags, border=2)

        ripchbxsymsizer = wx.BoxSizer(wx.VERTICAL)

        self.ripanorexia = wx.CheckBox(self.gbf_panel, -1, 'Anorexia (1)', name='ripchbxanorexia')
        ripchbxsymsizer.Add(self.ripanorexia)
        self.obj_links['ripchbxanorexia'] = 'alvchbxanorexia'
        self.ripanorexia.Bind(wx.EVT_CHECKBOX, self.on_ripanorexia)

        self.ripmig = wx.CheckBox(self.gbf_panel, -1, 'Migration of pain (0.5)', name='ripchbxmig')
        ripchbxsymsizer.Add(self.ripmig)
        self.obj_links['ripchbxmig'] = 'alvchbxmig'
        self.ripmig.Bind(wx.EVT_CHECKBOX, self.on_ripmig)

        self.ripnausea = wx.CheckBox(self.gbf_panel, -1, 'Nausea or vomiting (1)', name='ripchbxnausea')
        ripchbxsymsizer.Add(self.ripnausea)
        self.obj_links['ripchbxnausea'] = 'alvchbxnausea'
        self.ripnausea.Bind(wx.EVT_CHECKBOX, self.on_ripnausea)

        self.riplrq2 = wx.CheckBox(self.gbf_panel, -1, 'RLQ pain (0.5)', name='ripchbxsymrlq')
        ripchbxsymsizer.Add(self.riplrq2)

        ripchbxsymsizer.Add(wx.StaticText(self.gbf_panel, -1,  'Duration of symptoms:'))

        self.riprblt48 = wx.RadioButton(self.gbf_panel, -1, "time <= 48 hours (1)", style=wx.RB_GROUP, name='riprbdurlt48')
        ripchbxsymsizer.Add(self.riprblt48)
        self.riprblt48.Bind(wx.EVT_RADIOBUTTON, self.on_rb_time)

        self.riprbgt48 = wx.RadioButton(self.gbf_panel, -1, "time > 48 hours (0.5)", name='riprbdurgt48')
        ripchbxsymsizer.Add(self.riprbgt48)
        self.riprbgt48.Bind(wx.EVT_RADIOBUTTON, self.on_rb_time)

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
    # sadly most of these require a user key
    #-----------------------------------------------------------------------------------------------
    def _build_menu(self):
        menu_bar = wx.MenuBar()
        about_menu = wx.Menu()
        citations_menu = wx.Menu()
        help_menu = wx.Menu()

        menu_bar.Append(about_menu, "&About")
        menu_bar.Append(citations_menu, "&Citations")
        menu_bar.Append(help_menu, "&Help")

        #######################
        # Citations menu
        primary_reference_item = citations_menu.Append(wx.ID_ANY, "&Primary Reference",
                                                       'The AAFP journal article')
        self.Bind(wx.EVT_MENU, self.on_primary_reference, primary_reference_item)

        seperator_item = citations_menu.Append(wx.ID_SEPARATOR)

        referenct_1_item = citations_menu.Append(wx.ID_ANY, "&Reference 1")
        self.Bind(wx.EVT_MENU, self.on_reference_1, referenct_1_item)

        referenct_2_item = citations_menu.Append(wx.ID_ANY, "&Reference 2")
        self.Bind(wx.EVT_MENU, self.on_reference_2, referenct_2_item)

        referenct_3_item = citations_menu.Append(wx.ID_ANY, "&Reference 3")
        self.Bind(wx.EVT_MENU, self.on_reference_3, referenct_3_item)

        referenct_4_item = citations_menu.Append(wx.ID_ANY, "&Reference 4")
        self.Bind(wx.EVT_MENU, self.on_reference_4, referenct_4_item)

        referenct_5_item = citations_menu.Append(wx.ID_ANY, "&Reference 5")
        self.Bind(wx.EVT_MENU, self.on_reference_5, referenct_5_item)

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

        # using partial to inject additional arguments tino the bound function
        self.rp_alvarado = wx.Button(panel, label="Alvardo")
        rbox_sizer.Add(self.rp_alvarado, 0, wx.EXPAND, 0)
        self.rp_alvarado.Bind(wx.EVT_BUTTON, partial(self.risk_score_report, self.alv_list, 'Alvarado', True))

        self.rp_ripasa = wx.Button(panel, label="RIPASA")
        rbox_sizer.Add(self.rp_ripasa, 0, wx.EXPAND, 0)
        self.rp_ripasa.Bind(wx.EVT_BUTTON,  partial(self.risk_score_report, self.rip_list, 'RIPASA'))

        self.rp_both = wx.Button(panel, label="Both")
        rbox_sizer.Add(self.rp_both, 0, wx.EXPAND, 0)
        self.rp_both.Bind(wx.EVT_BUTTON, self.combo_report)

        button_row_sizer.Add(rbox_sizer, 1, 5)

        obox = wx.StaticBox(panel, label="Options")
        obox_sizer = wx.StaticBoxSizer(obox, wx.VERTICAL)

        self.ob_reset = wx.Button(panel, label="Reset")
        obox_sizer.Add(self.ob_reset, 0, wx.EXPAND, 0)
        self.ob_reset.Bind(wx.EVT_BUTTON, self.on_reset)
        obox_sizer.Add(0, 25)

        self.exit_but=wx.Button(panel, label="Exit")
        self.exit_but.Bind(wx.EVT_BUTTON, self.on_exit)
        obox_sizer.Add((self.exit_but), 0, wx.EXPAND, 0)
        button_row_sizer.Add(obox_sizer, 1, 5)

        return button_row_sizer


if __name__ == "__main__":
    app = wx.App()
    mainFrame = MainFrame()
    mainFrame.Show()
    app.MainLoop()
