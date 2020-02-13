import os, csv

def get_conductivity(path):
    path = os.path.join(path, 'effElectricalConductivity.dat')
    with open(path, 'r') as f:
        fir = f.readline()
        fir = fir.split()
        sec = f.readline()
        sec = sec.split()
        thr = f.readline()
        thr = thr.split()
        
        matrix = [fir, sec, thr]
        diag = []
        for n in range(3):
            for m in range(3):
                if m == n:
                    diag.append(float(matrix[n][m]))
        out = sum(diag)/len(diag)
        return out
    

def get_concentr(path):
    path = os.path.join(path, 'struct.in')
    with open(path, 'r') as f:
        data = f.read(95)
        matrix = data[69:75]
        interface = data[79:85]
        filler = data[89:95]
        return [matrix, interface, filler]

def write_csv(sim_dir):
    name = (os.path.basename(sim_dir))
    if name[6].isdigit():
        name = name[:7]
    else:
        name = name[:6]
    csv_name = f'{name}_conduct.csv'
    
    with open(csv_name, 'w') as csv_file:
        writer = csv.writer(csv_file, dialect='excel')
        
        header = ["number of particles", "matrix", "interface", "filler", "conductivity"]
        writer.writerow(header)
        
        for file in sorted(os.listdir(sim_dir)):
            if file[:6] != "number":
                continue
            else:
                path = os.path.join(sim_dir, file)
                num = file[7:]
                conduct = get_conductivity(path)
                concent = get_concentr(path)
                row = concent
                row.insert(0, num)
                row.append(conduct)
                writer.writerow(row)

cwd = os.getcwd()
for file in sorted(os.listdir(cwd)):
    prefix = ['c_a1', 's_a1']
    file_pre = file[:4]
    if os.path.isdir(file) == True:
        if  file_pre not in prefix:
            continue
        else:
            path = os.path.join(cwd, file)
            write_csv(path)