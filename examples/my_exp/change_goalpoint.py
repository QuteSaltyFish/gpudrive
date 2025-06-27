# %%
# Dependencies
import json
import matplotlib.pyplot as plt
import os
from pathlib import Path
import seaborn as sns
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
%config InlineBackend.figure_format = 'svg'
sns.set("notebook", font_scale=1.1, rc={"figure.figsize": (8, 3)})
sns.set_style(
    "ticks", rc={"figure.facecolor": "none", "axes.facecolor": "none"})

# %%
# Take an example scene
data_path = "data/processed/testing/tfrecord-00005-of-00150_84.json"

with open(data_path) as file:
    traffic_scene = json.load(file)

print(traffic_scene.keys())

pd.Series(
    [
        traffic_scene["objects"][idx]["type"]
        for idx in range(len(traffic_scene["objects"]))
    ]
).value_counts().plot(kind="bar", rot=45, color=cmap)
plt.title(
    f'Distribution of road objects in traffic scene. Total # objects: {len(traffic_scene["objects"])}'
)
plt.show()
# Start to deal with traffic objects
new_objs = []
ids = [26]
count = 0
new_goalpoints = copy.deepcopy(traffic_scene["objects"][0]["goalPosition"])
for obj in traffic_scene["objects"]:
    new_obj = copy.deepcopy(obj)
    print(obj)
    if new_obj["id"] < 15:
        continue
    if new_obj["type"] == "vehicle" and new_obj["valid"][0] and new_obj["mark_as_expert"] == False:
        print(
            f"Object ID: {new_obj['id']}, Type: {new_obj['type']}, Position: {new_obj['position']}, Goal Point: {new_obj['goalPosition']}")
        new_obj["goalPosition"] = traffic_scene["objects"][0]["goalPosition"].copy()
        new_obj["goalPosition"]['x'] += 1
        new_obj["goalPosition"]['y'] += 2
        # new_obj["mark_as_expert"] ==
        new_objs.append(new_obj)

        # Copy a obj and add it to the new objects
        if count % 1 == 0:
            copy_obj = copy.deepcopy(new_obj)
            # copy_obj['length'] += 2
            for xyz in copy_obj['position']:
                xyz['y'] += 6
            copy_obj['id'] += 100
            new_objs.append(copy_obj)
        if count % 1 == 0:
            copy_obj = copy.deepcopy(new_obj)
            # copy_obj['length'] += 2
            for xyz in copy_obj['position']:
                xyz['y'] += 3
            copy_obj['id'] += 200
            new_objs.append(copy_obj)

        count += 1
        if count == 20:
            break

    # break
traffic_scene["objects"] = []
traffic_scene["metadata"]["sdc_track_index"] = -1
traffic_scene["metadata"]['tracks_to_predict'] = []
for road in traffic_scene['roads']:
    # types.add(road['type'])
    if road['type'] == 'road_line':
        road['type'] = 'road_edge'
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
# traffic_scene['metadata'] = {}
data_path = "data/exp/tfrecord-00005-of-00150_84_changed_goal.json"
json.dump(traffic_scene, open(data_path, "w"))

# %%
# Run the following command to visualize the scene with changed goal points

# %%
types = set()
for road in traffic_scene['roads']:
    types.add(road['type'])
    if road['type'] == 'road_line':
        road['type'] = 'road_edge'
# traffic_scene['roads'][0]['type']
# %%
types
# %%
