from io import BytesIO
from matplotlib import pyplot as plt
import base64


def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format = 'png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph


def get_plot(x, y):

    plt.switch_backend('AGG')
    plt.figure(figsize=(10,5))
    plt.title('trades')
    plt.plot(x, y, marker='o', linestyle='-', color = 'blue', markerfacecolor='red')

    plt.xticks(rotation=45)
    plt.xlabel('Days')
    plt.ylabel('Total money')
    plt.tight_layout()

    graph = get_graph()
    return graph