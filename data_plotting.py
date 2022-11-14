import csv
import numpy as np
from matplotlib import pyplot as plt
import random
import time
import threading
import math

time_list = ['Time']
pilot = ['Pilot']
prox = ['Prox']
ground = ['Ground']
count = 0
flag = 0

def generate_data(list):
    list.append(random.randint(0, 1))


def cleanup_data_processing(time_list, prox_list, pilot_list, ground_list):
    time_list = np.transpose(np.array(time_list))
    prox_list = np.transpose(np.array(prox_list))
    pilot_list = np.transpose(np.array(pilot_list))
    ground_list = np.transpose(np.array(ground_list))

    csv_list = np.column_stack((time_list, prox_list, pilot_list, ground_list))
    np.savetxt("test.csv", csv_list, delimiter=',', fmt='%s')

def plotting(time_list, prox_list, pilot_list, ground_list):
    new_list = range(math.floor(min(time_list)), math.ceil(max(time_list)) + 1)
    plt.figure()
    plt.plot(time_list, prox_list, 'r')
    plt.plot(time_list, pilot_list, 'g')
    plt.plot(time_list, ground_list, 'b')
    plt.legend(['Prox', 'Pilot', 'Ground'])
    plt.title('Handle abuse LV signal plot')
    plt.xlabel('Time(s)')
    plt.ylabel('Continuity signal')
    plt.xticks(new_list)
    plt.yticks([0, 1])
    plt.show()
    plt.savefig("test.png")

def terminate():
    global flag

    while True:
        end = input()
        if end == "end":
            flag = 1
            break

if __name__ == '__main__':
    print('started')
    record = input()

    terminate_thread = threading.Thread(target=terminate)
    terminate_thread.start()

    if int(record) == 1:
        print("Recording...")
        while True:
            generate_data(pilot)
            generate_data(prox)
            generate_data(ground)

            count += 0.05  # seconds
            time_list.append(count)

            time.sleep(0.05)

            if flag == 1:
                terminate_thread.join()
                print("Done taking data.")
                break

    cleanup_data_processing(time_list, prox, pilot, ground)
    plotting(time_list[1:-1], prox[1:-1], pilot[1:-1], ground[1:-1])
