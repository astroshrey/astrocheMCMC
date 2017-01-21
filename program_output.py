from astrochem import tools
import matplotlib.pyplot as plt

time, abun = tools.readabun("astrochem_output.h5", 'CO')

plt.plot(time, abun[:,0])
plt.title('Normal Astrochem Figure')
plt.xlabel('Time')
plt.ylabel('Abundance')
plt.xscale('log')
plt.yscale('log')
plt.savefig('normal_astrochem.png')
