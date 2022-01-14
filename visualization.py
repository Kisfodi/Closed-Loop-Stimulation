import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib
import stimulation

matplotlib.use("TkAgg")


class Visualizer:
    """
    A class used for visualization of real-time data
    """

    def __init__(self, f, window_size=50, interval_size=1, counter=1):
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
        self.stim_index = []
        self.non_stim_index = []
        self.y = []
        self.ysq = []
        self.m = []
        self.f = f
        self.counter = counter
        self.stimulus = stimulation.Stimulation('keys.json')
        self.is_stim = False
        self.stim = []
        self.non_stim = []

    def update(self, i):
        # TODO
        # Solve IndexError: list index out of range error
        # Cause: not enough keys
        # Solution terminating signal / Exception handlding

        # print(self.f.qsize())
        self.x.append(i)
        print(self.y[i:])
        print(i)
        try:
            print(self.stimulus.json_keys[i])
        except IndexError:
            print("No more keys...")
        print("Is stimulus {index}".format(index=self.is_stim))
        self.y.append(self.f.get())
        self.ysq.append(-1 * (self.f.get()))
        self.m.append(np.mean(self.y))
        try:
            if self.stimulus.json_keys[i] and self.y[i:] != []:
                self.stim.append(self.y[i])
                self.stim_index.append(i)

            # self.is_stim = True
            # ha 1es kulcsot olvas be és is_stim=false
            # stimulus konténer (új lista)
            # stimulus.append
            # is_stim = true

            if not self.stimulus.json_keys[i] and self.y[i:] != []:
                self.non_stim.append(self.y[i])
                self.non_stim_index.append(i)
        # ha 1es kulcsot olvas be és is_stim=true
        # stimulus konténer (új lista)
        # stimulus.append
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
            # self.ax.cla()
            # self.ax2.cla()
            # self.ax3.cla()
            # self.ax4.cla()
            # self.ax5.cla()
            self.axbig.plot(self.x[-self.window_size:], self.y[-self.window_size:])
            # akkor plotoljon, ha az egyesek után 0 lesz
            # if flag:
            try:
                if not self.stimulus.json_keys[i] and self.is_stim:
                    print("Starting non-stimulus block at index {index}...".format(index=i))
                    print("Plotting terminated stimulus block...")

                    self.axs[1, 1].cla()
                    self.axs[1, 1].plot(self.stim_index, self.stim, color='green')
                    self.axs[1, 1].scatter(self.stim_index[-1], self.stim[-1], color='green')
                    self.axs[1, 1].text(np.mean(np.array(self.stim_index)), np.mean(np.array(self.stim)), "Stimulus")
                    self.stim.clear()
                    self.stim_index.clear()
                    self.is_stim = False

                if self.stimulus.json_keys[i] and not self.is_stim:
                    print("Starting stimulus block at index {index}...".format(index=i))
                    print("Plotting terminated non-stimulus block...")

                    self.axs[1, 1].cla()
                    self.axs[1, 1].plot(self.non_stim_index, self.non_stim, color='red')
                    self.axs[1, 1].scatter(self.non_stim_index[-1], self.non_stim[-1], color='red')
                    self.axs[1, 1].text(np.mean(np.array(self.non_stim_index)), np.mean(np.array(self.non_stim)),
                                        "Not stimulus")
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

            self.axs[1, 0].plot(self.x[-self.window_size:], 2 * np.abs(self.y[-self.window_size:]))
            # self.axs[1, 1].plot(self.x[-self.window_size:], self.ysq[-self.window_size:])
            self.axs[2, 0].plot(self.x[-self.window_size:], self.m[-self.window_size:])
            self.axs[2, 1].plot(self.x[-self.window_size:], self.ysq[-self.window_size:])
            self.axbig.scatter(i, self.y[-1])
            self.axbig.text(i - 1, self.y[-1] + 2, "{}".format(self.y[-1]))
            self.axs[1, 0].scatter(i, 2 * np.abs(self.y[-1]))
            # self.axs[1, 1].scatter(i, self.ysq[-1])
            self.axs[2, 0].scatter(i, self.m[-1])
            self.axs[2, 1].scatter(i, self.ysq[-1])

    def animate(self):
        ani = animation.FuncAnimation(fig=self.fig, func=self.update, interval=self.interval_size)
        # f = r"C:\Egyetem\TTK\Closed loop stimulation_project\animation_multiplot.gif"
        # writergif = animation.PillowWriter(fps=30)
        # ani.save(f, writer=writergif)
        plt.show()
