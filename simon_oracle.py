import random
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit import IBMQ, Aer, assemble, execute
from qiskit.visualization import plot_histogram

state_size = 3
la = QuantumRegister(state_size, name='la')
lb = QuantumRegister(state_size, name='lb')
ra = QuantumRegister(state_size, name='ra')
rb = QuantumRegister(state_size, name='rb')
x = QuantumRegister(state_size + 1, name='x')
out = QuantumRegister(state_size+1, name='out')
k0 = [random.randint(0, 1) for _ in range(state_size)]
k1 = [random.randint(0, 1) for _ in range(state_size)]
outc = ClassicalRegister(state_size+1, name='outcr')

alpha = [1, 1, 1]
beta = [0, 0, 0]

def simon(qc, l, r):
    for i in range(state_size):
        qc.ccx(r[(i-1)%state_size],r[(i-8)%state_size],l[i])
        qc.cx(r[(i-2)%state_size],l[i])
        if k0[i]:
            qc.x(l[i])
    
    for i in range(state_size):
        qc.ccx(l[(i-1)%state_size],l[(i-8)%state_size],r[i])
        qc.cx(l[(i-2)%state_size],r[i])
        if k1[i]:
            qc.x(r[i])

def f(qc, x):
    qc.cx(x[1:], la)
    qc.cx(x[1:], lb)
    simon(qc, la, ra)
    for i in range(state_size):
        if beta[i]:
            qc.x(ra[i])

    simon(qc, lb, rb)
    for i in range(state_size):
        if alpha[i]:
            qc.x(rb[i])
    
    qc.cx(x[0], out[0])
    for i in range(state_size):
        qc.ccx(x[0], ra[i], out[i+1])
        qc.x(x[0])
        qc.ccx(x[0], rb[i], out[i+1])
        qc.x(x[0])
    
    for i in range(state_size):
        if alpha[i]:
            qc.x(rb[i])

    for i in range(state_size):
        if beta[i]:
            qc.x(ra[i])
    
    for i in range(state_size):
        if k1[i]:
            qc.x(ra[i])
        qc.cx(la[(i-2)%state_size],ra[i])
        qc.ccx(la[(i-1)%state_size],la[(i-8)%state_size],ra[i])

    for i in range(state_size):
        if k0[i]:
            qc.x(la[i])
        qc.cx(ra[(i-2)%state_size],la[i])
        qc.ccx(ra[(i-1)%state_size],ra[(i-8)%state_size],la[i])

    for i in range(state_size):
        if k1[i]:
            qc.x(rb[i])
        qc.cx(lb[(i-2)%state_size],rb[i])
        qc.ccx(lb[(i-1)%state_size],lb[(i-8)%state_size],rb[i])

    for i in range(state_size):
        if k0[i]:
            qc.x(lb[i])
        qc.cx(rb[(i-2)%state_size],lb[i])
        qc.ccx(rb[(i-1)%state_size],rb[(i-8)%state_size],lb[i])
    
    qc.cx(x[1:], la)
    qc.cx(x[1:], lb)

    qc.measure(out, outc)
    qc.h(x)
    qc.measure(x, outc)

qc = QuantumCircuit(la, lb, ra, rb, x, out, outc)
for i in range(state_size):
    if alpha[i]:
        qc.x(ra[i])
    if beta[i]:
        qc.x(rb[i])
qc.h(x)
f(qc, x)
for i in range(state_size):
    if alpha[i]:
        qc.x(ra[i])
    if beta[i]:
        qc.x(rb[i])
qc.draw(output='mpl', fold=50, interactive= True)
# aer_sim = Aer.get_backend('aer_simulator')
# qobj = assemble(qc, shots=1024)
# results = aer_sim.run(qobj).result()
# counts = results.get_counts()
# plot_histogram(counts)
plt.show()