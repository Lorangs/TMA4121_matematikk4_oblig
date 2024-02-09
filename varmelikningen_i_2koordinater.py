# Obligatisk innlevering for matematikk 4 våren 2024
# skrevet av Lorang Strand
# Numerisk løsning av varmelikningen i to romlige dimensjoner.
# Dokumenatasjon er vedlagt i sepperat notat.

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib.animation as animation

# antall tidssted (oppløsning for t-aksen)
i = 100
# antall posisjonssteg i x-retning (oppløsning for x-aksen)
n = 20
# antall posisjonssteg i y-retning (oppløsning for y-aksen)
m = 20

# start og slutt for tid
t_start = 0
t_slutt = 1
k = (t_slutt - t_start) / i

# start og slutt for x-akse
x_start = 0
x_slutt = 10
g = (x_slutt - x_start) / n

# start og slutt for y-akse
y_start = 0
y_slutt = 10
h = (y_slutt - y_start) / m

x_gamma = k/h**2
y_gamma = k/g**2
print(x_gamma, '\n',y_gamma)


# Randkrav: Alle tempraturer langs ytterkanten er alltid lik 0.
# matrise som utgjør alle punktene i planet for u gjennom alle tidssteg m. 
u = np.zeros((i, m, n))

# Initialkrav: 5 spredt punkter med alle 100 grader
u[0, m//2, n//2] = 100
u[0, m//4, n//2] = 100
u[0, 3*m//4, n//2] = 100
u[0, m//2, n//4] = 100
u[0, m//2, 3*n//4] = 100

# Eksplisitt metode
# Gjennomgang av alle tids-"plan"
for a in range(0, i-1):
    # For alle y-akser
    for b in range (1, m-1):
        # For alle punkter i x-retning innenfor gitt y-akse. 
        for c in range (1, n-1):
            u[a+1, b, c] = x_gamma * (u[a, b, c+1] - 2*u[a, b, c] + u[a, b, c-1]) + y_gamma * (u[a, b-1, c] - 2*u[a, b, c] + u[a, b+1, c]) + u[a, b, c]



# plotting av grafene
x = np.arange (x_start, x_slutt, g)
y = np.arange (y_start, y_slutt, h)
X, Y = np.meshgrid(x, y)

fig = plt.figure()
ax = fig.add_subplot(projection="3d")

# lager en itererbar liste hvor alle separate tidsplot blir lagret.
figures = []
for a in range(len(u)):
    surf = ax.plot_surface (X, Y, u[a], cmap=cm.coolwarm)
    figures.append([surf])
    
# Fargeskalering av temperatur
fig.colorbar(surf, shrink=0.5, aspect=5)

# Animasjon som iterer gjennom listen og plotter alle elementene i tur etter et gitt tidsinterval
anim = animation.ArtistAnimation(
    fig, figures, interval=100, repeat=True
)

# For å lagre animasjonen som en GIF brukes Matplotlib Pillow
writer = animation.PillowWriter(fps=10,
                                metadata=dict(artist='Lorang Strand'),
                                bitrate=1800)
anim.save('animasjon.gif', writer=writer)

plt.show()


