import matplotlib.pyplot as plt


def draw_plot(x_values, y_values, clr='b', label=''):
    plt.plot(x_values, y_values, linestyle='-', markersize=0.2, color=clr, label=label)


def use_plot_legend():
    plt.legend()


def save_plot(title, x_label, y_label, name):
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.grid()
    plt.savefig(name)
