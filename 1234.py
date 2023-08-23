from datetime import datetime
import numpy as np
from numba import njit

l_st = [1, 2, 3, 4]
lst = np.array(l_st, dtype=int)
q = len(lst)
l = 13
var = np.zeros(shape=l, dtype=int)

@njit
def proc(var, i=0):
  for k in range(q):
    var[i] = lst[k]
    if i < l-1:
      proc(var, i+1)
    else:
      #print(var)

start_time = datetime.now()
proc(var)
print(f'\nSpent time: {datetime.now() - start_time}')