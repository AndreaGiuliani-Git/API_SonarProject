#Module to plot chart of data.
from matplotlib import pyplot as plt

def scatter_plot_chart(x_data, y_data, x_label, y_label, title):
    """
    Plot a scatter chart with the data of dataframe.

        :param x_data: data object which use in x axe
        :param y_data: data object which use in y axe
        :param x_label: string contains the x_data information
        :param y_label: string contains the y_label information
        :param title: string contains the chart title
        :return: None
    """
    plt.style.use('seaborn-darkgrid')
    plt.title(title.upper(), fontsize = 30)
    plt.scatter(x_data, y_data, marker = 'o', color = 'red')
    plt.ylabel(y_label, fontsize = 15)
    plt.xlabel(x_label, fontsize = 15)
    plt.show()
    

