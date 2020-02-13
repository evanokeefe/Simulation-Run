import os, sys, shutil, time, csv


def send_job(shape, a1, a2, a3, b1, b2, b3, lower, upper, step):
    
    cwd = os.getcwd()
    
    if shape == "s":
        dir_name = f"{shape}_a1_{a1}_b1_{b1}"
    else:
        dir_name = f"{shape}_a1_{a1}_a3_{a3}_b1_{b1}_b3_{b3}"

    try:
        path = os.path.join(cwd, dir_name)
        os.mkdir(path)
        os.chdir(path)
        
    except FileExistsError:
        os.chdir(path)

        # Creating the number file
        # This file has 3 lines the first being the name the following are the parameters of the simulation
        if os.path.exists("number.txt") == False:
            a_line = f"{a1} {a2} {a3}\n"
            b_line = f"{b1} {b2} {b3}"

            f = open("number.txt", "w")
            f.write("number\n")
            f.write(a_line)
            f.write(b_line)
            f.close()

    # Copying over run files from the run_file folder to the simulation folder
    # User must have a "run_files" folder before beginning
    files = ["EffProperty.exe", "multiple-batch.sh", "param.in", "parameter.in", "run_single.sh", "Structure.f90",
             "submit-single.sub"]
    run_files = os.path.join(cwd, "run_files")

    assert os.path.exists(run_files), "run_files folder does not exist in current directory"

    for file in files:
        source = os.path.join(run_files, file)
        destination = os.path.join(path, file)
        if os.path.exists(destination):
            continue
        shutil.copyfile(source, destination)

    os.chdir(path)
    os.system("chmod 777 EffProperty.exe")

    f = open("multiple-batch.sh", "r")

    s = f.read()
    begin = s[:s.find("for")] + "for"
    mid = s[s.find("for")+3:s.find(" i")]
    end = s[s.find(" i"):]

    f.close()

    # Changing upper and lower bounds of the particle range
    bounds = f"(i={lower};i<={upper};i=i+{step})"
    multi_batch = begin + bounds + end

    f = open("multiple-batch.sh", "w")
    f.write(multi_batch)
    f.close()

    os.system("chmod 777 multiple-batch.sh")
    os.system("./multiple-batch.sh")
    os.chdir(cwd)

def run_sim(plan):
    reader = csv.reader(open('sim_plan.csv'))
    data = list(reader)
    keys = data[0]
    vals = data[1:]

    result = []
    for run in vals:
        run = enumerate(run)
        d = {}
        for param in run:
            key = keys[param[0]]
            val = param[1]
            d[key] = val
        result.append(d)
    
    for run in result:
        start = time.time()
        
        shape = run["shape"][0]
        a1, a2, a3 = run["a1"], run["a2"], run["a1"]
        b1, b2, b3 = run["b1"], run["b2"], run["b1"]
        lower, upper, step = int(run["lower"]), int(run["upper"]), int(run["step"])

        num_of_structures = (upper-lower)/step + 1
        
        print("lower:", lower, "upper:", upper,"number of structure to be generated:", num_of_structures)
    
        send_job(shape, a1, a2, a3, b1, b2, b3, lower, upper, step)
        
        end = time.time()
        elapsed = (end - start)/60
        elapsed = round(elapsed, 2)
        print("Simulation runs queued, took", elapsed, "minutes")
                
run_sim("sim_plan.csv")
