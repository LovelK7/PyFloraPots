import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})

class PyF_plots():
    def __init__(self):
        pass    
        # import tkinter as tk
        # self.root = tk.Tk()
        # self.root.title('Plots')
        # self.root.protocol("WM_DELETE_WINDOW", quit)
        
    def line_plt(self, df): #
        df.datetime = mdates.date2num(df.datetime)
        set_figsize = (3,2)
        x=df['datetime'].values
        colors = ['blue','green','red','yellow']
        linewidth = 2
        time_format = DateFormatter("%H:%M:%S")

        fig_vwc, ax = plt.subplots(figsize=set_figsize)
        ax.xaxis.set_major_formatter(time_format)
        ax.plot(x,df[['vwc']], color=colors[0], linewidth=linewidth, linestyle='-')
        ax.set_xlabel('Time')
        ax.set_ylabel('Vol. water cont. (%)')
        ax.set(ylim=(0,100))
        fig_vwc.autofmt_xdate()
        ax.fill_between(x, y1=20, y2=50, color='0.9')
        #plt.tight_layout()

        fig_ph, ax = plt.subplots(figsize=set_figsize)
        ax.xaxis.set_major_formatter(time_format)
        ax.plot(x,df[['ph']], color=colors[1], linewidth=linewidth, linestyle='-')
        ax.set_xlabel('Time')
        ax.set_ylabel('pH')
        ax.set(ylim=(3,14))
        fig_ph.autofmt_xdate()
        ax.fill_between(x, y1=5.5, y2=8, color='0.9')
        #plt.tight_layout()

        fig_sal, ax = plt.subplots(figsize=set_figsize)
        ax.xaxis.set_major_formatter(time_format)
        ax.plot(x,df[['sal']], color=colors[2], linewidth=linewidth, linestyle='-')
        ax.set_xlabel('Time')
        ax.set_ylabel('Salinity (ms/cm)')
        ax.set(ylim=(0,16))
        fig_sal.autofmt_xdate()
        ax.fill_between(x, y1=0, y2=4, color='0.9')
        #plt.tight_layout()

        fig_lux, ax = plt.subplots(figsize=set_figsize)
        ax.xaxis.set_major_formatter(time_format)
        ax.plot(x,df[['lux']], color=colors[3], linewidth=linewidth, linestyle='-')
        ax.set_xlabel('Time')
        ax.set_ylabel('Lux')
        ax.set(ylim=(0,1200))
        fig_lux.autofmt_xdate()
        ax.fill_between(x, y1=500, y2=1000, color='0.9')
        #plt.tight_layout()

        return fig_vwc, fig_ph, fig_sal, fig_lux

#         from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
#         fig_list = [fig_vwc,fig_ph,fig_sal,fig_lux]
#         for fig_one in fig_list:
#             canvas = FigureCanvasTkAgg(fig_one, master=self.root)
#             canvas.draw()
#             canvas.get_tk_widget().pack(padx=10, pady=10)

#     def run(self):
#         self.root.mainloop()

# if __name__ == '__main__':
#     from measurements import Meas
#     plot_app = PyF_plots()
#     meas_app = Meas()
#     df = meas_app.read_csv(1)
#     plot_app.line_plt(df)
#     plot_app.run()