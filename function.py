def hello():
  print("khang")

#-----
def exampleplot():
  import pandas as pd
  mytext='''
  2019/01/1,2
  2019/01/2,4
  2019/01/3,6
  2019/01/4,7
  2019/01/5,3
  2019/01/5,3
  '''
  mycols=['date','qty']

  import sys
  from io import StringIO


  df=pd.read_csv(StringIO(mytext),sep=",")
  df.columns=mycols
  y=df.set_index(['date'])

  import matplotlib.pyplot as plt
  import matplotlib
  # warnings.filterwarnings("ignore")
  plt.style.use('fivethirtyeight')
  matplotlib.rcParams['axes.labelsize'] = 14
  matplotlib.rcParams['xtick.labelsize'] = 12
  matplotlib.rcParams['ytick.labelsize'] = 12
  matplotlib.rcParams['text.color'] = 'G'

  y.plot(figsize=(15, 4))
  plt.show()
  print('ok')
