import numpy as np
import  os
import  json

def player_report(value,ideal, tolerance=10, smaller_is_better= False):
    if value  is None:
        return 0
    if smaller_is_better:
        point = max(1,10-int((value-ideal)/tolerance*10))
    else:
        point = max(1,10-int(abs(ideal-value)/tolerance*10))
    return min(point,10)

def final_evaluation(all_elbow_angles, all_spine_angles,all_head_knee_dist, all_foot_directions):
    avg_elbow_angle = np.mean(all_elbow_angles)
    avg_spine_angle = np.mean(all_spine_angles)
    avg_head_knee = np.mean(all_head_knee_dist)
    avg_foot = np.mean(all_foot_directions)

    #1-10 score

    report = {
        "Footwork": player_report(avg_foot,ideal=80),
        "Head Position": player_report(avg_head_knee,ideal = 0, smaller_is_better=True),
        "Swing Control": player_report(avg_elbow_angle, ideal = 150),
        "Balance": player_report(avg_spine_angle,ideal=0,smaller_is_better=True),
        "Follow-through": player_report(avg_elbow_angle,ideal=150),
        "Comments":[
            "Footwork is good; maintain balance and head alignment.",
            "Elbow position and follow-through can be improved for more control."
        ]
    }
    #save the Report to json
    output_folder  = 'output'
    os.makedirs(output_folder,exist_ok=True)
    output_file = os.path.join(output_folder,'evaluation.json')
    with open(output_file,'w') as f:
        json.dump(report, f,indent=4)

    print(f"Evaluation saved to {output_file}")
    return report




