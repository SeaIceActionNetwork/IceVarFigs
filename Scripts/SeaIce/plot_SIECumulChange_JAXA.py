"""
Reads in current year's Arctic sea ice extent from JAXA

Website   : https://ads.nipr.ac.jp/vishop/vishop-extent.html
Author    : Zachary M. Labe
Date      : 11 October 2016
"""

### Import modules
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as c
import urllib.request
import urllib as UL
import datetime
import cmocean

### Directory and time
directoryfigure = './Figures/'
directorydata = './Data/'
now = datetime.datetime.now()
currentmn = str(now.month)
currentdy = str(now.day)
currentyr = str(now.year)
currenttime = currentmn + '_' + currentdy + '_' + currentyr
currentdoy = now.timetuple().tm_yday

### Load url
url = 'https://ads.nipr.ac.jp/vishop.ver1/data/graph/plot_extent_n_v2.csv'

### Read file
raw_data = UL.request.urlopen(url)
dataset = np.genfromtxt(raw_data, skip_header=0,delimiter=",",)

### Set missing data to nan
dataset[np.where(dataset==-9999)] = np.nan

### Variables
month     = dataset[1:,0]        # 1-12, nan as month[0]
day       = dataset[1:,1]        # 1-31, nan as day[0]
mean1980  = dataset[1:,2]        # km^2, nan as mean1980[0]
mean1990  = dataset[1:,3]        # km^2, nan as mean1990[0]
mean2000  = dataset[1:,4]        # km^2, nan as mean2000[0]
years     = dataset[1:,5:]

doy       = np.arange(0,len(day),1)

### Change units to million km^2
years = years/1e6

### Recent day of current year
currentyear = years[:,-1]
lastday = now.timetuple().tm_yday -1
currentice = currentyear[lastday]
currentanom = currentice - (mean1980[lastday]/1e6)

currentyear[10] = currentyear[9]
currentyear[59] = currentyear[58]
                        
print('\nCompleted: Read sea ice data!')                        

### Set missing data to nan
dataset[np.where(dataset==-9999)] = np.nan

### October
monthq = np.where(month == 3)[0]

octice = years[monthq,:]
currentoct = currentyear[monthq]

### Calculate change
diffoct = octice - octice[0,:]
diffcurrent = currentoct - currentoct[0]

###########################################################################
###########################################################################
###########################################################################
### Define parameters
plt.rc('text',usetex=True)
plt.rc('font',**{'family':'sans-serif','sans-serif':['Avant Garde']}) 
plt.rc('savefig',facecolor='black')
plt.rc('axes',edgecolor='white')
plt.rc('xtick',color='white')
plt.rc('ytick',color='white')
plt.rc('axes',labelcolor='white')
plt.rc('axes',facecolor='black')

### Create plot
fig = plt.figure()
ax = plt.subplot(111)

#### Set x/y ticks and labels
ylabels = map(str,np.arange(-4,4.5,0.5))
plt.yticks(np.arange(-4,4.5,0.5),ylabels)
xlabels = map(str,np.arange(1,33,3))
plt.xticks(np.arange(0,33,3),xlabels)
plt.ylabel(r'\textbf{Extent Change $\bf{(\times}$10$\bf{^{6}}$ \textbf{km}$\bf{^2}$\textbf{)}',
            fontsize=15,color='w',alpha=0.6)
plt.xlabel(r'\textbf{March',fontsize=15,color='w',alpha=0.6)

#### Set x/y limits
plt.xlim([0,30])
plt.ylim([-0.5,0.5])

### Adjust axes in time series plots 
def adjust_spines(ax, spines):
    for loc, spine in ax.spines.items():
        if loc in spines:
            spine.set_position(('outward', 5))
        else:
            spine.set_color('none')  
    if 'left' in spines:
        ax.yaxis.set_ticks_position('left')
    else:
        ax.yaxis.set_ticks([])

    if 'bottom' in spines:
        ax.xaxis.set_ticks_position('bottom')
    else:
        ax.xaxis.set_ticks([]) 
  
### Adjust borders of figure      
ax.tick_params('both',length=5.5,width=2,which='major')             
adjust_spines(ax, ['left','bottom'])            
ax.spines['top'].set_color('none')
ax.spines['right'].set_color('none') 
ax.spines['left'].set_linewidth(2)
ax.spines['bottom'].set_linewidth(2) 

### Plot lines
plt.plot(diffoct[:,:],color='w',linewidth=0.35,alpha=0.8)
plt.plot(diffcurrent[:],color='darkorange',linewidth=2.5)
plt.scatter(int(day[lastday]-1),diffcurrent[int(day[lastday]-1)],s=13,
            color='darkorange',zorder=3)
            
zeroline = [0]*31
plt.plot(zeroline,linewidth=2,color='w',linestyle='--',
         zorder=1)

##### Add legend and labels
plt.text(day[lastday]-1,diffcurrent[int(day[lastday]-1)]+.1,r'\textbf{2018}',
         fontsize=14,color='darkorange')  


#### Define title
plt.title(r'\textbf{ARCTIC SEA ICE CHANGE [2002-2018]}',
                       fontsize=19,color='w',alpha=0.6)         

#### Add text box information
plt.text(0,-0.46,r'\textbf{DATA:} JAXA (Arctic Data archive System, NIPR)',
         fontsize=4.5,rotation='horizontal',ha='left',color='w',alpha=0.6)
plt.text(0,-0.48,r'\textbf{SOURCE:} https://ads.nipr.ac.jp/vishop/vishop-extent.html',
         fontsize=4.5,rotation='horizontal',ha='left',color='w',alpha=0.6)
plt.text(0,-0.5,r'\textbf{GRAPHIC:} Zachary Labe (@ZLabe)',
         fontsize=4.5,rotation='horizontal',ha='left',color='w',alpha=0.6) 
         
### Adjust figure sizing
fig.subplots_adjust(top=0.91)
fig.subplots_adjust(bottom=0.17)
   
### Save figure     
plt.savefig(directoryfigure + 'Mar18_siecumul_jaxa.png',dpi=300)       
                      