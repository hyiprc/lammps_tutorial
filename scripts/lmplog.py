import numpy as np

alias = {
    'tpcpu': 't/cpu',
    'spcpu': 's/cpu',
    'cpuremain': 'cpuleft',
    'timeremain': 'timeoutleft',
    'pe': 'poteng',
    'ke': 'kineng',
    'etotal': 'toteng',
    'evdwl': 'e_vdwl',
    'ecoul': 'e_coul',
    'epair': 'e_pair',
    'ebond': 'e_bond',
    'eangle': 'e_angle',
    'edihed': 'e_dihed',
    'eimp': 'e_impro',
    'emol': 'e_mol',
    'elong': 'e_long',
    'etail': 'e_tail',
    'vol': 'volume',
    'dihedrals': 'diheds',
    'impropers': 'impros',
}
ialias = {alias[k]:k for k in alias}

inttyp = [
    'step','elapsed','elaplong','part','atoms',
    'bonds','angles','dihedrals','impropers',
    'nbuild','ndanger'
]


def update_data(output):

    if output['dataline'].strip() == '':
        return

    l = output['dataline'].split()
    output['dataline'] = ''
    key = [k.lower() for k in l[0::3]]
    value = [
        int(v) if k in inttyp else float(v)
        for k,v in zip(key,l[2::3])
    ]

    # record data
    outkey = []
    for k,v in zip(key,value):
        if k in outkey: continue
        if not k in output:
            output.update({k:[]})
        output[k].append(v)
        outkey.append(k)
    output['n'] += 1

    # get key if not exist
    try:
        output['key'][0]
    except:
        output['key'] = outkey
        # link alias keys
        for c in outkey:
            try: output[ialias[c]] = output[c]
            except: continue

    # update min and eq index
    me = {-1:'min',1:'eq'}[output['_']]
    output[f'ix_{me}'][-1][1] = output['n']-1
    if 'step' in output:
        output[f'N{me}'] = sum([
            output['step'][n[1]] - output['step'][n[0]]
            if not n[1] is None else 0
            for n in output[f'ix_{me}']
        ])


def parser(line,self):
    """
    Read data from lammps log file
    """
    line = line.rstrip()

    if line.startswith('LAMMPS '):
        self.data['dataline'] = ''
        for s in ['_','n','Nrun','Nmin','Neq']:
            self.data[s] = 0
        for s in ['ix_min','ix_eq','key']:
            self.data[s] = []

    elif line.startswith('minimize '):
        self.data['ix_min'].append([self.data['n'],None])
        self.data['_'] = -1
        return
    elif line.startswith('run '):
        try: self.data['Nrun'] += int(line.split()[1])
        except: return
        self.data['ix_eq'].append([self.data['n'],None])
        self.data['_'] = 1
        return

    elif line.startswith('Per MPI rank memory allocation '):
        self.data['_'] *= 2
        return
    elif line.startswith('Loop time of '):
        update_data(self.data)
        self.data['_'] = 0
        return

    elif 'ERROR: ' in line:
        print(line.strip())

    if not '_' in self.data or self.data['_'] == 0: return

    # process header
    if ' Step ' in line and ' CPU ' in line:
        if abs(self.data['_']) == 2:
            # mark style to 'multi'
            self.data['_'] = int(0.5*self.data['_'])
        update_data(self.data)
        l = line.split(' Step ')[1].split(' CPU ')
        self.data['dataline'] = \
            f'step = {l[0].split()[0]} cpu = {l[1].split()[1]}'
        return
    elif abs(self.data['_']) == 2:
        self.data['key'] = [s.lower() for s in line.split()]
        self.data['_'] = int(0.5*self.data['_'])
        return

    l = line.split()
    nk = len(self.data['key'])

    # ----- thermo_modify line multi -----
    if (
        ' = ' in line and 
        not line.startswith(' ') and 
        all([s=='=' for s in l[1::3]])
    ):
        self.data['dataline'] += ' '+line
        dk = set([
            s.lower() for s in 
            self.data['dataline'].split()[0::3]
        ])
        if len(dk) != nk: return

    # ----- thermo_modify line one -----
    elif len(l) == nk:
        try:
            [float(v) for v in l]
            self.data['dataline'] += ' '.join([
                f'{k} = {v}' for k,v in zip(
                self.data['key'], l
                )
            ])
        except: return

    update_data(self.data)


def read(filename):

    class tmpobj: data = {}
    tmpobj.data['dataline'] = ''
    for s in ['_','n','Nrun','Nmin','Neq']:
        tmpobj.data[s] = 0
    for s in ['ix_min','ix_eq','key']:
        tmpobj.data[s] = []

    with open(filename,'r') as f:
        for line in f:
            parser(line,self=tmpobj)
    return tmpobj.data
