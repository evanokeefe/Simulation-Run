import os, sys

def tar_to_group(sim_dir, dest):
    cwd = os.getcwd()
    sim_path = os.path.join(cwd, sim_dir)
    rm = ["EffProperty.exe", "multiple-batch.sh", "parameter.in", "run_single.sh", "Structure.f90", "submit-single.sub"]
    keep = ['effElectricalConductivity.dat', 'struct.in']

    for file in sorted(os.listdir(sim_path)):
        file_path = os.path.join(sim_path, file)
        if file in rm:
            os.remove(file_path)
        elif file[:6] == "number":
            num_dir = os.path.join(sim_path, file)
            for sub_file in os.listdir(num_dir):
                sub_path = os.path.join(num_dir, sub_file)
                if sub_file not in keep:
                    if sub_file[0] == '.':
                        continue
                    os.remove(sub_path)
    f_tar = f'tar -czf {sim_dir + ".tar.gz"} {sim_path}'
    os.system(f_tar)
    move = f'mv {sim_path + ".tar.gz"} {dest}'
    os.system(move)
    return print('file moved')
    
dir_name = 'to_process'
group = os.path.join(' ', 'mnt', 'gluster', 'groups', 'hu_group_mse', dir_name)[1:]  

for arg in sys.argv[1:]:
    print(arg)
    tar_to_group(arg, group) 
