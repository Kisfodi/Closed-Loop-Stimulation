import queue

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib
import stimulation
import csv

matplotlib.use("TkAgg")


class Visualizer:
    """
    A class used for visualization of real-time data
    """

    def __init__(self, f, fx, window_size=50, interval_size=1, counter=1):
        """
        :param f: The container (mainly a Queue) which contains real-time data
        :param window_size: The size of the data we want to visualize
        :param interval_size: The frequency of the plot animation
        """
        # self.fig = plt.figure()
        # remove the underlying axes

        self.fig, self.axs = plt.subplots(nrows=3, ncols=2)
        gs = self.axs[0, 0].get_gridspec()
        for ax in self.axs[0, 0:]:
            ax.remove()

        self.axbig = self.fig.add_subplot(gs[0, 0:])
        # self.ax = plt.subplot(3,2,(1,2))
        # self.ax2 = plt.subplot(323)
        # self.ax3 = plt.subplot(324)
        # self.ax4 = plt.subplot(325)
        # self.ax5 = plt.subplot(326)
        self.window_size = window_size
        self.interval_size = interval_size
        self.x = []
        self.xval = []
        self.stim_index = []
        self.non_stim_index = []
        self.y = []
        self.ysq = []
        self.m = []
        self.f = f
        self.fx = fx
        self.counter = counter
        self.stimulus = stimulation.Stimulation('keys.json')
        self.is_stim = False
        self.stim = []
        self.non_stim = []
        self.block_means = []

    def update(self, i):
        self.x.append(i)
        #TODO
        # Solve IndexError: list index out of range error
        # Cause: not enough keys
        # Solution terminating signal / Exception handlding

        # print(self.f.qsize())
        next_y = self.f.get()
        print("Timestamp empty status: {status}".format(status = self.fx.empty()))
        if (not self.fx.empty()):
            next_x = self.fx.get()
            self.xval.append(next_x)
        print("x value: {xx} - y value: {yy}".format(xx=self.xval[-1:],yy=self.y[-1:]))
        try:
            print(self.stimulus.log[i])
        except IndexError:
            print("No more keys...")
        print("Is stimulus {index}".format(index=self.is_stim))

        self.y.append(next_y)

        with open("C:\Egyetem\TTK\Closed loop stimulation_project\Test_xy.csv",'w',newline='') as ofile:
            result_writer = csv.writer(ofile, delimiter = ',')
            for ind in range(len(self.y)):
                result_writer.writerow([self.xval[ind],self.y[ind]])
        self.ysq.append(-1 * (next_y))
        self.m.append(np.mean(self.y))

        #TODO
        # make stimulus selection work for iteration/direction indices/timestamps
        try:
            if self.stimulus.log[i] and self.y[i:] != []:
                self.stim.append(self.y[i])
                self.stim_index.append(i)

            if not self.stimulus.log[i] and self.y[i:] != []:
                self.non_stim.append(self.y[i])
                self.non_stim_index.append(i)
        except IndexError:
            pass
        # gs = ff.add_gridspec(2, 2)
        # axs = ff.add_subplot()

        # istim
        if i % self.counter == 0:
            for row in self.axs[1:, 0:]:
                for ax in row:
                    if ax != self.axs[1, 1]:
                        ax.cla()
            self.axbig.cla()
            self.axbig.plot(self.x[-self.window_size:], self.y[-self.window_size:])

            #TODO
            # Types of data to put into output
            # What kind of data (DF/F means, simple activity)
            try:
                if not self.stimulus.log[i] and self.is_stim:
                    print("Starting non-stimulus block at index {index}...".format(index=i))
                    print("Plotting terminated stimulus block...")

                    self.axs[1, 1].cla()
                    self.axs[1, 1].plot(self.stim_index, self.stim, color='green')
                    self.axs[1, 1].scatter(self.stim_index[-1], self.stim[-1], color='green')
                    self.axs[1, 1].text(np.mean(np.array(self.stim_index)), np.mean(np.array(self.stim)), "Stimulus")

                    self.block_means.append([np.mean(np.array(self.stim)),"Stim"])
                    with open("C:\Egyetem\TTK\Closed loop stimulation_project\Test_block_means.csv", 'w', newline='') as ofile:
                        result_writer = csv.writer(ofile, delimiter=',')
                        for ind in range(len(self.block_means)):
                            result_writer.writerow([ind,self.block_means[ind][0],self.block_means[ind][1]])

                    self.stim.clear()
                    self.stim_index.clear()
                    self.is_stim = False

                if self.stimulus.log[i] and not self.is_stim:
                    print("Starting stimulus block at index {index}...".format(index=i))
                    print("Plotting terminated non-stimulus block...")

                    self.axs[1, 1].cla()
                    self.axs[1, 1].plot(self.non_stim_index, self.non_stim, color='red')
                    self.axs[1, 1].scatter(self.non_stim_index[-1], self.non_stim[-1], color='red')
                    self.axs[1, 1].text(np.mean(np.array(self.non_stim_index)), np.mean(np.array(self.non_stim)),
                                        "Not stimulus")

                    self.block_means.append([np.mean(np.array(self.non_stim)),"Non_Stim"])
                    with open("C:\Egyetem\TTK\Closed loop stimulation_project\Test_block_means.csv", 'w',
                          newline='') as ofile:
                        result_writer = csv.writer(ofile, delimiter=',')
                        for ind in range(len(self.block_means)):
                            result_writer.writerow([ind, self.block_means[ind][0],self.block_means[ind][1]])


                    self.non_stim.clear()
                    self.non_stim_index.clear()
                    self.is_stim = True
            except IndexError:
                self.axs[1, 1].cla()
            # if stim=0 és is_stim=true
            # self.ax.plot(self.x[stimulus elejétől], self.y[a stimulus elejétől]) piros
            # plot stimulus
            # stimulus kiürítése
            # is_stim = false
            self.axs[1, 0].plot(self.x[-self.window_size:], (self.xval[-self.window_size:]))
            # self.axs[1, 1].plot(self.x[-self.window_size:], self.ysq[-self.window_size:])
            self.axs[2, 0].plot(self.x[-self.window_size:], self.m[-self.window_size:])
            self.axs[2, 1].scatter(self.xval[-self.window_size:], self.y[-self.window_size:])
            self.axbig.scatter(i, self.y[-1])
            self.axbig.text(i - 1, self.y[-1] + 2, "{}".format(self.y[-1]))
            self.axs[1, 0].scatter(i, (self.xval[-1]))
            # self.axs[1, 1].scatter(i, self.ysq[-1])
            self.axs[2, 0].scatter(i, self.m[-1])
           # self.axs[2, 1].scatter(i, self.y[-1])

    def animate(self):
        ani = animation.FuncAnimation(fig=self.fig, func=self.update, interval=self.interval_size)
        # f = r"C:\Egyetem\TTK\Closed loop stimulation_project\animation_multiplot.gif"
        # writergif = animation.PillowWriter(fps=30)
        # ani.save(f, writer=writergif)
        plt.show()
