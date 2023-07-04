#!/usr/bin/env python3

import argparse
import matplotlib.pyplot as plt
import pandas as pd
import os
import time


def _read_data(disFilePath, sumFilePath):
    """
    Read force displacement data from files and return it as pandas dataframe
    """
    dis_data = pd.read_csv(disFilePath, delim_whitespace=True, names=["time", "disp"])
    sum_data = pd.read_csv(sumFilePath, delim_whitespace=True, names=["time", "force"])
    data = pd.concat([dis_data, sum_data], axis=1)
    data = data.loc[:, ~data.columns.duplicated()].copy()
    data["force"] = -1.0 * data["force"]

    return data


def main() -> None:

    # Set up command line argument parsing
    parser = argparse.ArgumentParser(
        description="Plotting FEAP F-U-diagrams in realtime."
    )
    parser.add_argument("inputfile", help="Name of input file for FEAP computation.")
    parser.add_argument(
        "--x",
        choices=["disp", "force", "time"],
        help="data set to be plotted on X axis. (default: disp)",
        default="disp",
    )
    parser.add_argument(
        "--y",
        choices=["disp", "force", "time"],
        help="data set to be plotted on Y axis. (default: force)",
        default="force",
    )
    parser.add_argument(
        "--refresh",
        help="refresh every N milliseconds.",
        default=100,
    )
    # parser.add_argument(
    #     "--reference",
    #     help="Path to a reference computation to plot together with results.",
    # )
    args = parser.parse_args()

    disFilePath = os.path.join(os.getcwd(), f"P{args.inputfile[1:]}a.dis")
    sumFilePath = os.path.join(os.getcwd(), f"P{args.inputfile[1:]}a.sum")

    # Decide which data sets to plot
    mappings = {"disp": "displacement", "time": "time", "force": "force"}
    x_identifier = args.x
    y_identifier = args.y

    # Setup plotting
    plt.ion()
    fig, ax = plt.subplots(1, 1)

    data = _read_data(disFilePath, sumFilePath)
    (line,) = ax.plot(data[x_identifier], data[y_identifier])

    ax.grid()
    plt.xlabel(mappings[x_identifier])
    plt.ylabel(mappings[y_identifier])

    # Plot loop
    while True:
        # Exit loop, if figure is manually closed
        if not plt.fignum_exists(fig.number):
            break
        else:
            data = _read_data(disFilePath, sumFilePath)
            xdata = data[x_identifier]
            ydata = data[y_identifier]
            line.set_xdata(xdata)
            line.set_ydata(ydata)
            ax.relim()
            ax.autoscale_view()
            fig.canvas.draw()
            fig.canvas.flush_events()
            time.sleep(args.refresh / 1000)


if __name__ == "__main__":
    main()
