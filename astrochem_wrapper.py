from astrochem.wrapper import *
import numpy as np
import matplotlib.pyplot as plt

p = phys()
p.chi = 1
p.cosmic = 1.3e-17

initial_abundances = {
"H2"      : 5.00e-1,
"He"      : 1.40e-1,
"N"       : 2.14e-5,
"O"       : 1.76e-4,
"C(+)"    : 7.30e-5,
"S(+)"    : 2.00e-8,
"Si(+)"   : 3.00e-9,
"Fe(+)"   : 3.00e-9,
"Na(+)"   : 3.00e-9,
"Mg(+)"   : 3.00e-9,
"P(+)"    : 3.00e-9,
"Cl"      : 3.00e-9,
"F"       : 2.00e-8,
"e(-)"    : 7.303500e-05}

density = 1e4
av = 20
tgas = 10
tdust = 10
c = cell(av, density, tgas, tdust)
verbose = 0
abs_err = 1e-20
rel_err = 1e-6
s = solver(c, "osu2009.chm", p, abs_err, rel_err, initial_abundances, density, verbose)
times = np.logspace(2, 8, 128)
abundances = []
for time in times:
    try:
        abundances.append(s.solve(time * 3600 * 24 * 365)['CO'])
    except ArithmeticError as e:
        raise "Something went wrong: %s" % e

plt.plot(times, abundances)
plt.title('Wrapper-Generated Figure')
plt.ylabel('Abundance')
plt.xlabel('Time')
plt.xscale('log')
plt.yscale('log')
plt.savefig('wrapper_figure.png')
