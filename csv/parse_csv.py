import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def generate_test_data(file_name, w, h):
    test_data = np.random.randn(w * h)
    with open(file_name, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(test_data)

def generate_diff_data(file_a, file_b, h, dx, dy):
    data_a = np.loadtxt(file_a, delimiter=',').reshape(h, -1)
    data_b = np.loadtxt(file_b, delimiter=',').reshape(h, -1)

    ax = dx // 2
    ay = dy // 2
    bx = dx - ax
    by = dy - ay

    cut_x = max(ax, bx)
    cut_y = max(ay, by)

    mat_a = np.roll(data_a, (ax, ay), axis=(0, 1))
    mat_b = np.roll(data_b, (-bx, -by), axis=(0, 1))

    if cut_x > 0:
        mat_a = mat_a[cut_x:-cut_x,:]
        mat_b = mat_b[cut_x:-cut_x,:]

    if cut_y > 0:
        mat_a = mat_a[:,cut_y:-cut_y]
        mat_b = mat_b[:,cut_y:-cut_y]

    diff = np.abs(mat_a - mat_b)
    return diff

def draw(data, cmin, cmax, file_name):
    plt.figure(figsize=(4,3))
    plt.gca().invert_yaxis()
    plt.imshow(data, interpolation='nearest', vmin=cmin, vmax=cmax, cmap='hot')
    plt.colorbar()
    plt.savefig(file_name)

w = 2000
h = 1000
#generate_test_data("sample2.csv", w, h)

#diff = generate_diff_data("sample1.csv", "sample2.csv", h, 0, 0)
diff = generate_diff_data("sample1.csv", "sample2.csv", h, 0, 0)

diff_w = diff.shape[0]
df = pd.Series(diff.reshape(-1))
idxmin = df.idxmin()
idxmax = df.idxmax()
print("min[%d,%d]=%f" % (idxmin % diff_w, idxmin // diff_w, df.min()))
print("max[%d,%d]=%f" % (idxmax % diff_w, idxmax // diff_w, df.max()))

amp = 5
draw(diff, 0, amp, 'result.png')