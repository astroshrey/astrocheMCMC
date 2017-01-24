from astrochem.wrapper import *
import numpy as np

def loglike(T, nH, time):
    """
    Given a temperature, density, and time, returns the log likelihood
    of those inputs giving observed abundances for a preset list of
    astrochemical species. TODO: figure out errors so we don't
    assume homoscedasticity.

    Args:
        T (float): the temperature of the dark cloud
        nH (float): the number density of hydrogen nuclei in the cloud
        time (float): the age of the cloud
    """

    specs = ['HCN', 'HCO(+)', 'C2H3N', 'CO']
    obser = np.log10(np.array([2e-8, 8e-9, (10**12.61)/1e22, 8e-5]))
    #error = np.log10(np.array([2e-8, 8e-9, (10**12.61)/1e22, 8e-5]))
    calcu = np.log10(np.array(get_abundances(T, nH, time, specs)))
    resid = obser - calcu
    #chisq = (resid/error)**2
    chisq = resid**2
    return -0.5*sum(chisq)

def get_abundances(T, nH, time, specs):
    """
    Given a set of input parameters and species, this function
    calls the astrochem model and returns abundances for those
    species.

    Args:
        T (float): the temperature of the dark cloud
        nH (float): the number density of hydrogen nuclei in the cloud
        time (float): the age of the cloud
        specs (list of str): a list of species to calculate abundances for
    """

    #setting physical conditions in the cell
    p = phys()
    p.chi = 1
    p.cosmic = 1.3e-17

    #setting initial abundances
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

    #setting more physical conditions in the cell
    density = nH
    av = 20
    tgas = T
    tdust = T
    c = cell(av, density, tgas, tdust)

    #setting up the solver
    verbose = 0
    abs_err = 1e-20
    rel_err = 1e-6
    s = solver(c, "osu2009.chm", p, abs_err, rel_err, initial_abundances, density, verbose)

    #solving for the abundances
    abundances = []
    try:
        abun = s.solve(time * 3600 * 24 * 365)
        for spec in specs:
            abundances.append(abun[spec])
    except ArithmeticError as e:
        raise "Something went wrong: %s" % e
    return abundances

print loglike(10, 1e4, 1e5)
