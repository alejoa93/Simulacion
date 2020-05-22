import numpy as np
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 22})

var = np.loadtxt('inputs.txt', delimiter = ',')

a = var[0]
b = var[1]
tau = var[2]
k = var[3]


size = 100  # size of the 2D grid
dx = 2. / size  # space step
T = var[4]  # total time
dt = .001  # time step
n = int(T / dt)  # number of iterations

U = np.random.rand(size, size)
V = np.random.rand(size, size)

def laplacian(Z):
    Ztop = Z[0:-2, 1:-1]
    Zleft = Z[1:-1, 0:-2]
    Zbottom = Z[2:, 1:-1]
    Zright = Z[1:-1, 2:]
    Zcenter = Z[1:-1, 1:-1]
    return (Ztop + Zleft + Zbottom + Zright - 4 * Zcenter) / dx**2

def show_patterns(U, ax=None, cmap=plt.cm.brg):
    ax.imshow(U, cmap=cmap,
              interpolation='bilinear',
              extent=[-1, 1, -1, 1])
    ax.set_axis_off()
    

step_plot = n // int(T)
# We simulate the PDE with the finite difference
# method.
for i in range(n):
    # We compute the Laplacian of u and v.
    deltaU = laplacian(U)
    deltaV = laplacian(V)
    # We take the values of u and v inside the grid.
    Uc = U[1:-1, 1:-1]
    Vc = V[1:-1, 1:-1]
    # We update the variables.
    U[1:-1, 1:-1], V[1:-1, 1:-1] = \
        Uc + dt * (a * deltaU + Uc - Uc**3 - Vc + k),\
        Vc + dt * (b * deltaV + Uc - Vc) / tau
    # Neumann conditions: derivatives at the edges
    # are null.
    for Z in (U, V):
        Z[0, :] = Z[1, :]
        Z[-1, :] = Z[-2, :]
        Z[:, 0] = Z[:, 1]
        Z[:, -1] = Z[:, -2]

    # We plot the state of the system at
    # 9 different times.
    if i % step_plot == 0 and i < T * step_plot:
        fig = plt.figure(figsize=(8, 8))
        ax = plt.axes(figure=fig)
        show_patterns(U, ax=ax, cmap = plt.cm.brg)
        ax.set_title(f'$t={i * dt:.2f}$')
        plt.savefig('T_%03d.png'%int(i * dt))
        plt.close()

fig, ax = plt.subplots(1, 1, figsize=(8, 8))
show_patterns(U, ax=ax, cmap=plt.cm.copper)
ax.set_title(f'$t={i * dt:.2f}$')

plt.savefig('Turing_final.png')