DLX_Sim
=======

Simulator für die DLX-Architektur geschrieben in Python.

gui
====
- GUI.py						    Enthält die Klasse ControllMainWindow und die Implementierung verschiedener GUI-Aktionen z.B. die Ausführung von Einzel- oder Mehrschritten
- MainWindow.py				Enthält die Klasse Ui_MainWindow.
- mainwindow.ui	                Mit QtCreator erzeugte Datei. Das Hauptfenster.
- mainwindow_alternativ.ui
- Models.py						 Enthält die Klassen Model, ProgramModel, PipelineModel, MemoryModel und RegisterModel.

src
===
- DLX_ALU.py:					Enthält die Klasse DLX_ALU und die Implementierung der DLX ALU.
- DLX_Pipeline.py				Enthält die Klasse DLX_Pipeline und die Implementierung der DLX Pipeline.
- DLX_Register.py				Enthält die Klassen DLX_Register, DLX_Register0 und DLX_Reg_Bank und die Implementierung der Pipeline Register.
- DLX_Speicher.py				Enthält die Klasse DLX_Speicher und die Implementierung der lese und schreibe Operationen des DLX Speichers.
- DLX_Translator.py		    Enthält die Klassen DLX_Translator und DLX_Disassembly und eine implementierung zum übersetzten den Maschinencodes.
- Sim.py						    Enthält die Klasse Simulator und enthält die Implementierung der Dateieinlesefunktion und der Pipeline Steuerung.

test
====
- IntegTestPipeline.py			    Enthält die Klasse TestCasesPipe und die Implementierung eines Pipelinetests.
- IntegTestPipeline_EX.py		Enthält die Klasse TestCasesPipe_EX und die Implementierung eines Tests der EX-Stufe der Pipeline.
- IntegTestPipeline_ID.py		Enthält die Klasse TestCasesPipe_ID und die Implementierung eines Tests der ID-Stufe der Pipeline.
- IntegTestPipeline_IF.py		Enthält die Klasse TestCasesPipe_IF und die Implementierung eines Tests der IF-Stufe der Pipeline.
- IntegTestPipeline_MEM.py	Enthält die Klasse TestCasesPipe_MEM und die Implementierung eines Tests der MEM-Stufe der Pipeline.
- IntegTestSim.py				    Enthält die Klasse TestCasesSim und die Implementierung eines Tests von Simulator und Pipeline.
- logging.conf					
- test.dlx	
- UnitTestRunner.py				
- UnitTestsALU.py				Enthält die Klasse TestCasesALU und die Implementierung eines Tests der DLX_ALU.
- UnitTestSim.py				Enthält die Klasse TestCasesSim und die Implementierung eines Tests des Simulators.
- UnitTestReg.py				Enthält die Klasse TestCasesReg und die Implementierung eines Tests der DLX_Register.


Ausführung und Verwendung des Programms
=======================================
Im DLX_Sim_deploy.zip befindet sich die unter Windows ausführbare Datei des DLX_Simulators. Nach dem Entpacken muss die Datei DLX_Sim.exe ausgefürht werden. 

Nach dem Start des Programms kann im Menü 'DLX_Sim' mit 'Load Program' ein neues Programm in den Simulator geladen werden.
Im Menüpunkt Simulator können nun mehrere oder einzelne Schritte ausgeführt werden. Um den Simulator zurückzusetzen
befindet sich im Menüpunkt DLX_Sim die Funktion Reset DLX.

