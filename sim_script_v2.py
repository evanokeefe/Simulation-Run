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
    begin = s[:207]
    mid = s[207:228]
    end = s[228:]

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
    return path

def run_sim(plan, username, hostname, out_path):
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
        shape = run["shape"][0]
        a1, a2, a3 = run["a1"], run["a2"], run["a1"]
        b1, b2, b3 = run["b1"], run["b2"], run["b1"]
        lower, upper, step = int(run["lower"]), int(run["upper"]), int(run["step"])

        num_of_structures = (upper-lower)/step
        num_of_jobs = num_of_structures / 20
        
        while num_of_jobs > 0:
            print(lower, upper, num_of_jobs)
    
            if (lower + (step * 20)) < upper:
                middle = lower + (step * 20)
                path = send_job(shape, a1, a2, a3, b1, b2, b3, lower, middle, step)
                lower = middle
                num_of_jobs += -1
            else:
                path = send_job(shape, a1, a2, a3, b1, b2, b3, lower, upper, step)
                dir_name = os.path.basename(path)
                
                compressed =f"tar -zcvf {dir_name}.tar.gz {path}"
                os.system(compressed)
                
                #scp = f"scp {username}@{hostname}:/home/{username}{path} ./{out_path}"
                #os.system(scp)
                
                remove = f"rm -r {path}"
                os.system(remove)
                num_of_jobs = 0
                
run_sim("sim_plan.csv", "eokeefe3", "submit2.chtc.wisc.edu", "programming/MSE_299")
