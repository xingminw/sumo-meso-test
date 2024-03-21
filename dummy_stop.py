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

    if timestep == 275:
        traci.vehicle.add("E0_dummy_stop_01", "r_0",
                          typeID="DEFAULT_VEHTYPE", depart="now",
                          departPos=200,  departSpeed=0,
                          departLane="best")
        inserted_vehicles.append("E0_dummy_stop_01")
        traci.vehicle.setStop("E0_dummy_stop_01", "E0",
                              laneIndex=0, pos=200, duration=60)

        traci.vehicle.add("E0_dummy_stop_02", "r_0",
                          typeID="DEFAULT_VEHTYPE", depart="now",
                          departPos=200, departSpeed=0,
                          departLane="best")
        inserted_vehicles.append("E0_dummy_stop_02")
        traci.vehicle.setStop("E0_dummy_stop_02", "E0",
                              laneIndex=1, pos=200, duration=60)

        traci.vehicle.add("E0_dummy_stop_03", "r_0",
                          typeID="DEFAULT_VEHTYPE", depart="now",
                          departPos=200, departSpeed=0,
                          departLane="best")
        inserted_vehicles.append("E0_dummy_stop_03")
        traci.vehicle.setStop("E0_dummy_stop_03", "E0",
                              laneIndex=2, pos=200, duration=60)

    if timestep == 350:
        traci.vehicle.remove("E0_dummy_stop_01")
        traci.vehicle.remove("E0_dummy_stop_02")
        traci.vehicle.remove("E0_dummy_stop_03")

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

plt.xlim([200, 400])
plt.grid()
plt.xlabel("Time (s)")
plt.ylabel("Distance (m)")
plt.tight_layout()
plt.show()

# End the simulation and clean up TraCI
traci.close()
sys.exit()
