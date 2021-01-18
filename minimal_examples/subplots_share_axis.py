import matplotlib.pyplot as plt

fig = plt.figure(figsize=(5,5))


n,m = 2,2

for i in range(n*m):
    ax = plt.subplot(int(f'{n}{m}{i+1}'), aspect='equal')
    if i%m!=0:
        ax.set_yticklabels([])
    
    ax.set_xticklabels([])

plt.subplots_adjust(wspace=0, hspace=0)

plt.show()