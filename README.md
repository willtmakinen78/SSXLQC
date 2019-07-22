# SSXLQC
A python package for automating QC data analysis of OPEX SSXL iBots

# SSXLQC Install, Setup and Usage Instructions

# INSTALLATION:

	Ensure that python 3.7 has been installed and added to the PATH environment variable. 
	A reboot must be performed for any changes to take effect.

	Fully unzip/extract the SSXLQC-x.x.x.tar.gz file, so that a plain SSXLQC-x.x.x folder is created.

	Open a command/PowerShell window at path\to\folder\SSXLQC-x.x.x\ssxlqc. Locate the requirements.txt file.

	Run the following command:
	
		pip install -r requirements.txt
		
	This will install all the necessary 3rd-party packages
	NOTE: an internet connection is required.

	If you would like to install the SSXLQC package under your python distribution, and have access
	to all the package's modules from any other python script on the system, back up the terminal one
	levels to path\to\folder\SSXLQC-x.x.x. Ensure that a setup.py file is visible.

	Run the following command:
	
		python setup.py install
		
	Now the modules will be accessable from anywhere on the system.

# SETUP:

	Navigate to path\to\folder\SSXLQC-x.x.x\ssxlqc and locate/open the run.py file
	
	Modify the second line that looks like:
	
		sys.path.append("path\to\folder\SSXLQC-x.x.x")
		
	To contain the path to the root folder of the package.
	NOTE: if you installed SSXLQC using setup.py, this is not strictly necessary and can be commented 
	out/deleted, however updating it cannot hurt and if the filepath does not exist errors will occur.
	
	Then identify the three lines of the form:
	
		rf_sum = RFSummary("path\\to\\folder\\SSXLQC-x.x.x\\ssxlqc\\data\\rf")
		track_sum = TrackSummary("path\\to\\folder\\SSXLQC-x.x.x\\ssxlqc\\data\\track")
		conveyer_sum = ConveyerSummary("path\\to\\folder\\SSXLQC-x.x.x\\ssxlqc\\data\\conveyer")
		
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
	
	Save everything and it is time to begin analysis
	
# USAGE:
	
	Navigate to path\to\folder\SSXLQC-x.x.x and type the command:
	
		python -m ssxlqc
		
	This will begin the folder monitors. Any time a log file of the correct format is uploaded to one
	of the designated folders, the analysis will automatically begin, each time updating the control
	charts located at path\to\folder\SSXLQC-x.x.x\ssxlqc\data\type\charts.
	
	Note that any time a file is uploaded, the respective summary/chart file will be overwritten, so
	if it is desired that this data is preserved, it should either be moved out of the charts folder
	or renamed.
	
	
