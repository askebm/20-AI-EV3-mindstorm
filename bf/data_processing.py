import numpy as np
import pandas as pd
import json
import scipy.io as sio
import scipy.stats as ss
import matplotlib as mpl
import matplotlib.pyplot as plt
import statsmodels.api as sm
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

def number_of_boxes(level):
    f = open( '../levels/' + str(int(level)) + '.json')
    m = json.load(f)
    result = 0
    for l in m:
        for c in l:
            if c == 'J':
                result +=1
    f.close()
    return result
##
df = pd.read_csv('results.csv')
df['boxes'] = 0
for i in range(df.shape[0]):
    level = df.iloc[i]['level']
    df.loc[i,'boxes'] = number_of_boxes(level)

##
df.loc[:,['boxes','succes']].boxplot(by='succes')
plt.savefig('plots/BoxPlotBySucces.pgf')
plt.show()

df.loc[df['succes']==False,['boxes']].hist()
plt.savefig('plots/HistogramSuccesFalse.pgf')
plt.show()

df.loc[df['succes']==True,['boxes']].hist()
plt.savefig('plots/HistogramSuccesTrue.pgf')
plt.show()

##
ss.probplot(df.loc[df['succes']==True,['boxes']].to_numpy().flatten(),plot=plt)
plt.savefig('plots/ProbPlotSuccesTrue.pgf')
plt.show()
ss.probplot(df.loc[df['succes']==False,['boxes']].to_numpy().flatten(),plot=plt)
plt.savefig('plots/ProbPlotSuccesFalse.pgf')
plt.show()

##
percent_succes = df.loc[df['succes'] == True,['succes']].shape[0]/df.shape[0]

##
to_file('plots/DescribeSuccesTrue.tex',\
        df.loc[df['succes']==True,['real','user','sys']].describe().to_latex())
to_file('plots/DescribeSuccesFalse.tex',\
        df.loc[df['succes']==False,['real','user','sys']].describe().to_latex())



##
df['boxes'].hist()
plt.savefig('plots/HistogramAllBoxes.pgf')
plt.show()

