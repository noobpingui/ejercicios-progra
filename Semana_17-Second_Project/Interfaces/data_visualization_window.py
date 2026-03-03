import matplotlib.pyplot as plt

class Visualization():

    def show_bar_chart(self, x, y):

        fig, ax = plt.subplots()

        labels = ["Income", "Expenses"]
        bar_labels = ['red', 'blue']
        bar_colors = ['tab:red', 'tab:blue']
        values = [x, y]


        ax.bar(labels, values, label=bar_labels, color=bar_colors)
        ax.set_title('Transactions Summary')
        ax.legend(title='Legend')

        #---- To show values for each label----
        for idx, val in enumerate(values):
            plt.text(idx, val, f"{val}", ha='center', va='bottom')

        return plt.show()

