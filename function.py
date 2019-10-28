def newfile():
  print("newfile")
  
def hello():
  print("khang")


#-----
def kvan_get_lib(filename):
  import pandas as pd
  link="https://raw.githubusercontent.com/khangvan/py/master/{}".format(filename)
  !curl -O link
  import filename
  print("done")
