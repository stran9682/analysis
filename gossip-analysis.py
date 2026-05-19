import pandas
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

send_time = pandas.read_csv("gossip/send_time.csv")
update_time = pandas.read_csv("gossip/update_time.csv")

time_to_update = pandas.merge(update_time, send_time, on=["doc-id"], how="inner")
time_to_update["difference"] = (time_to_update["time_x"] - time_to_update["time_y"]) / 10**6

print(time_to_update.describe())

time_to_update["difference"].plot.hist(color="purple", edgecolor="black")
plt.ylabel("Counts", fontsize=15)
plt.xlabel('Time (ms)',  fontsize=15)
plt.title("Gossip Update Time Latency Distribution")

plt.savefig('gossip_update_time.svg') 
plt.show()