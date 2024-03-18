import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET

# Understanding fundamental diagram

output_edge_file = "outputs/TrafficFlowTest/edge_data.xml"
tree = ET.parse(output_edge_file)
root = tree.getroot()

# evaluate_traffic_state("temp", "inputs/TraffcFlowTest",
#                        ["outputs/trafficFlowTest"],
#                        # ["outputs/Rhombus", "outputs/Rhombus_r1", "outputs/Rhombus_r2"],
#                        "images", time_range=(0, 5 * 3600), time_resolution=3600)
# evaluate_sim_stats("temp", "inputs/TraffcFlowTest",
#                    ["outputs/trafficFlowTest"],
#                    # ["outputs/Rhombus", "outputs/Rhombus_r1", "outputs/Rhombus_r2"],
#                    "images", time_range=(0, 5 * 3600), time_resolution=3600)

edge_fd_dict = {}
for interval in root:
    for edge in interval:
        try:
            edge_id = edge.attrib["id"]
            edge_lane_density = float(edge.attrib['laneDensity'])
            edge_speed = float(edge.attrib['speed'])
            edge_flow = edge_lane_density * edge_speed * 3.6
            if not (edge_id in edge_fd_dict.keys()):
                edge_fd_dict[edge_id] = {"q": [], "k": [], "v": []}

            edge_fd_dict[edge_id]["q"].append(edge_flow)
            edge_fd_dict[edge_id]["v"].append(edge_speed)
            edge_fd_dict[edge_id]["k"].append(edge_lane_density)
        except KeyError:
            pass

plt.figure()
for edge_id, edge_fd in edge_fd_dict.items():
    edge_k = edge_fd["k"]
    edge_q = edge_fd['q']
    plt.scatter(edge_k, edge_q, label=edge_id, alpha=0.3)
plt.grid()
plt.legend()
plt.xlabel("Density (veh / (lane $\cdot$ km))")
plt.ylabel("Flow (veh / (lane $\cdot$ hour))")
plt.tight_layout()
# plt.savefig("fd.png", dpi=200)
plt.show()
