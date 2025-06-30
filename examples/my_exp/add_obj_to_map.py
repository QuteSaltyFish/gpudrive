# %%
# Dependencies
import json
import matplotlib.pyplot as plt
import os
from pathlib import Path
import numpy as np
import seaborn as sns
import math
import pandas as pd
import copy

# Set working directory to the base directory 'gpudrive'
working_dir = Path.cwd()
while not 'gpudrive' in working_dir.name:
    working_dir = working_dir.parent
    if working_dir == Path.home():
        raise FileNotFoundError("Base directory 'gpudrive' not found")
os.chdir(working_dir)

cmap = ["r", "g", "b", "y", "c"]
sns.set("notebook", font_scale=1.1, rc={"figure.figsize": (8, 3)})
sns.set_style(
    "ticks", rc={"figure.facecolor": "none", "axes.facecolor": "none"})

# Take an example scene
data_path = "data/processed_small_no_obj.json"

with open(data_path) as file:
    traffic_scene = json.load(file)

print(traffic_scene.keys())
traffic_scene["objects"] = []
traffic_scene["metadata"]["sdc_track_index"] = -1
traffic_scene["metadata"]['tracks_to_predict'] = []
types = set()
for road in traffic_scene['roads']:
    types.add(road['type'])
    if road['id'] == 634:
    #     road['type'] = 'road_edge'
        lane = road
print(lane)

lane['geometry'] =  lane['geometry'][:10]
obj = {}
obj["type"] = "vehicle"
obj['id'] = 1
obj['position'] = lane['geometry']
obj['valid'] = [True for _ in range(len(lane['geometry']))]
obj['goalPosition'] = lane['geometry'][-1]
obj['mark_as_expert'] = False
obj['width'] = 2.0
obj['length'] = 4.0
obj['height'] = 1.5
obj['velocity'] =[ {'x': 0.0, 'y': 0.0, } for _ in range(len(lane['geometry']))]
obj['heading'] = [0.0 for _ in range(len(lane['geometry']))]
for i in range(len(lane['geometry'])):
    if i == 0:
        continue
    obj['velocity'][i]['x'] = 0.1 * (obj['position'][i]['x'] - obj['position'][i-1]['x'])
    obj['velocity'][i]['y'] = 0.1 * (obj['position'][i]['y'] - obj['position'][i-1]['y'])
    obj['heading'][i-1] = np.arctan2(obj['velocity'][i]['y'], obj['velocity'][i]['x'])

#
# pd.Series(
#     [
#         traffic_scene["objects"][idx]["type"]
#         for idx in range(len(traffic_scene["objects"]))
#     ]
# ).value_counts().plot(kind="bar", rot=45, color=cmap)
# plt.title(
#     f'Distribution of road objects in traffic scene. Total # objects: {len(traffic_scene["objects"])}'
# )
# plt.show()
traffic_scene['objects'] = [obj]
data_path = "data/exp/new_map.json"
json.dump(traffic_scene, open(data_path, "w"))

# %%
