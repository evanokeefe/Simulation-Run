import os, csv, shutil, time
import pandas as pd

def get_conductivity(num_dir):
    path = os.path.join(num_dir, 'effElectricalConductivity.dat')
    with open(path, 'r') as f:
        matrix = []
        for line in f:
            matrix.append(line.split())
        
        diag = []
        for n in range(3):
            for m in range(3):
                if m == n:
                    diag.append(float(matrix[n][m]))
        out = sum(diag)/len(diag)
        return out
    

def get_concentr(num_dir):
    path = os.path.join(num_dir, 'struct.in')
    with open(path, 'r') as f:
        data = f.read(95)
        matrix = data[69:75]
        interface = data[79:85]
        filler = data[89:95]
        return [matrix, interface, filler]

def rename_remove(src, dest, num):
    if num < 100:
        if num < 10:
            num = '00' + str(num)
        else:
            num = '0' + str(num)
    name = f'struct_{num}.in'
    dest = os.path.join(dest, name)
    src = os.path.join(src, 'struct.in')
    shutil.copyfile(src, dest)
    with open(dest, 'r+') as f:
        f.readline()
        data = f.read()
        f.seek(0)
        f.write(data)
        f.truncate()

def get_params(sim_dir):
    path = os.path.join(sim_dir, 'param.in')
    with open(path, 'r') as f:
        out = []
        for line in f:
            for param in line.split():
                out.append(param)
    return out[1:]
        
def write_data(base_dir, sim_dir, num):
    d = {}
    header = ["number of particles", "matrix", "interface", "filler", "conductivity"]
    params = ['a1', 'a2', 'a3', 'b1', 'b2', 'b3']
    for param in params:
        d[param] = []
    for col_name in header:
        d[col_name] = []
    
    last = None
    for file in sorted(os.listdir(sim_dir)):
        if file[:6] != "number":
            continue
        else:
            num_dir = os.path.join(sim_dir, file)
            num_part = file[7:]
            d['number of particles'].append(num_part)
            d["conductivity"].append(get_conductivity(num_dir))
            d["matrix"].append(get_concentr(num_dir)[0])
            d["interface"].append(get_concentr(num_dir)[1])
            d['filler'].append(get_concentr(num_dir)[2])
            
            if last == None:
                vals = get_params(sim_dir)
                for idx, param in enumerate(params):
                    val = vals[idx]
                    d[param].append(val)
            else:
                for param in params:
                    d[param].append('')
            
            
            rename_remove(num_dir, os.path.join(base_dir, 'neural_input', 'structure'), num)
            num += 1 
            
        last = ""
            
    return d, num
                           
def extract(base_dir, group_dir):
    start = time.time()
    if os.path.exists('neural_input') != True:
        os.mkdir('neural_input')
        os.mkdir(os.path.join('neural_input','structure'))
    
    num = 0
    dict_list = []
    process = os.path.join(group_dir, 'to_process')
    for file in sorted(os.listdir(process)):
        prefix = ['c_a1', 's_a1']
        file_pre = file[:4]
        if file.endswith('.tar.gz') == True:
            if  file_pre not in prefix:
                continue
            else:
                data = os.path.join(base_dir, 'data')
                src = os.path.join(process, file)
                dest = os.path.join(data, file)
                shutil.copyfile(src, dest)
                
                f_tar = f'tar -C {data} -xzf {dest}'
                os.system(f_tar)
                remove = f"rm -r {dest}"
                os.system(remove)
                
                file = file[:-7]
                path = os.path.join(base_dir, 'data', file)
                
                d, num = write_data(base_dir, path, num)
                dict_list.append(d)
                
                dest = os.path.join(data, file)
                remove = f"rm -r {dest}"
                os.system(remove)
    
    d0 = dict_list.pop(0)
    for dic in dict_list:
        for key in dic:
            d0[key].extend(dic[key])
    
    df = pd.DataFrame(d0)
    df.to_csv(os.path.join('data', 'Microstructure Data.csv'), encoding='utf-8', index=False)
    cond = df['conductivity']
    cond.to_csv(os.path.join('neural_input', 'conductivity.csv'), encoding='utf-8', index=False)
    
    
    if dict_list == []:
        end = time.time()
        print('ran in', round(end-start, 2), 'seconds')
        return print('No data found')
    else:
        os.system('tar -czf neural_input.tar.gz neural_input')
        name = 'neural_input_00'
        dest = os.path.join(group, name + '.tar.gz')
        while os.path.exists(dest):
            val = int(name[-2:])+1
            if val < 10:
                name = f'neural_input_0{str(val)}.tar.gz'
            else:
                name = f'neural_input_{str(val)}.tar.gz'
            dest = os.path.join(group, name + '.tar.gz')
            
        shutil.copyfile('neural_input.tar.gz', os.path.join(group, name))
        os.system("rm neural_input.tar.gz")
        end = time.time()
        print('ran in', round(end-start, 2), 'seconds')
        return print('CSV files generated')


    
group = os.path.join(' ', 'mnt', 'gluster', 'groups', 'hu_group_mse')[1:]    
extract(os.getcwd(), group)
