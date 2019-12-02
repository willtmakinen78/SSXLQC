SSXLQC Install, Setup and Usage Instructions

INSTALLATION:

	Ensure that python 3.7 has been installed and added to the PATH environment variable. 
	A reboot must be performed for any changes to take effect.

	Fully unzip/extract the SSXLQC-x.x.x.tar.gz file, so that a plain SSXLQC-x.x.x folder is created.

	Open a command/PowerShell window at path\to\folder\SSXLQC-x.x.x\ssxlqc. Locate the requirements.txt file.

	Run the following command:
	
		pip install -r requirements.txt
		
	This will install all the necessary 3rd-party packages
	test
	
	NOTE: an internet connection is required.

	If you would like to install the SSXLQC package under your python distribution, and have access
	to all the package's modules from any other python script on the system, back up the terminal one
	levels to path\to\folder\SSXLQC-x.x.x. Ensure that a setup.py file is visible.

	Run the following command:
	
		python setup.py install
		
	Now the modules will be accessable from anywhere on the system.
	
	The OPEX PerfectPick/SSXL and ELMO Composer software must also be installed on the system. Once
	done, pin the SSXL icon directly to the right of the start button, and the ELMO Composer icon to
	the right of the SSXL icon.
	
	Ensure that the ELMO test scripts, SSXL_Track_Test.ehl and SSXL_Conveyer_Test.ehl are 
	copied to the QC computer. Th exact location does not matter (see USAGE for details). Current loc:
	
		"C:\\Users\\Opex\\My Documents\\QC Automation\\ELMO Programs"
		
	Finally, schedule the autobackup of files using Windows Task Scheduler. Use the sample:
		
		path\to\folder\SSXLQC-x.x.x\SSXL_Auto_Backup.cmd
		
	replacing "path\to\data\location" and "path\to\backup\location" with the proper paths. Schedule
	this cmd file to run as often as you like at a convenient time.


SETUP:

	Navigate to path\to\folder\SSXLQC-x.x.x\ssxlqc and locate/open the run.py file
	
	Modify the second line that looks like:
	
		sys.path.append("path\to\folder\SSXLQC-x.x.x")
		
	To contain the path to the root folder of the package.
	NOTE: if you installed SSXLQC using setup.py, this is not strictly necessary and can be commented 
	out/deleted, however updating it cannot hurt and if the filepath does not exist errors will occur.
	
	Then identify the three lines of the form:
	
		rf_loc = "path\\to\\folder\\SSXLQC-x.x.x\\ssxlqc\\data\\rf"
		track_loc = "path\\to\\folder\\SSXLQC-x.x.x\\ssxlqc\\data\\track"
		conveyer_loc = "path\\to\\folder\\SSXLQC-x.x.x\\ssxlqc\\data\\conveyer"
		
	To point to the upload locations of the log files. These folders will be monitored for changes 
	and analysis performed when new files appear.
	
	The above locations can be changed to point to wherever is suitable, however each folder above
	must contain a subfolder called summary, which itself contains a file of the form:
	
		iBot_Type_Summary.csv
		
	Formatted exactly as it was when the package was first downloaded and unzipped, where type is
	rf or track or conveyer.
	
	If it is desireable to remove old entries from these files, the .csvs can be  opened using excel
	and the unwanted rows removed, after which any remaining rows should be cut and pasted to remove
	any blank lines between the header/statistic rows and the data rows.
	
	DO NOT remove columns or modify the header or statistic rows! The program will fail if these are 
	not in their exact locations. Additionally, always leave at least two rows of data. If a fresh
	file is desired with no past data, run the package on two new trials, then delete all the old 
	data rows and shift the newet ones up to the top. 
	
	Next identify the following line, just below the three previously modified:
	
		perfectpick_logs_loc = "C:\\OPEX\\PerfectPick\\Logs"
		
	Change it to match the default log save location of the perfect pick logs (if using the QC PC,
	there should be a shortcut to here on the desktop - the correct location should be set by 
	default). After each rf lifetest, the latest log file will automatically be copied from here to 
	the rf_loc folder specified earlier, where analysis will be performed.
	
	The GUI automation tool used to automatically click around is somewhat a hack in that it simply
	clicks and points to hard-coded points on the screen, requiring icons to be pinned to specific 
	locations on the screen (SSXL closest to the start menu, ELMO Composer to its right), and that 
	any windows opened are always maximized (nothing to worry about here, this is the default 
	behavior of the programs). The hard-coded values should work on most systems with 1080p screens
	and 100% Windows scaling, given a 25 +- 5in screen. Past that, however, the values coded may not
	work past this range.
	
	If the mouse clicks are inaccurate, run the program:  
	
		path\to\folder\SSXLQC-x.x.x\tests\mousecoords.py
		
	It will print to the console the (x, y) location of the cursor as well as its xy-percentage.
	Use theser outputs to modify the 
		
		path\to\folder\SSXLQC-x.x.x\ssxlqc\autogui\TYPEauto.py 
		
	files with the correct values for the specific screen. Any number of additional clicks/procedures
	can also be added to this script, fillowing the format of the rest of the code.
	
	Save everything and it is time to begin analysis
	
	
USAGE:
	
	Navigate to path\to\folder\SSXLQC-x.x.x and run the batch script:
	
		SSXLQC.bat
		
	This script will not work if it is moved around or python has not been added to the PATH environment
	variable, however a shortcut can be made to it and places anywhere on the system.
	
	This will begin the folder monitors. Any time a log file of the correct format is uploaded to one
	of the designated folders, the analysis will automatically begin, each time updating the control
	charts located at path\to\folder\SSXLQC-x.x.x\ssxlqc\data\TYPE\charts.
	
	Note that any time a file is uploaded, the respective summary/chart file will be overwritten, so
	if it is desired that this data is preserved, it should either be moved out of the charts folder
	or renamed.
	
	To automate the above processes, use the gui window that pops up. The available parameters are:
	
		iBot #: the iBot being tested
				NOTE: no default, tests will not run with invalid input (negative #, non-numeric
				chars, etc). Error message will appear on console, retype and clock start again.
				If more than 5 digits are entered, the 5 least-significant ones will be used.
		
		Run Time: how long in minutes to run the test for (only relevant for rf tests, the track 
				  and conveyer tests are canned and run for a set period of time)
				  NOTE: default of 10 mins, will not run with invalid input
				  
		# Trials: how many consecutive of the chosen tests to run (again, only relevant for rf tests,
				  however can still be used on track/conveyer tests).
				  
		Calc #: the number of previous trials to calculate the control charts' average and standard
				deviation from
				NOTE: default of 50, inputs saved with 'Update Point #s' button are saved to config
					  file located at: path\to\folder\SSXLQC-x.x.x\ssxlqc\chart\chartconfig.ini. This
					  can be edited manually at any time. Each time software is restarted, the saved
					  values will be used
		
		Show #: the number of previous trials that will be shown on the control charts and have Nelson
				rules applied to them.
				NOTE: same as Calc #
				
		Start: clicking any of these 3 buttons starts the gui automation tool. Select the test type from
			   the list and it back and let the test run to completion
			   NOTE: An error will show on the console if any of the inputted parameters are invalid or
					 if there is no test selected when start is pressed.
					
		Update Point #s: will save the Calc # and Show # entries to a config file
						 NOTE: config located at 
							   path\to\folder\SSXLQC-x.x.x\ssxlqc\chart\chartconfig.ini
							   
		Scrub Last Trial: Removes the last trial of the selected TYPE from the data set
						  NOTE: will not update charts, have to upload a log file first for updates to 
								occur. An error will show on the console if there is no test selected.
								This can also be done MANUALLY. Simply open up the relevent summary file
								and delete the offending row. Make sure to shift everything below is up
								one row if the romoved row is not at the bottom.
	
	Make sure that the iBot is in the lifetester/rotissery, power is applied, the rf receiver/serial 
	connection is in place, and that the guardian box is plugged in (serial tests only) before hitting
	start!
	
	Before running any automated test, go through all the motions at least once manually. This will
	identify any errors outside of the automation script, as well as set the last open location to 
	the location of the .ehl ELMO scripts for the track/conveyer tests (ESSENTIAL - the auto GUI 
	sequence does not look to a specific path, it assumes they are in the last-opened folder). The 
	automation script does not take differnt save locations into account, so make sure to always 
	reset the last save location to the QC automation location if different ones were used in between 
	automatic runs.
	
	FINAL NOTE: the SSXL OPEX software must be logged into first (pwd: snowman). This was not
	hard-coded to allow for different passwords/users. Additionally, both the SSXL and ELMO composer
	windows must be maximized.
	
	Once the test is running, DO NOT TOUCH ANYTHING ON THE COMPUTER. The gui automation tool assumes
	things are in certain places, and clicking around/moving windows around can and will mess things
	up. A more robust solution can hopefully be implemented in the future.
	
	
THEORY OF OPERATION:

	This package automates the data collection and analysis of three different QC tests, to be
	performed on completed R20 iBots: life tests (dubbed "rf" tests due to the rf transceiver used
	to collect data), track tests, and conveyer tests.
	
	The rf tests monitor 26 different parameters as the bot is run for a user-deterined amount of 
	time, ranging from electronics temperatures to the bot's following errors at various points in 
	the loop (the exact parameters that are collected can be seen by viewing the 
	path\\to\\folder\\SSXLQC-x.x.x\\ssxlqc\\data\\rf\\summary\\iBot_RF_Summary.csv file). In the 
	summary file, all the maximums of each parameter are recorded, so that they can be compared
	against each other. Each time a new trial is run, this file and the control charts, where the
	average and standard deviations are determined from all of the maximumns and nelson rules are
	applied.
	
	The track and conveyer tests are fairly similar, however it is the averages and standard
	deviations that are compared, not the maximums, as well as each parameter's average + 3 
	standard deviations. The control charts are then generated from the average and standard
	deviations of these averages + 3 standard deviations.
	
	When the SSXLQC package as a whole is run as a single module as is described above, two primary
	operations are performed: a GUI automation tool is used to automatically click around the 
	various GUI-based to actually collect the data, after which an analysis routine is performed
	to summarize each trial and update the control charts. 
	
	Everything is initiated from the 
	
		path\\to\\folder\\SSXLQC-x.x.x\\ssxlqc\\run.py
	
	file, which is what is run when the package as a whole is executed as a module. This takes care 
	of launching all the folder monitoring in separate background processes as well as creating the 
	GUI dialogue box which starts the GUI automation.
	
	GUI AUTOMATION:
		
		The logic for this component is all located in the 
			
			path\\to\\folder\\SSXLQC-x.x.x\\ssxlqc\\autogui
			
		sub-package, which contains the rfauto.py and serialauto.py modules. These modules simply
		use the pyautogui package to perform a series of mouseclicks and keypresses tp run the
		tests. Delays have been built in to allow for various elements to load, and can change if 
		different execution speeds are desired. As said earlier, the exact mouseclick locations 
		may have to be updated as the screen sizes change, UI elements are updated, etc.
		
	DATA ANALYSIS:
	
		Data analysis is performed using the unpack, sum, and chart sub-packages, as well as the data
		folder. Each package is explained below:
		
		UNPACK:
		
			Each unpack module (rfdata.py, trackdata.py, conveyerdata.py) contains a class that performs
			the relevent analysis for that module's data type (most of the "heavy lifting" is done here). 
			Look through each one's implementation; they are all capable of doing a lot more analysis 
			than is used in the control charts( averages for absolute and true values, standard deviations,
			etc). It is also easy to add additional analysis methods as needed. The full analysis using
			every parameter is written to a raw_input_name_Summary.csv file each time a raw data file is
			uploaded.
			
			The most important methods of each TYPEdata.py file are the unpack() and get_summary()
			methods. The unpack() method parses the raw files of each test type, placing the data
			into lists that are easier to deal with. The get_summary() method returns a single list
			containing the most important information from each trial, which is then used by other
			packages in other stages of analysis
			
		SUM:
			
			The sum modules take the single-line summary from the TYPEData classes and summarizes them into
			the iBot_TYPE_Summary.csv files. Each module contains three classes: TYPESummary, _Watcher, 
			and _TYPEHandler. The latter two are private and are responisble for monintoring the data 
			file locations specified earlier (_Watcher) and actually doing the parsing/file writing 
			(_TYPEHandler). The public TYPESummary class is what is actually used by other modules, and
			simply starts up the _Watcher with the method summarize()
			
			The _TYPEHandler class does most of the work. It is what actually calls the unpack() and 
			get_summary() methods from the unpack modules, and is called upon by the _Watcher class. 
			Once a file as been uploaded to the watched folder, it ensures it has the correct filename 
			format using a regular expression, reads in the existing data from the iBot_Type_Summary.csv
			file, appends the summary information of the final trial, finally re-saving the updated 
			version.
			
			Finally, the relevent data is passed to the chart module for graphing.
			
		CHART:
			
			This package conatains two modules, chart.py and nelsonrules.py. chart.py does all the work
			in terms of parsing the input data from the sum package and displaying the control charts,
			while nelsorules.py determines which trials have violated any Nelson Rules. nelsonrules.py
			should not have to be touched at all, however there are a few of things that one might to 
			edit in chart.py.
			
			Within chart.py are two mostly identical methods, plotAll() and plotSeparate(). The difference
			between the two is that plotAll() will generate all the graphs in a single view, while
			plotSeparate() will save each parameter's control chart separately. The arguments of each
			method are identical explained below:
			
			data: the 2D list containig all the summary lines from iBot_Type_Summary.csv, created and 
				  formatted by the TYPEsum.py modules.
			
			title_line: a 1D list containing the titles of each parameter/control chart, generated by 
						the TYPEsum.py modules
						
			start_col: each iBot_Type_Summary.csv file has leading rows containing each trial's name,
					   date and time. These are not relevent for the control charts, so this lets you
					   skip over these first few columns
					   
			multiple: the track anc conveyer summary files contains the average, standard devition, and 
					  average + 3*std of each parameter. Only the average + 3*stds are relevent for the
					  control chart, so this makes it possible to skip over uneeded data columns.
					  
			show_mode: set to "save" or "show". "save" will save the control charts a png to the 
					   location/charts folder, while "show" will generate a popout window with the charts.
					   
			location: the root directory to save the charts to. A /charts/ directory will be created in
					  this location where the charts will be saved.
					  
			title_strip: the track and conveyer summary files have qualifying information tacked on to the
						 end of their parameter titles that shouldn't show up in the control chart titles.
						 The number entered here will strip that many characters off the end of each col's
						 title.
						 
			rules: a boolean to draw the Nelson Rules vioations (True) or not (False)
			
	
	The run.py module (called upon by the __main__.py) module is responsible for initiating everything.
	After starting the gui window, it starts each sum module in a separate process, so that data files can
	be uploaded to the watched locations and analyzed without having to start any test. Upon clicking a 
	start button, each GUI automation routine is also started in a new process, so that multiple tests
	can be run simulatenously. Clicking the 'x' of the GUI window will terminate all the processes and 
	close everything out.
	
	GENERAL NOTE: Watch the output console, it provides useful insights into what is going on. Additionally,
				  should a fatal failure occur and exiting the GUI window fails to close everything out,
				  pressing ctr-c in this window should guarentee that everything exits.
			
			
			
			
	
	
