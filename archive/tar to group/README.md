### Steps to Run the tar_to_group.py Script:
1. Download the script
1. If desired, update the 'dir_name' on line 27 to change the destination of the tar file
1. ssh into the CHTC server
1. Change directory to where simulation output directories are contained
1. Confirm python is installed on ther server
    1. Run: `python3 --version`
    1. Version should be 3.6 or higher
    1. If the version is not correct: follow these [steps](http://chtc.cs.wisc.edu/python-jobs.shtml) from CHTC 
1. Using your preferred FTP protcol, transfer the script onto the server
1. Use the command: `python3 tar_to_group.py Arg1 Arg2...`
    1. Replace 'Args' with names of the simulation directories ex: c_a1_2_a3_2_b1_4_b3_4 
1. The script will remove all but the necessary files and transfer the compressed version to the group directory
