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
deleted_vehicles, reinsert_vehicles = [], []

while traci.simulation.getMinExpectedNumber() > 0:  # Continue while there are active vehicles
    if timestep >= 800:
        break

    # Your model logic goes here
    vehicle_ids = traci.vehicle.getIDList()
    for vehicle_id in vehicle_ids:
        if not (vehicle_id in vehicle_ts_dict.keys()):
            vehicle_ts_dict[vehicle_id] = {"time": [], "distance": []}
        vehicle_dis = traci.vehicle.getDistance(vehicle_id)
        vehicle_edge = traci.vehicle.getRoadID(vehicle_id)
        vehicle_edge_dis = traci.vehicle.getLanePosition(vehicle_id)
        vehicle_lane_id = traci.vehicle.getLaneID(vehicle_id)

        vehicle_ts_dict[vehicle_id]["time"].append(timestep)
        vehicle_ts_dict[vehicle_id]["distance"].append(vehicle_dis)

        # move the vehicle test (-- does not work --)
        # if timestep - vehicle_ts_dict[vehicle_id]["time"][0] == 10:
        #     traci.vehicle.moveTo(vehicle_id, vehicle_lane_id, vehicle_edge_dis + 150)
        # delete the vehicle
        if timestep - vehicle_ts_dict[vehicle_id]["time"][0] == 20:
            if random() < 0.2:
                deleted_vehicles.append(vehicle_id)
                traci.vehicle.remove(vehicle_id)
                reinsert_vehicles.append(vehicle_id)

        # reinsert vehicles

    # Advance the simulation time by a small time step
    timestep += 1
    traci.simulationStep()

plt.figure(figsize=(10, 5))
for vehicle_id in vehicle_ts_dict.keys():
    if vehicle_id in deleted_vehicles:
        color, alpha = "red", 1
    else:
        color, alpha = "k", 0.5
    plt.plot(vehicle_ts_dict[vehicle_id]["time"],
             vehicle_ts_dict[vehicle_id]["distance"],
             ".-", alpha=alpha, color=color)

plt.xlim([500, 800])
plt.grid()
plt.xlabel("Time (s)")
plt.ylabel("Distance (m)")
plt.tight_layout()
plt.show()

# End the simulation and clean up TraCI
traci.close()
sys.exit()
