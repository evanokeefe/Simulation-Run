### Steps to Run the sim_script.py Script:
1. Download the script, plan, and run files
1. Unzip the run files folder
1. ssh into the CHTC server
1. Change directory to where you want the output directories to be created
1. Confirm python is installed on ther server
    1. Run: `python3 --version`
    1. Version should be 3.6 or higher
    1. If the version is not correct: follow these [steps](http://chtc.cs.wisc.edu/python-jobs.shtml) from CHTC 
1. Using your preffered FTP protcol: transfer the three files onto the server
1. Use the command: `python3 sim_script_v3.py`
    1. Expect it to take appox. 5 min per run to submit to the condor queue
1. Once the script finishes, the command line will reopen and use `condor_q` to check status of your runs
1. When the queue is run through, confirm output data is in the number directories
1. Run extract_data.py script to process
