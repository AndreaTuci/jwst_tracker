import matplotlib.pyplot as plt
import database as d


colors = [
    'black',
    'purple',
    'green',
    'red',
    'orange',
    'blue'
]

if __name__ == '__main__':

    database = r"travel_data.db"
    conn = d.create_connection(database)
    data = d.select_all(conn)
    y = [row[1] for row in data]
    x = [num for num in range(len(y))]
    plt.xticks(x)

    plt.title('Miles away from Earth')
    plt.plot(x, y, color=colors[0])
    plt.show()

    y = [row[2] for row in data]
    plt.title('Distance from L2')
    plt.plot(x, y, color=colors[1])
    plt.show()

    y = [row[3] for row in data]
    plt.title('Percentage')
    plt.plot(x, y, color=colors[2])
    plt.show()

    y = [row[4] for row in data]
    plt.title('Speed (miles/second)')
    plt.plot(x, y, color=colors[3])
    plt.show()

    y = [row[5] for row in data]
    plt.title('Temperature - Warm side')
    plt.plot(x, y, color=colors[4])
    plt.show()

    y = [row[6] for row in data]
    plt.title('Temperature - Cold side')
    plt.plot(x, y, color=colors[5])
    plt.show()
