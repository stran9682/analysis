import pandas
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

times = pandas.read_csv("gossip/prop_time.csv")

min = times.groupby('update number')['time'].min()
max = times.groupby('update number')['time'].max()

print(min)
print(max)

df = pandas.merge(min, max, on="update number", how="inner")

df["difference"] = (df["time_y"] - df["time_x"]) / 10**6

print(df["difference"].describe())

df["difference"].plot.hist(color="purple", edgecolor="black", range=(0, 80))
plt.ylabel("Counts", fontsize=15)
plt.xlabel('Time (ms)',  fontsize=15)
plt.title("Gossip Propogation Time Latency Distribution")

plt.savefig('gossip_prop_time.svg') 
plt.show()