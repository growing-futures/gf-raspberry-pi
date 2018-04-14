#!/usr/bin/env python

import json
import random

json_string = """[
    {"measurement": "TowerData",
    "tags": {
        "towerName": "Tower_%s",
        "towerGroup": "Tower_Group_%s"
        },

        "fields": {
            "water_level": %d,
            "pH": %d,
            "light_sensor": "%s"
        }



    }]"""

tower_name_num = range(1,51)
tower_group_num = range(1,11)
water_level_num = range(1, 101)
pH = range(0, 15)
light_sensor = "off";

new_string = json_string % (random.choice(tower_name_num), random.choice(tower_group_num), random.choice(water_level_num), random.choice(pH), random.choice(["off", "on"]))

print new_string
