import re
import numpy as np
from time import perf_counter
import glob
import matplotlib.pyplot as plt
from numpy.lib.function_base import median

def get_website(line: str) -> str:
    start_idx = re.search("PING ", line)
    end_idx = re.search(" \(", line)
    website = line[start_idx.end():end_idx.start()]
    return website

def get_times(lines: list) -> list:
    times: list = []
    for line in lines: 
        if "time=" in line:
            time_loc = re.search("time=", line)
            ms_loc = re.search(" ms\n", line)
            t = float(line[time_loc.end():ms_loc.start()])
            times.append(t)

    return times

def main():
    pc_start = perf_counter()
    summary_file = open("summary.log", "w")

    file_glob = glob.glob("*.txt")
    for file in file_glob:
        with open(file, 'r') as f:
            lines = f.readlines()
        
        # Get the website name and the response times
        website = get_website(lines[0])
        times = get_times(lines)
        
        # Simple statistics
        mean_resp = np.mean(times)
        std_resp = np.std(times)

        # Plot
        plt.plot(times)
        plt.axhline(y=mean_resp, color='r', linestyle='-')
        plt.xlabel("Samples")
        plt.ylabel("Milliseconds (ms)")
        plt.savefig(file[:-4] + ".png")
        plt.clf()
        pc_end = perf_counter() - pc_start
        summary = f"{website:>16}: {mean_resp:6.2f} ±{std_resp:6.2f} ms from {len(times):6} samples"
        summary_file.write(summary + "\n")

        print(summary)


if __name__ == "__main__": main()