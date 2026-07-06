# Clinical Scoring System fo Adults with Acute Appendicitis

### Source material American Family Physician
https://www.aafp.org/afp/2026/0600/pocg-acute-appendicitis-clinical-scoring-systems


This is a Python script to automate the evaluation of Adult patients with possible Acute Appendicitis.

There are multiple scoring systems, two were reviewed in the above citation.  The article by Natasha Pyzocha, DO was
comparing 2 of several scoring systems; Alvarado and RIPASA.

While the RIPASA has improved diagnostic accuracy I have included both in this short application.

You may use one or the other or both.  A short report is generated and presented for review in a dialog.

The report is also placed / saved to the computer's 'clipboard' this allows the user to simple paste (Ctrl+V on windows)
into the documentation they are working on.  The report is a simple text block and may be further
edited by the user once it is pasted into their document. 

It is imagined that the user would launch the script form within what ever documentation system,
EMR, EHR, etc. they are using via a HotKey.  On windows good options are AutoHotKey or an easier to use application
AutoHotKey (on MS Windows systems, but similar tools are available on Lynx or Mac's). 

I am doing this both as a useful tool and as a practice module for learning Python and wxPython

There are only 2 dependencies for this, Python 13.x and wxPython 4.x.  No 'packaging' at this point yet, planning to
figure that out. 

Original creation date 06/21/2026

It very much use as is and at your own risk. 