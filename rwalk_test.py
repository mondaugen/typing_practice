import numpy as np
import rwalk

chars=np.array([ord(c) for c in 'abc'])
y=rwalk.weighted1(50,3,.9)
y=chars[y]
s="".join([chr(c) for c in y])
print(s)
