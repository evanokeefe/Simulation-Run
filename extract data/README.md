### Steps to Run the extract_data.py Script:
1. Download the script
1. ssh into the CHTC server
1. Change directory to where you want the data to be generated
1. Create a directory named 'data' but DO NOT set as current
    1. This is where the output csv file will be returned and files from group folder stored
1. Confirm python is installed on ther server
    1. Run: `python3 --version`
    1. Version should be 3.6 or higher
    1. If the version is not correct: follow these [steps](http://chtc.cs.wisc.edu/python-jobs.shtml) from CHTC 
1. Using your preffered FTP protcol: transfer the script onto the server
1. Use the command: `python3 extract_data.py`
    1. Expect it to take appox. 5 to 10 min to run
1. Once the script finishes, a 'Microstructure Data' csv file should be returned in the data directory
