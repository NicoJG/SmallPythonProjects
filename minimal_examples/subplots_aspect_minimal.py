import matplotlib.pyplot as plt
from matplotlib import figure

fig = plt.figure(figsize=(5,5))

ax1 = plt.subplot(221, anchor='SE', aspect=1, xlim=(0,1), ylim=(0,2))
ax2 = plt.subplot(222, anchor='SW', box_aspect=1, sharey=ax1, xlim=(0,3))
ax3 = plt.subplot(223, anchor='NE', box_aspect=1, sharex=ax1, ylim=(0,4))
ax4 = plt.subplot(224, anchor='NW', xlim=(0,5), ylim=(0,6))

#plt.subplots_adjust(left=0, right=1)
#fig.set_size_inches(*figure.figaspect(1))

plt.show()