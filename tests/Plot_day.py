'''Program to show Licght Curves of gamma-tay novae by showing stacked

graphs each with the same realtive scales'''



import numpy as np

import matplotlib.pylab as plt

import matplotlib as mat

import warnings

warnings.filterwarnings('ignore')

import pandas as pd
import sys
import datetime

import seaborn as sns



sns.set_style("whitegrid",
              {'axes.edgecolor': '.2',
               'axes.facecolor': 'white',
               'axes.grid': True,
               'axes.linewidth': 0.5,
               'figure.facecolor': 'white',
               'grid.color': '.8',
               'grid.linestyle': u'-',
               'legend.frameon': True,
               'xtick.color': '.15',
               'xtick.direction': u'in',
               'xtick.major.size': 3.0,
               'xtick.minor.size': 1.0,
               'ytick.color': '.15',
               'ytick.direction': u'in',
               'ytick.major.size': 3.0,
               'ytick.minor.size': 1.0,
               })

sns.set_context("poster")




if __name__ == '__main__':
    from optparse import OptionParser


    p = OptionParser()
    p.set_usage('plot_day.py <DATE> [options]')
    p.set_description(__doc__)
    p.add_option("-p", dest="plot_parameter", default="x", help="Select what battery parameter should be plotted: v, a, c, t")
    opts, args = p.parse_args(sys.argv[1:])
    plot_parameter= opts.plot_parameter
    if args==[]:
        file = '/home/pollak/PycharmProjects/BMS/Log/' + str(datetime.date.today()) + '.csv'
    else:
     file = '/home/pollak/PycharmProjects/BMS/Log/' + str(args[0]) + '.csv'



BMS = pd.read_csv(file, sep=',')



time = np.linspace(0,len(BMS['Time'].values)/120.0,len(BMS['Time'].values))


voltage1 = BMS['Volt1'].values/1000.0
voltage2 = BMS['Volt2'].values/1000.0
voltage3 = BMS['Volt3'].values/1000.0
voltage4 = BMS['Volt4'].values/1000.0
charge1 = BMS['Charge1'].values
charge2 = BMS['Charge2'].values
charge3 = BMS['Charge3'].values
charge4 = BMS['Charge4'].values
current1 = BMS['Current1'].values/1000.0
current2 = BMS['Current2'].values/1000.0
current3 = BMS['Current3'].values/1000.0
current4 = BMS['Current4'].values/1000.0
temp1 = BMS['Temp1'].values/1000.0
temp2 = BMS['Temp2'].values/1000.0
temp3 = BMS['Temp3'].values/1000.0
temp4 = BMS['Temp4'].values/1000.0













if plot_parameter =='v':
    plt.figure()
    plt.plot(time, voltage1, linewidth=1.5, label="Battery Voltage A")
    plt.plot(time, voltage2, linewidth=1.5, label="Battery Voltage B")
    plt.plot(time, voltage3, linewidth=1.5, label="Battery Voltage C")
    plt.plot(time, voltage4, linewidth=1.5, label="Battery Voltage D")
    plt.xlim(0, 24)
    plt.ylim(45,55)
    plt.ylabel('Voltage (V)')
elif plot_parameter =='a':
    plt.figure()
    plt.plot(time, current1, linewidth=1.5, label="Battery Current A")
    plt.plot(time, current2, linewidth=1.5, label="Battery Current B")
    plt.plot(time, current3, linewidth=1.5, label="Battery Current C")
    plt.plot(time, current4, linewidth=1.5, label="Battery Current D")
    plt.xlim(0, 24)
    plt.ylim(0, 50)
    plt.ylabel('Current (A)')
elif plot_parameter =='c':
    plt.figure()
    plt.plot(time, charge1, linewidth=1.5, label="Battery Charge A")
    plt.plot(time, charge2, linewidth=1.5, label="Battery Charge B")
    plt.plot(time, charge3, linewidth=1.5, label="Battery Charge C")
    plt.plot(time, charge4, linewidth=1.5, label="Battery Charge D")
    plt.xlim(0, 24)
    plt.ylim(0, 100)
    plt.ylabel('Charge (%)')
elif plot_parameter == 't':
    plt.figure()
    plt.plot(time, temp1, linewidth=1.5, label="Battery Temperature A")
    plt.plot(time, temp2, linewidth=1.5, label="Battery Temperature B")
    plt.plot(time, temp3, linewidth=1.5, label="Battery Temperature C")
    plt.plot(time, temp4, linewidth=1.5, label="Battery Temperature D")
    plt.xlim(0, 24)
    plt.ylim(10, 30)
    plt.ylabel('Temperature (degC)')

elif plot_parameter == 'x':

    plt.subplot(221)
    plt.plot(time, temp1, linewidth=1.5, label="Battery A")
    plt.plot(time, temp2, linewidth=1.5, label="Battery B")
    plt.plot(time, temp3, linewidth=1.5, label="Battery C")
    plt.plot(time, temp4, linewidth=1.5, label="Battery D")
    plt.xlim(0, 24)
    plt.ylim(10, 30)
    plt.ylabel('Temperature (degC)')
    plt.xlabel('Time')
    plt.xticks([0, 3, 6, 9, 12, 15, 18, 21, 24])
    plt.rcParams.update({'font.size': 12})
    legend = plt.legend(loc='best', shadow=True)
    leg = plt.gca().get_legend()
    ltext = leg.get_texts()  # all the text.Text instance in the legend
    llines = leg.get_lines()  # all the lines.Line2D instance in the legend
    plt.setp(ltext, fontsize='small')
    plt.setp(llines, linewidth=1.5)  # the legend linewidth
    plt.tight_layout()

    plt.subplot(222)
    plt.plot(time, voltage1, linewidth=1.5, label="Battery A")
    plt.plot(time, voltage2, linewidth=1.5, label="Battery B")
    plt.plot(time, voltage3, linewidth=1.5, label="Battery C")
    plt.plot(time, voltage4, linewidth=1.5, label="Battery D")
    plt.xlim(0, 24)
    plt.ylim(45, 55)
    plt.ylabel('Voltage (V)')
    plt.xlabel('Time')
    plt.xticks([0, 3, 6, 9, 12, 15, 18, 21, 24])
    plt.rcParams.update({'font.size': 12})
    legend = plt.legend(loc='best', shadow=True)
    leg = plt.gca().get_legend()
    ltext = leg.get_texts()  # all the text.Text instance in the legend
    llines = leg.get_lines()  # all the lines.Line2D instance in the legend
    plt.setp(ltext, fontsize='small')
    plt.setp(llines, linewidth=1.5)  # the legend linewidth
    plt.tight_layout()

    plt.subplot(223)
    plt.plot(time, current1, linewidth=1.5, label="Battery A")
    plt.plot(time, current2, linewidth=1.5, label="Battery B")
    plt.plot(time, current3, linewidth=1.5, label="Battery C")
    plt.plot(time, current4, linewidth=1.5, label="Battery D")
    plt.xlim(0, 24)
    plt.ylim(0, 50)
    plt.ylabel('Current (A)')
    plt.xlabel('Time')
    plt.xticks([0, 3, 6, 9, 12, 15, 18, 21, 24])
    plt.rcParams.update({'font.size': 12})
    legend = plt.legend(loc='best', shadow=True)
    leg = plt.gca().get_legend()
    ltext = leg.get_texts()  # all the text.Text instance in the legend
    llines = leg.get_lines()  # all the lines.Line2D instance in the legend
    plt.setp(ltext, fontsize='small')
    plt.setp(llines, linewidth=1.5)  # the legend linewidth
    plt.tight_layout()

    plt.subplot(224)
    plt.plot(time, charge1, linewidth=1.5, label="Battery A")
    plt.plot(time, charge2, linewidth=1.5, label="Battery B")
    plt.plot(time, charge3, linewidth=1.5, label="Battery C")
    plt.plot(time, charge4, linewidth=1.5, label="Battery D")
    plt.xlim(0, 24)
    plt.ylim(0, 100)
    plt.ylabel('Charge (%)')
    plt.xlabel('Time')
    plt.xticks([0, 3, 6, 9, 12, 15, 18, 21, 24])
    plt.rcParams.update({'font.size': 12})
    legend = plt.legend(loc='best', shadow=True)
    leg = plt.gca().get_legend()
    ltext = leg.get_texts()  # all the text.Text instance in the legend
    llines = leg.get_lines()  # all the lines.Line2D instance in the legend
    plt.setp(ltext, fontsize='small')
    plt.setp(llines, linewidth=1.5)  # the legend linewidth
    plt.tight_layout()

else:
    print"Error: Plot parameter not valid. Allowed values: v,a,c,t"
    exit()









plt.xlabel('Time')

plt.grid(True)

plt.xticks([0,3,6,9,12,15,18,21,24])
plt.rcParams.update({'font.size': 12})

#plt.plot((4, 4), (0, -80), 'k:',linewidth=2.0)
#plt.plot((8.5, 8.5), (0, -80), 'k:',linewidth=2.0)
#plt.plot((3, 9), (-15, -15), 'k:',linewidth=2.0)

legend = plt.legend(loc='best', shadow=True)
leg = plt.gca().get_legend()
ltext  = leg.get_texts()  # all the text.Text instance in the legend
llines = leg.get_lines()  # all the lines.Line2D instance in the legend
plt.setp(ltext, fontsize='small')
plt.setp(llines, linewidth=1.5)      # the legend linewidth

plt.tight_layout()

#plt.savefig('OMT_IL_with_legend.eps', bbox_inches="tight")
#plt.savefig('returnloss.pdf')
plt.show()
