import numpy as np
import matplotlib.pyplot as plt

cm_name = 'cividis'
cm = plt.get_cmap(cm_name)

def print_rgb(value):
    rgba = cm(value)
    print("r=%f, g=%f, b=%f" % (rgba[0]*255, rgba[1]*255, rgba[2]*255))

print_rgb(0.0)
print_rgb(0.25)
print_rgb(0.5)
print_rgb(0.75)
print_rgb(1.0)