"""Client for Example 3 of pcaspy."""

from epics import caput, caget
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import time


# Run the simulation
status_code = caput("MTEST:Run", 1)

# let PV get updated before we read it...
time.sleep(1.0)

# Create initial plot
fig, ax = plt.subplots()
graph = ax.plot([0], [0], color="g")[0]
plt.ylim(0, 10)


# creating the first plot and frame
def update(frame):
    """Update graph using call to oscilloscope channel access."""
    global graph

    # updating the data
    data = caget("MTEST:Waveform")

    # creating a new graph or updating the graph
    graph.set_xdata(range(len(data)))
    graph.set_ydata(data)
    plt.xlim(0, len(data))
    plt.ylim(min(data), max(data))


anim = FuncAnimation(fig, update, frames=None)
plt.show()
