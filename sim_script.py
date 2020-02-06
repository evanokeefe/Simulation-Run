import os, sys, time, shutil

#Confirms current working directory with user
cwd = os.getcwd()
print("Should the simulation folder be created here? ", cwd)

question = input("y/n: ")
question = question.lower()
assert question in ["y", "n"], "Invalid input. Must be y or n"

if question == "n":
    sys.exit("User chose to exit...quitting")

#Takes user input in order to set all parameters for the run
params = ["shape", "a1", "a2", "a3", "b1", "b2", "b3"]
out = {}
print("Setting parameters for the run. Input desired values or type 'q' to quit")
for param in params:
    p = param + ": "
    question = input(p)
    if question == "q":
        sys.exit("User chose to exit...quitting")
    if param is params[0]:
        assert question == "s" or question == "c", "Input was invalid. Shape must be either s or c"
    else:
        try:
            int(question)
        except:
            print("Input was invalid. Parameters must be of type int")
            break
    out[param] = question

print("Paramters set as: ", out)
time.sleep(1)
    

#Setting the variables equal to the input by the user for the parameters and shape    
shape = out["shape"]
a1, a2, a3 = out["a1"], out["a2"], out["a1"]
b1, b2, b3 = out["b1"], out["b2"], out["b1"] 


#Creating the name for the directory that will contain the simulation
if shape == "s":
    dir_name = f"{shape}_a1_{a1}_b1_{b1}"
else:
    dir_name = f"{shape}_a1_{a1}_a3_{a3}_b1_{b1}_b3_{b3}"
    
print("Folder for the run will be named: ", dir_name)
time.sleep(1)

    
#Saves starting directory
#start_dir = copy.copy(os.getcwd())


#Creates path for simulation directory, makes it, and set it as current
try:
    path = os.path.join(cwd, dir_name)
    if dir_name in cwd:
        print("New directory appears to be the same as the current")
        question = input("Continue? (y/n): ")
        question = question.lower()
        assert question in ["y", "n"], "Invalid input. Must be y or n"
        if question == "n":
            sys.exit("User chose to exit...quitting")
    
    os.mkdir(path)
    print("Directory created")
    os.chdir(path)
    time.sleep(1)
    print("Current directory is now: ", path)
    time.sleep(1)
except FileExistsError:
    print("Directory already exisits. Setting as current")
    os.chdir(path)
    time.sleep(1)
    print("Current directory is now: ", path)
    time.sleep(1)
    

#Creating the number file
#This file has 3 lines the first being the name the following are the parameters of the simulation
if os.path.exists("number.txt") == False:
    a_line = f"{a1} {a2} {a3}\n"
    b_line = f"{b1} {b2} {b3}"

    f = open("number.txt", "w")
    f.write("number\n")
    f.write(a_line)
    f.write(b_line)
    f.close()

    print("Number file created")
    time.sleep(1)
    
else:
    print("Number file already exists")
    time.sleep(1)
    
#Copying over run files from the run_file folder to the simulation folder
#User must have a "run_files" folder before beginning
files = ["EffProperty.exe", "multiple-batch.sh", "param.in", "parameter.in", "run_single.sh", "Structure.f90",
        "submit-single.sub"]
run_files = os.path.join(cwd, "run_files")

for file in files:
    source = os.path.join(run_files, file)
    destination = os.path.join(path, file)
    if os.path.exists(destination):
        continue
    shutil.copyfile(source, destination)
    print(file, " was transferred")
print("All run files are present in the directory")
time.sleep(1)
    
#Scrapes Multiple-batch.sh for current number of particle range to run   
os.chdir(path)

f = open("multiple-batch.sh", "r")

s = f.read()
begin = s[:207]
mid = s[207:228]
end = s[228:]

f.close()
print("Current range for number of particle is: ", mid)

question = input("Continue? (y/n): ")
question = question.lower()
assert question in ["y", "n"], "Invalid input. Must be y or n"
if question == "n":
    print("Enter bounds and step of the particle range. ")
    #os.chdir(cwd)
    #sys.exit("User chose to exit...quitting")
    
    lower = input("lower bound: ")
    assert type(int(lower)) == int, "Invalid input. Lower bound must be an int"
    assert len(lower) == 3, "Invalid input. Lower bound must be len 3"
    assert int(lower) >= 0, "Invalid input. Lower bound must be greater than 0"  
    
    upper = input("upper bound: ")
    assert type(int(upper)) == int, "Invalid input. Upper bound must be an int"
    assert len(upper) == 3, "Invalid input. Upper bound must be len 3"
    assert int(upper) > int(lower), "Invalid input. Upper bound must be greater than lower"
    
    step  = input("step: ")
    assert type(int(step ))  == int, "Invalid input. Step must be an int"
    assert len(step ) == 2, "Invalid input. Step must be len 2"
    assert (int(upper)-int(lower)) / int(step) <= 20, "Set bounds such that 20 or less jobs will be submitted"
    
#Changing upper and lower bounds of the particle range
    os.chdir(path)
    bounds = f"(i={lower};i<={upper};i=i+{step})"
    multi_batch = begin + bounds + end

    f = open("multiple-batch.sh", "w")
    f.write(multi_batch)
    f.close()
    
print("Simulation folder created! Transfer to server and run './multiple-batch.sh'")
os.chdir(cwd)

