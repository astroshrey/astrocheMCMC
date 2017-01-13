from astrochem import tools
import matplotlib.pyplot as plt
time, abun = tools.readabun("astrochem_output.h5", 'CO')
print max(abun[:,0])
plt.plot(time, abun[:,0])
plt.xscale('log')
plt.yscale('log')
plt.show()
