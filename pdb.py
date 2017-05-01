'''
Uses BioPython's PDB module to parse and extract information from
PDB.
The goal of writing this script is to analysis a model of the protein. 
There are a lot of different models for any given proteins in PDB.
It is almost impossible to analyze all of them in a single go. So this 
generic script would help with analyzing any model that the user is interested
in, at the time of analyzes.
'''

from __future__ import print_function
from Bio import PDB
from Bio.PDB import *
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

repository = PDB.PDBList()

#Parse the file using mmcif, pdb parser is no longer supported by PDB
parser = MMCIFParser()

#######################   METHODS ######################

#Number of Residues and atoms on Each Chain
def describe_model(name, pdb):
    print()
    this_list = []
    for model in pdb:
        for chain in model:
            this_list.append('%s - Chain: %s. Number of residues: %d. Number of atoms: %d.' % \
                   (name, chain.id, len(chain), len(list(chain.get_atoms()))))
    return this_list

#for generating 3d Plot
def plot(model):
    fig = plt.figure(figsize=(16, 9))
    fig.suptitle(model, fontsize=20)
    ax3d = fig.add_subplot(111, projection='3d')
    ax_xy = fig.add_subplot(331)
    ax_xy.set_title('X/Y')
    ax_xz = fig.add_subplot(334)
    ax_xz.set_title('X/Z')
    ax_zy = fig.add_subplot(337)
    ax_zy.set_title('Z/Y')
    color = {'A': 'r', 'B': 'g', 'C': 'b', 'D': '0.25', 'E': '0.5', 'F': '0.75', 'G': '1', 'H': '1', 'J': '1'}
    zx, zy, zz = [], [], []
    for chain in model.get_chains():
        xs, ys, zs = [], [], []
        for residue in chain.get_residues():
            ref_atom = next(residue.get_iterator())
            x, y, z = ref_atom.coord
            if ref_atom.element == 'HOH':
                zx.append(x)
                zy.append(y)
                zz.append(z)
                continue
            xs.append(x)
            ys.append(y)
            zs.append(z)
        ax3d.scatter(xs, ys, zs, color=color[chain.id])
        print(color[chain.id])
        ax_xy.scatter(xs, ys, marker='.', color=color[chain.id])

        ax_xz.scatter(xs, zs, marker='.', color=color[chain.id])
        ax_zy.scatter(zs, ys, marker='.', color=color[chain.id])
    ax3d.set_xlabel('X')
    ax3d.set_ylabel('Y')
    ax3d.set_zlabel('Z')
    ax3d.scatter(zx, zy, zz, color='k', marker='v', s=300)
    ax_xy.scatter(zx, zy, color='k', marker='v', s=80)
    ax_xz.scatter(zx, zz, color='k', marker='v', s=80)
    ax_zy.scatter(zz, zy, color='k', marker='v', s=80)
    for ax in [ax_xy, ax_xz, ax_zy]:
        ax.get_yaxis().set_visible(False)
        ax.get_xaxis().set_visible(False)

    fig.savefig('./matplotlib_analysis/myc_1nkp.jpg')
    # fig = plt.show()

####################### P53 1UTP MODEL ANALYSIS #######################

#Using PDB to retrieve model from the list
# repository.retrieve_pdb_file('1TUP', pdir='.')

p53_1tup = parser.get_structure('P 53 - DNA Binding', './protein_models/1tup.cif')

#TOP DOWN ANALYSIS

#chains in itup
p53_itup_model = describe_model('1TUP', p53_1tup)
# print(p53_itup_model)

# #all nonstandard residues except water
residues = []
for residue in p53_1tup.get_residues():
    if residue.id[0] in [' ', 'H_HOH']:
        continue
    residues.append(residue.id)
# print(residues)

#Pick a chain and look at its atoms
res = next(p53_1tup[0]['A'].get_residues())
# print(res)

# plot(p53_1tup)

####################### MYC 1NKP MODEL ANALYSIS #######################
# repository.retrieve_pdb_file('1NKP', pdir='.')
myc_1nkp = parser.get_structure('MYC - DNA Binding', './protein_models/1nkp.cif')

#chains in 1nkp
myc_1nkp_model = describe_model('1NKP', myc_1nkp)
print(myc_1nkp_model)

#all nonstandard residues except water
count = 0
for residue in myc_1nkp.get_residues():
    if residue.id[0] in [' ', 'H_HOH']:
        count +=1
print("Most of the residues are HOH: {}".format(count))

#Pick a chain and look at its atoms
res1 = next(myc_1nkp[0]['F'].get_residues())
print(res1)

plot(myc_1nkp)


####################### ERRB2 1N8Z MODEL ANALYSIS #######################
# repository.retrieve_pdb_file('1N8Z', pdir='.')
errb_1n8z = parser.get_structure('ERRB2-Complexed with Herceptin', './protein_models/1n8z.cif')

#chains in 1nkp
errb_1n8z_model = describe_model('1NKP', errb_1n8z)
print(errb_1n8z_model)

#all nonstandard residues except water
residues1 = []
for residue in errb_1n8z.get_residues():
    if residue.id[0] in [' ', 'H_HOH']:
        continue
    residues1.append(residue.id)
print(residues1)

#Pick a chain and look at its atoms
res1 = next(myc_1nkp[0]['A'].get_residues())
print(res1)

# plot(errb_1n8z)

# should be done using a better way, extracting data from uniprot API and hardcoding it defeats the purpose
# pass this to proteomics datatbase table models
# data = [(1, 'P53 1UTP Model', p53_itup_model, residues, res),
#         (2, 'MYC 1NKP Model', myc_1nkp_model, "Majority of residues are HOH, Total 962", res1
#
#         ]
