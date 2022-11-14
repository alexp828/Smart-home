from matplotlib import pyplot as plt
import csv
import numpy as np
import math


time_list = []
prox = []
pilot = []
ground = []
count = 0


with open("test.csv", 'r') as file:
    csv_read = csv.reader(file)

    for row in csv_read:
        if count == 0:
            count += 1
            pass
        else:
            time_list.append(float(row[0]))
            prox.append(float(row[1]))
            pilot.append(float(row[2]))
            ground.append(float(row[3]))


# last_second = str(time_list[-1])[0])
new_list = range(math.floor(min(time_list)), math.ceil(max(time_list))+1)
plt.figure()
plt.plot(time_list, prox, 'r')
plt.plot(time_list, pilot, 'g')
plt.plot(time_list, ground, 'b')
plt.legend(['Prox', 'Pilot', 'Ground'])
plt.title('Handle abuse LV signal plot')
plt.xlabel('Time(s)')
plt.ylabel('Continuity signal')
plt.xticks(new_list)
plt.yticks([0,1])
plt.show()
