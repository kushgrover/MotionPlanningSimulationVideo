import sys
import pandas as pd
import numpy as np
import matplotlib
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import csv
import math
import datetime


def plot_file(filename, col, dashed, thickness):
    csv_reader = pd.read_csv(filename, delimiter=',')
    x1 = csv_reader['x1']
    x2 = csv_reader['x2']
    y1 = csv_reader['y1']
    y2 = csv_reader['y2']

    if(dashed):
        plt.plot((x1, x2), (y1, y2), color = col, linestyle = 'dashed')
    elif(thickness == 1):
        plt.plot((x1, x2), (y1, y2), color = col, linewidth = 3)
    elif(thickness == 2):
        plt.plot((x1, x2), (y1, y2), color = col, linewidth = 5)
    else: 
        plt.plot((x1, x2), (y1, y2), color = col)



def animate(x1,y1,x2,y2,col,circle,small_circle,delay):
    x_data = []
    y_data = []
    slope = (y2-y1)/(x2-x1)
    ax = plt.gca()
    line, = ax.plot(x1, y1, marker = 'o', markersize = 5, color = col)
    distance = math.sqrt((x2-x1)*(x2-x1) + (y2-y1)*(y2-y1))

    def init():
        circle.center = (5, 5)
        small_circle.center = (5, 5)
        ax.add_patch(circle)
        ax.add_patch(small_circle)
        return circle, small_circle

    def animation_frame(i):
        if(i<=distance):
            x = x1 + (x2-x1) * i/distance
            y = y1 + slope * (x - x1)
            x_data.append(x)
            y_data.append(y)
            line.set_xdata(x_data)
            line.set_ydata(y_data)
            circle.center = (x, y)
            small_circle.center = (x, y)
            return line, circle, small_circle
        else:
            return

    animation = FuncAnimation(plt.gcf(), func=animation_frame, frames=np.arange(0,distance+delay,0.01), interval=1)
    return animation


# def mod(x, y):
#     if(x<y):
#         return y-x
#     else:
#         return x-y

# def find_index(list, x):
#     for i in range(list.size):
#         if(mod(list[i], x)< 1e-6):
#             return i
#     return -1


def plot_movement(filename, col, thickness, dir, i):
    csv_reader = pd.read_csv(filename, delimiter=',')
    X1 = csv_reader['x1']
    X2 = csv_reader['x2']
    Y1 = csv_reader['y1']
    Y2 = csv_reader['y2']

    # i = find_index(X1, start_x)
    # j = find_index(Y1, start_y)
    # assert(i == j and i >= 0)

    if(i>0):
        x1 = X1[:i]
        x2 = X2[:i]
        y1 = Y1[:i]
        y2 = Y2[:i]

        if(thickness == 1):
            plt.plot((x1, x2), (y1, y2), color = col, linewidth = 3)
        elif(thickness == 2):
            plt.plot((x1, x2), (y1, y2), color = col, linewidth = 5)
        else: 
            plt.plot((x1, x2), (y1, y2), color = col)

    circle = plt.Circle((X1[i], Y1[i]), 1.0, color = "orange", fill = False, linewidth = 5, zorder = 100000000)
    small_circle = plt.Circle((X1[i], Y1[i]), 0.02, color = "orange", linewidth = 5, zorder = 100000000)
    plt.gca().add_patch(circle)
    plt.gca().add_patch(small_circle)

    Writer = matplotlib.animation.writers['ffmpeg']
    writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)
    
    for k in range(i, X1.size):
        x1 = X1[k]
        x2 = X2[k]
        y1 = Y1[k]
        y2 = Y2[k]
        if(k == X1.size-1):
            animation = animate(x1,y1,x2,y2,col,circle,small_circle,0.2)
        else:
            animation = animate(x1,y1,x2,y2,col,circle,small_circle,0)

        print("Saving to " + dir + "videos/new/" + str(k) + ".mp4...")
        start_time = datetime.datetime.now()
        animation.save(dir + "videos/new/" + str(k) + ".mp4", writer = writer)
        end_time = datetime.datetime.now()
        time_diff = (end_time - start_time)
        execution_time = time_diff.total_seconds() * 1000
        print("done")
        print("Time taken: ", execution_time)

    # plt.show()    
    return X1.size




# def plot_last_point(filename, col):
#     csv_reader = pd.read_csv(filename, delimiter = ',')
#     x2 = csv_reader['x2']
#     y2 = csv_reader['y2']
#     plt.plot(x2[x2.size-1], y2[y2.size-1], marker = 'o', markersize = 15, color = col)
#     circle = plt.Circle((x2[x2.size-1], y2[y2.size-1]), 1.0, color = "orange", fill = False, linewidth = 5, zorder = 100000000)
#     plt.gca().add_artist(circle)

# def plot_first_point(filename, col):
#     csv_reader = pd.read_csv(filename, delimiter = ',')
#     x1 = csv_reader['x1']
#     y1 = csv_reader['y1']
#     plt.plot(x1[0], y1[0], marker = 'o', markersize = 15, color = col)

def set_axes():
    # plt.figure(figsize=(13.2,6.6))
    plt.figure(figsize=(19.8,10))
    plt.gca().set_aspect('equal', 'datalim')
    plt.xlim(0,6)
    plt.ylim(0,3)
    plt.xticks([0, 1, 2, 3, 4, 5, 6])
    plt.yticks([0, 1, 2, 3])
    plt.tick_params(axis = 'both', labelsize = '20')


dir_output = sys.argv[1]
dir_together = sys.argv[1] + "/video/together/"

# x,y = (0.1, 1.5)
# x,y = (5.045041561126709, 0.9325271844863892)
# x,y = (0.943608283996582, 0.5849441885948181)
k = 0
for i in range(1,4):
    print("Starting iteration " + str(i))
    set_axes()
    plot_file(dir_together + str(i) + ".csv", "#20168a", False, 0)
    plot_file(dir_output + "/obstacles.csv", "black", False, 1)
    plot_file(dir_output + "/labels.csv", "black", True, 0)
    k = plot_movement(dir_together + str(i) + "-movement.csv", "#33e026", 2, dir_together, k)


