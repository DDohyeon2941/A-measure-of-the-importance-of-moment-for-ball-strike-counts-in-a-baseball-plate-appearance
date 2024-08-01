# -*- coding: utf-8 -*-
"""
Created on Mon Dec 19 17:23:06 2022

@author: dohyeon
"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


temp_df = pd.read_csv(r'count_1028.csv', index_col=0)
temp_df



xx=[0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3]
yy=[0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 2]

plt.scatter(xx,yy)


#%%


import matplotlib.pyplot as plt
from matplotlib.transforms import Affine2D
import mpl_toolkits.axisartist.floating_axes as floating_axes

fig = plt.figure()

plot_extents = 0, 10, 0, 10
transform = Affine2D().rotate_deg(40)
helper = floating_axes.GridHelperCurveLinear(transform, plot_extents)
ax = floating_axes.FloatingSubplot(fig, 111, grid_helper=helper)

fig.add_subplot(ax)

plt.show()

#%%


from matplotlib.transforms import Affine2D
import mpl_toolkits.axisartist.floating_axes as floating_axes
import numpy as np
import mpl_toolkits.axisartist.angle_helper as angle_helper
from matplotlib.projections import PolarAxes
from mpl_toolkits.axisartist.grid_finder import (FixedLocator, MaxNLocator,
                                                 DictFormatter)
import matplotlib.pyplot as plt


def setup_axes1(fig, rect):
    """
    A simple one.
    """
    tr = Affine2D().scale(2, 1).rotate_deg(30)

    grid_helper = floating_axes.GridHelperCurveLinear(
        tr, extremes=(0, 3, 0, 2))

    ax1 = floating_axes.FloatingSubplot(fig, rect, grid_helper=grid_helper)
    fig.add_subplot(ax1)

    aux_ax = ax1.get_aux_axes(tr)

    grid_helper.grid_finder.grid_locator1._nbins = 3
    grid_helper.grid_finder.grid_locator2._nbins = 2

    return ax1, aux_ax

fig = plt.figure()

#x = range(10)
#y = x + np.random.randint(-1,1,10)


ax1, aux_ax1 = setup_axes1(fig, 111)
aux_ax1.scatter(xx,yy,c='green',label='green')
aux_ax1.set_yticks([0,1,2,3], [0,1,2,3])
#aux_ax1.scatter(y,x,c='purple',label='purple')
ax1.legend(loc='upper right')

plt.show()



#%%
"""
교수님께 보여드릴부분
"""




import matplotlib.pyplot as plt
from matplotlib.transforms import Affine2D
import mpl_toolkits.axisartist.floating_axes as floating_axes
import numpy as np
from mpl_toolkits.axisartist import angle_helper, Axes, HostAxes

fig = plt.figure()
skewed_transform = Affine2D().skew_deg(90 -55 , 0)
grid_helper = floating_axes.GridHelperCurveLinear(skewed_transform, extremes=(0, 3, 0, 2),  )

#grid_helper.new_fixed_axis()
grid_helper.grid_finder.grid_locator1._nbins = 3
grid_helper.grid_finder.grid_locator2._nbins = 2
#grid_helper.grid_finder.tick_formatter2(direction=0, factor=[0,1,2],values=[0,1,2])
skewed_ax = floating_axes.FloatingSubplot(fig, 111, grid_helper=grid_helper)
#skewed_ax.set_yticklabels(skewed_ax.get_xticks(), rotation = 90)
#skewed_ax.set_facecolor('0.95')  # light grey background
#skewed_ax.axis["top"].set_visible(False)
#skewed_ax.axis["left"].set_visible(False)
fig.add_subplot(skewed_ax)
#skewed_ax.axis['left'].get_helper().nth_coord_ticks=1
#skewed_ax.axis["left"].major_ticklabels.set_axis_direction("top")
skewed_ax.axis["left"].major_ticklabels.set_rotation(130)
#skewed_ax.axis["left"].set_axis_direction("left")
skewed_ax.grid(color='k')
skewed_ax.text(0.1,0,'20.34%')
skewed_ax.text(1.1,0,'31.19%')
skewed_ax.text(2.1,0,'44.59%')
skewed_ax.text(3.1,0,'73.46%')



skewed_ax.text(0.8,1,'26.68%')
skewed_ax.text(1.8,1,'33.31%')
skewed_ax.text(2.8,1,'45.66%')
skewed_ax.text(3.8,1,'73.69%')



skewed_ax.text(1.45,2,'57.52%')
skewed_ax.text(2.45,2,'66.09%')
skewed_ax.text(3.45,2,'78.39%')
skewed_ax.text(4.45,2,'100.00%')

skewed_ax.set_ylabel("Strike Count")
skewed_ax.set_xlabel("Ball Count")


#ax.text(8, 13, 'December', style='italic')


#x, y = np.random.rand(2, 100)  # random point in a square of [0,1]x[0,1]
#skewed_ax.scatter(xx, yy, transform=skewed_transform + skewed_ax.transData, lw=0.5)
#plt.yticks(rotation = 90)
#skewed_ax.set_yticklabels([0,1,2], rotation=45)
#skewed_ax.plot([0,1,2,3], [2,2,2,2],transform=skewed_transform + skewed_ax.transData)

plt.show()
#%%


fig = plt.figure()
skewed_transform = Affine2D().skew_deg(90 -55 , -30)
grid_helper = floating_axes.GridHelperCurveLinear(skewed_transform, extremes=(0, 3, 0, 2),  )

#grid_helper.new_fixed_axis()
grid_helper.grid_finder.grid_locator1._nbins = 3
grid_helper.grid_finder.grid_locator2._nbins = 2
#grid_helper.grid_finder.tick_formatter2(direction=0, factor=[0,1,2],values=[0,1,2])
skewed_ax = floating_axes.FloatingSubplot(fig, 111, grid_helper=grid_helper)
#skewed_ax.set_yticklabels(skewed_ax.get_xticks(), rotation = 90)
#skewed_ax.set_facecolor('0.95')  # light grey background
#skewed_ax.axis["top"].set_visible(False)
#skewed_ax.axis["left"].set_visible(False)
fig.add_subplot(skewed_ax)
#skewed_ax.axis['left'].get_helper().nth_coord_ticks=1
#skewed_ax.axis["left"].major_ticklabels.set_axis_direction("top")
skewed_ax.axis["left"].major_ticklabels.set_rotation(130)
skewed_ax.axis["bottom"].major_ticklabels.set_rotation(20)
#skewed_ax.axis["bottom"].major_ticklabels.set_label([" "," "," "," b"])

#skewed_ax.axis["left"].set_axis_direction("left")
skewed_ax.grid(color='k')
skewed_ax.text(0.1,0,'20.34%')
skewed_ax.text(1.1,-0.6,'31.19%')
skewed_ax.text(2.1,-1.2,'44.59%')
skewed_ax.text(3.1,-1.8,'73.46%')



skewed_ax.text(0.8,1,'26.68%')
skewed_ax.text(1.8,0.4,'33.31%')
skewed_ax.text(2.8,-0.2,'45.66%')
skewed_ax.text(3.8,-0.8,'73.69%')



skewed_ax.text(1.45,2,'57.52%')
skewed_ax.text(2.45,1.5,'66.09%')
skewed_ax.text(3.45,0.9,'78.39%')
skewed_ax.text(4.45,0.3,'100.00%')

skewed_ax.set_ylabel("Strike Count")
skewed_ax.set_xlabel("Ball Count")

skewed_ax.scatter(xx, yy, transform=skewed_transform + skewed_ax.transData, lw=0.05, c='k', marker='.')

#ax.text(8, 13, 'December', style='italic')


#x, y = np.random.rand(2, 100)  # random point in a square of [0,1]x[0,1]
#plt.yticks(rotation = 90)
#skewed_ax.set_yticklabels([0,1,2], rotation=45)
#skewed_ax.plot([0,1,2,3], [2,2,2,2],transform=skewed_transform + skewed_ax.transData)

plt.show()















