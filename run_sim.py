import sys
import traci

# Define the path to the SUMO binary and the network configuration file
sumo_bin = "C:/Program Files (x86)/Eclipse/Sumo/bin/sumo"  # Replace with the actual path to your SUMO binary
# sumo_cmd = [sumo_bin, "-c", "scenarios/Rhombus/run.cfg.xml"]  # Replace with your network configuration file
sumo_cmd = [sumo_bin, "-c", "scenarios/TrafficFlowTest/run.cfg.xml"]  # Replace with your network configuration file

# Start the SUMO simulation with TraCI
sumo_process = traci.start(sumo_cmd)

# Initialize the simulation
traci.simulationStep()

timestep = 0

while traci.simulation.getMinExpectedNumber() > 0:  # Continue while there are active vehicles
    # Your model logic goes here
    timestep += 1
    # Advance the simulation time by a small time step
    traci.simulationStep()

# End the simulation and clean up TraCI
traci.close()
sys.exit()
