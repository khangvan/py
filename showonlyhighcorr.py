def showonlyhighcorr(df,N=0.8):
  """
  do filter only these item that have correalation with abs upper or lower 0.8
  """
  import numpy as np
  df=df.copy()
  # Create correlation matrix
  corr_matrix = df.corr()

  # Select upper triangle of correlation matrix
  upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(np.bool))

  # Find index of feature columns with correlation greater than 0.8
  to_drop = [column for column in upper.columns if any(upper[column] > N) | any(upper[column] < -N)]
  print(to_drop)

  dfz=upper.stack().reset_index().dropna() # do stack
  dfz.columns=["level_1","level_2","corr_val"] #remane
  masknew=(dfz["corr_val"]>=N) | (dfz["corr_val"]<=-N) # filter
  f=dfz[masknew].sort_values(["level_1","corr_val"], ascending =[True,False])
  return f.reset_index(drop=True)

# showonlyhighcorr(X,0.8)
