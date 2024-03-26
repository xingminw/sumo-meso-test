import sys
import traci
import matplotlib.pyplot as plt
from random import random

# Define the path to the SUMO binary and the network configuration file
sumo_bin = "C:/Program Files (x86)/Eclipse/Sumo/bin/sumo"  # Replace with the actual path to your SUMO binary
# sumo_cmd = [sumo_bin, "-c", "scenarios/Rhombus/run.cfg.xml"]  # Replace with your network configuration file
sumo_cmd = [sumo_bin, "-c", "scenarios/TrafficFlowTest/run.cfg.xml"]  # Replace with your network configuration file

# Start the SUMO simulation with TraCI
sumo_process = traci.start(sumo_cmd)

# Initialize the simulation
traci.simulationStep()

timestep = 0
vehicle_ts_dict = {}
deleted_vehicles, inserted_vehicles = [], []

while traci.simulation.getMinExpectedNumber() > 0:  # Continue while there are active vehicles
    if timestep >= 500:
        break

    # Your model logic goes here
    vehicle_ids = traci.vehicle.getIDList()

    stop_lane_count = 0
    for vehicle_id in vehicle_ids:
        if not (vehicle_id in vehicle_ts_dict.keys()):
            vehicle_ts_dict[vehicle_id] = {"time": [], "distance": []}
        vehicle_dis = traci.vehicle.getDistance(vehicle_id)
        vehicle_edge = traci.vehicle.getRoadID(vehicle_id)
        vehicle_edge_dis = traci.vehicle.getLanePosition(vehicle_id)

        vehicle_lane_id = traci.vehicle.getLaneID(vehicle_id)
        vehicle_lane_int = traci.vehicle.getLaneIndex(vehicle_id)
        route_id = traci.vehicle.getRouteID(vehicle_id)

        vehicle_speed = traci.vehicle.getSpeed(vehicle_id)
        vehicle_type = traci.vehicle.getTypeID(vehicle_id)

        if vehicle_edge == "E0":
            vehicle_ts_dict[vehicle_id]["time"].append(timestep)
            vehicle_ts_dict[vehicle_id]["distance"].append(vehicle_edge_dis)
        elif vehicle_edge == "E2":
            vehicle_ts_dict[vehicle_id]["time"].append(timestep)
            # fixme: 518.66 is the length of the edge E0
            vehicle_ts_dict[vehicle_id]["distance"].append(vehicle_edge_dis + 518.66)

        # # move the vehicle test (-- does not work for meso --)
        # if timestep - vehicle_ts_dict[vehicle_id]["time"][0] == 10:
        #     traci.vehicle.moveTo(vehicle_id, vehicle_lane_id, vehicle_edge_dis + 150)

        # # delete and reinsert vehicles
        # if vehicle_edge == "E0" and vehicle_edge_dis > 200:
        #     if vehicle_id not in inserted_vehicles:
        #         deleted_vehicles.append(vehicle_id)
        #         traci.vehicle.remove(vehicle_id)
        #
        #         insert_veh_id = vehicle_id + "-0"
        #         traci.vehicle.add(insert_veh_id, route_id,
        #                           typeID=vehicle_type, depart="now",
        #                           departLane="best",
        #                           departPos=vehicle_edge_dis + 200,
        #                           departSpeed=vehicle_speed)
        #         inserted_vehicles.append(insert_veh_id)

        # set vehicle to stop and resume (-- does not work for meso --)

        # if timestep == 275 and stop_lane_count < 1:
        #     # traci.vehicle.slowDown(vehicle_id, 0, 10)
        #     if vehicle_edge_dis <= 200 and vehicle_edge == "E0":
        #         print(stop_lane_count)
        #         stop_lane_index = int(stop_lane_count % 3)
        #         traci.vehicle.setStop(vehicle_id, vehicle_edge,
        #                               # laneIndex=vehicle_lane_int,
        #                               # laneIndex=stop_lane_index,
        #                               pos=300, duration=30)
        #         print(f"Lane {stop_lane_index} is set as stop for vehicle {vehicle_id}")
        #         stop_lane_count += 1

    # disallow lane usage test
    if timestep == 250:
        traci.lane.setMaxSpeed("E2_0", 0)
        # for vehicle_id in vehicle_ids:
        #     if traci.vehicle.getRoadID(vehicle_id) == "E2":
        #         traci.vehicle.remove(vehicle_id)
        #         deleted_vehicles.append(vehicle_id)

        # traci.lane.setMaxSpeed("E2_1", 0)
        # traci.lane.setMaxSpeed("E2_2", 20)
        # traci.edge.setMaxSpeed("E2", 0)
    if timestep == 300:
        # traci.lane.setMaxSpeed("E2_0", 20)
        # traci.lane.setMaxSpeed("E2_1", 20)
        # traci.lane.setMaxSpeed("E2_2", 20)
        # traci.edge.setMaxSpeed("E2", 20)
        pass

    # Advance the simulation time by a small time step
    timestep += 1
    traci.simulationStep()


plt.figure(figsize=(10, 5))
for vehicle_id in vehicle_ts_dict.keys():
    if vehicle_id in deleted_vehicles:
        color, alpha = "red", 1
    elif vehicle_id in inserted_vehicles:
        color, alpha = "blue", 1
    else:
        color, alpha = "k", 0.2
    plt.plot(vehicle_ts_dict[vehicle_id]["time"],
             vehicle_ts_dict[vehicle_id]["distance"],
             ".-", alpha=alpha, color=color)

plt.axvline(250, color="r", linestyle="--")
plt.axhline(518.66, color="b", linestyle="--")
plt.xlim([200, 500])
plt.grid()
plt.xlabel("Time (s)")
plt.ylabel("Distance (m)")
plt.tight_layout()
plt.show()

# End the simulation and clean up TraCI
traci.close()
sys.exit()
