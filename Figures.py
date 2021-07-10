from matplotlib import pyplot as plt


def create_pie_chart(labels, values, title=None, fname=None):
    """
    Takes in a list of names and values and constructs a pie chart
    """
    # Create the plot
    explode = [0.01] * len(labels)
    fig = plt.figure(figsize =(10, 7))
    plt.pie(values, explode=explode, labels=labels)

    plt.title(label=title)
    
    if fname:
        plt.savefig(fname, transparent=True)
