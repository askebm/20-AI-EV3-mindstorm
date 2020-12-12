import numpy as np
import pandas as pd
import json
import scipy.io as sio
import scipy.stats as ss
import matplotlib as mpl
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.formula.api import ols

##
COLOR = 'black'
mpl.rcParams['text.color'] = COLOR
mpl.rcParams['axes.labelcolor'] = COLOR
mpl.rcParams['xtick.color'] = COLOR
mpl.rcParams['ytick.color'] = COLOR

def to_file(name,text):
    f = open(name,mode='w')
    f.write(text)
    f.close()
##
bf = pd.read_csv('bf.csv')
astar = pd.read_csv('astar.csv')

bf['algorithm_name'] = 'Breadth First'
bf['algorithm'] = 1
astar['algorithm'] = 2
astar['algorithm_name'] = 'A*'

df = bf.append(astar)
##
anova_test = 'algorithm ~ succes'
lm = ols(anova_test,data=df).fit()
table = sm.stats.anova_lm(lm,typ=1)

##
bf.loc[bf['succes']==True].boxplot(by='boxes',column=['real'])
tmp = plt.ylim()
plt.savefig('plots/BFBoxPlotBoxesTime.pgf')
plt.show()
astar.loc[astar['succes']==True].boxplot(by='boxes',column=['real'])
plt.savefig('plots/AstarBoxPlotBoxesTime.pgf')
plt.show()
astar.loc[astar['succes']==True].boxplot(by='boxes',column=['real'])
plt.ylim(tmp)
plt.savefig('plots/AstarBoxPlotBoxesBFscale.pgf')
plt.show()

##
to_file('plots/ConfusionMatrix.tex', df[['algorithm_name','succes']].groupby(by='algorithm_name').sum().to_latex())

##
ss.probplot(bf.loc[bf['succes']==True]['boxes'].to_numpy(),plot=plt)
