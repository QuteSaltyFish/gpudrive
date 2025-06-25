# %%
# Dependencies
import json
import matplotlib.pyplot as plt
import os
from pathlib import Path
import seaborn as sns
import pandas as pd

# Set working directory to the base directory 'gpudrive'
working_dir = Path.cwd()
# while working_dir.name != 'gpudrive':
#     working_dir = working_dir.parent
#     if working_dir == Path.home():
#         raise FileNotFoundError("Base directory 'gpudrive' not found")
# os.chdir(working_dir)

cmap = ["r", "g", "b", "y", "c"]
%config InlineBackend.figure_format = 'svg'
sns.set("notebook", font_scale=1.1, rc={"figure.figsize": (8, 3)})
sns.set_style(
    "ticks", rc={"figure.facecolor": "none", "axes.facecolor": "none"})

# %%
