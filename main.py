# /usr/bin/python3

import sys

import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FuncFormatter
from matplotlib import animation
import matplotlib.patches as patches
import numpy as np

plt.style.use('dark_background')
plt.rc('font', serif='Helvetica Neue')
plt.rcParams.update({'font.size': 16})


def my_formatter(x, pos):
    """Format 1 as 1, 0 as 0, and all values whose absolute values is between
    0 and 1 without the leading "0." (e.g., 0.7 is formatted as .7 and -0.4 is
    formatted as -.4)."""
    val_str = '{:g}'.format(x)
    if np.abs(x) > 0 and np.abs(x) < 1:
        return val_str.replace("0", "", 1)
    else:
        return val_str


def base_plot(xmin, xmax):
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.set_xlim(xmin - 0.2*abs(xmin), xmax + 0.2*abs(xmin))

    # Move left y-axis and bottim x-axis to centre, passing through (0,0)
    ax.spines['left'].set_position('center')
    ax.spines['bottom'].set_position('center')

    # Eliminate upper, right and left axes
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.spines['left'].set_color('none')

    major_formatter = FuncFormatter(my_formatter)
    ax.xaxis.set_major_formatter(major_formatter)

    # ax.grid(visible=True, which='both', axis='both')
    for tic in ax.yaxis.get_major_ticks():
        tic.tick1line.set_visible(False)
        tic.label1.set_visible(False)

    modxmin = abs(xmin)
    ax.xaxis.set_major_locator(MultipleLocator(modxmin*1))
    ax.xaxis.set_minor_locator(MultipleLocator(modxmin*0.1))
    ax.tick_params(axis='x', which='both', length=20, color='w', width=2, direction='in', pad=-36)
    ax.set_ylim(-0.5625*modxmin, 0.5625*modxmin)
    ax.set_aspect('equal')
    # plt.tight_layout()

    return fig, ax

def movie(fig, ax, xmin, xmax):
    lw = 2
    line, = plt.plot([], [], lw=lw, c='r', alpha=0.6)
    v = np.array([
        [xmin-0.2*xmin, -0.2*abs(xmin)],
        [xmin, 0],
        [xmin+0.2*xmin, -0.2*abs(xmin)]
    ])
    patch = patches.Polygon(v, closed=True, fc='r', ec='r')
    ax.add_patch(patch)
    ann_list = []
    def init():
        line.set_data([], [])
        return line,

    def animate(i):
        for a in ann_list:
            a.remove()
        ann_list[:] = []
        steps = 200
        # line
        x = np.linspace(xmin, xmax, steps+1)
        y = [0, 0.1*abs(xmin)]
        line.set_data([x[i],x[i]], y)

        # triangle
        tmp = v.copy()
        tmp[:, 0] += i*0.01*abs(xmin)
        patch.set_xy(tmp)

        # text
        if tmp[1][0] < 0:
            ann = ax.annotate(f'    {int(x[i]):04} ms\n Video ahead', [tmp[2][0]+5, tmp[2][1]-27], color='w', fontsize=10)
        else:
            ann = ax.annotate(f'     {int(x[i]):03} ms\n Audio ahead', [tmp[2][0]+5, tmp[2][1]-27], color='w', fontsize=10)
        ann_list.append(ann)

        # write animation progress
        sys.stdout.write('\r')
        sys.stdout.write("{0:.0f}%".format(i * 100 / steps))

        return line,

    anim = animation.FuncAnimation(fig, animate, init_func=init, frames=120, blit=True)
    anim.save('editing/one_sync_cycle.mp4', fps=200, extra_args=['-vcodec', 'libx264'], bitrate=-1, dpi=240)


if __name__ == '__main__':
    xmin, xmax = -500, 500
    fig, ax = base_plot(xmin, xmax)
    movie(fig, ax, xmin, xmax)
    plt.show()
