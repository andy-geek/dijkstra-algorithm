from time import time
from dijkstra_algorithm import Graph
from advanced_drawing import draw_plot, use_plot_legend, save_plot


def stopwatch(graph, src, d):
    start = time()
    graph.dijkstra(src, d)
    end = time()

    return end - start


def generate_plot(x_values, y_values_2, y_values_3):
    draw_plot(x_values, y_values_2, clr='r', label='2-ary heap')
    draw_plot(x_values, y_values_3, clr='b', label='3-ary heap')
    use_plot_legend()


def experiment_1(name, lot):
    x_values, y_values_2, y_values_3 = [], [], []

    q, r = 1, 10 ** 6
    for n in range(100, 5001, 100):
        graph = Graph(n)
        m = lot(n)
        if m >= n * (n - 1):
            graph.generate_complete_graph(q, r)
        else:
            graph.generate_random_graph(m // 2, q, r)

        x_values.append(n)
        y_values_2.append(stopwatch(graph, 0, 2))
        y_values_3.append(stopwatch(graph, 0, 3))

        print(n)

    generate_plot(x_values, y_values_2, y_values_3)
    save_plot(title=f'Experiment {name}: n = 10^2...5*10^3 + 1 (step 10^2)',
              x_label='Number of n (vertices)', y_label='Time t (с)', name=f'experiment{name}.png')


def experiment_2(name):
    x_values, y_values_2, y_values_3 = [], [], []

    n = 5000
    q, r = 1, 10 ** 6
    for m in range(100_000, 5_000_001, 100_000):
        graph = Graph(n)
        if m >= n * (n - 1):
            graph.generate_complete_graph(q, r)
        else:
            graph.generate_random_graph(m // 2, q, r)

        x_values.append(m)
        y_values_2.append(stopwatch(graph, 0, 2))
        y_values_3.append(stopwatch(graph, 0, 3))

        print(m)

    generate_plot(x_values, y_values_2, y_values_3)
    save_plot(title=f'Experiment {name}: m = 10^5...5*10^6 + 1 (step 10^5)',
              x_label='Number of m (edges)', y_label='Time t (с)', name=f'experiment{name}.png')


def experiment_3(name, lot):
    x_values, y_values_2, y_values_3 = [], [], []

    n = 5000
    m = lot(n)
    q = 1
    for r in range(10, 201, 10):
        graph = Graph(n)
        if m >= n * (n - 1):
            graph.generate_complete_graph(q, r)
        else:
            graph.generate_random_graph(m // 2, q, r)

        x_values.append(r)
        y_values_2.append(stopwatch(graph, 0, 2))
        y_values_3.append(stopwatch(graph, 0, 3))

        print(r)

    generate_plot(x_values, y_values_2, y_values_3)
    save_plot(title=f'Experiment {name}: r = 10...2*10^2 + 1 (step 10)',
              x_label='Number of r (upper bound)', y_label='Time t (с)', name=f'experiment{name}.png')


def main():
    experiment_1('1_1', lambda n: n ** 2 // 10)
    #experiment_1('1_2', lambda n: n ** 2)

    #experiment_1('1_3', lambda n: n * 100)
    #experiment_1('1_4', lambda n: n * 1000)

    #experiment_2('2')

    #experiment_3('3_1', lambda n: n ** 2)
    #experiment_3('3_2', lambda n: n * 1000)


if __name__ == '__main__':
    main()
