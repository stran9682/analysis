import pandas
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

media_type = [
    ("udp/audio", "quic/audio", "Audio"), 
    ("udp/video", "quic/video", "Video"), 
    ("udp-constrained/audio", "quic-constrained/audio", "Constrained Audio"), 
    ("udp-constrained/video", "quic-constrained/video", "Constrained Video")
]

for (udp, quic, type) in media_type:
    receive1 = pandas.read_csv(f"{udp}_receive_data.csv")
    send1 = pandas.read_csv(f"{udp}_send_data.csv")

    received_packets1 = pandas.merge(receive1, send1, on=["sequence number"], how="inner")

    print(f"sent {len(send1)}, recieved {len(received_packets1)}")

    received_packets1["difference"] = (received_packets1["unix timestamp_x"] - received_packets1["unix timestamp_y"]) / 10**6
    
    # Second dataset
    receive2 = pandas.read_csv(f"{quic}_receive_data.csv")
    send2 = pandas.read_csv(f"{quic}_send_data.csv")

    received_packets2 = pandas.merge(receive2, send2, on=["sequence number"], how="inner")

    print(f"sent {len(send2)}, recieved {len(received_packets2)}")

    received_packets2["difference"] = (received_packets2["unix timestamp_x"] - received_packets2["unix timestamp_y"]) / 10**6

    # combining the datasets
    min_rows = min(len(received_packets1), len(received_packets2))
    received_packets1 = received_packets1.iloc[:min_rows]
    received_packets2 = received_packets2.iloc[:min_rows]

    # display statistics 
    print(received_packets1["difference"].describe())
    print(received_packets2["difference"].describe())

    statistic, p_value = stats.ranksums(received_packets1["difference"], received_packets2["difference"])
    print(f"Statistic: {statistic}")
    print(f"P-value: {p_value}")

    plt.hist(received_packets1["difference"])
    plt.show()

    plt.hist(received_packets2["difference"])
    plt.show()

    # ax = received_packets2['difference'].plot.hist(bins=15, alpha=0.5, label='QUIC', legend=True, color=["purple"] )

    # # Plot the second dataset onto the same axis
    # received_packets1['difference'].plot.hist(bins=15, ax=ax,  label='UDP', legend=True, color='gold')
    # plt.xlabel("Round trip latency (ms)")
    # plt.title("Latency of QUIC vs UDP audio packets")

    # plt.show()

    plt.figure(figsize=(8, 8))

    plt.ecdf(received_packets1["difference"], label="UDP", linewidth=2, color="gold")

    plt.ecdf(received_packets2["difference"], label="QUIC", linewidth=2, color="purple")

    plt.ylim(0.97, 1.0001) 
    plt.ylabel(r'$\lambda_{packets}$', fontsize=15)
    plt.xlabel('Time (ms)',  fontsize=15)
    plt.legend(title='Protocols', loc='lower right')
    plt.title(f"{type} Latency Cumulative Distribution")

    plt.savefig(f'{type}.svg') 
    plt.show()