import matplotlib.pyplot as plt
import  os

#list to store all elbow anlge

elbow_angle_list = []

def track_elbow_angle(value_elbow_angle):
    if value_elbow_angle is not None:
        elbow_angle_list.append(value_elbow_angle)
def smoothness_graph(output_folder = 'graph'):
    os.makedirs(output_folder,exist_ok=True)
    output_path = os.path.join(output_folder,'elbow_angle_smoothness.png')

    plt.figure(figsize=(10,6))
    plt.plot(elbow_angle_list,label = 'Elbow Angle(degrees)', color = 'blue')
    plt.xlabel('Frame Number')
    plt.ylabel('Elbow Angle (degrees)')
    plt.title('Elbow Angle Over Time(Smoothness Check)')
    plt.legend()
    plt.grid(True)

    plt.savefig(output_path)
    plt.close()
    print(f":: Elbow angle smootness graph saved to {output_path}")