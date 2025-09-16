import numpy as np
import os
import json
with open("config.json") as f:
    CONFIG = json.load(f)

THRESHOLD = CONFIG["thresholds"]
TOLERANCE = CONFIG["tolerances"]
IDEALS = CONFIG["ideal_values"]
def player_report(value,metric_name, tolerance=10, smaller_is_better= False):
    if value  is None:
        return 0

    ideal = IDEALS[metric_name]
    tolerance = TOLERANCE[metric_name]

    if abs(value-ideal) <= tolerance:
        score = 10
    else:
        deviation = abs(value-ideal)-tolerance
        max_deviation = tolerance*3

        if deviation >= max_deviation:
            score = 1
        else:
            score = max(1,10-int((deviation/max_deviation)))

    comment_dict = {
        "elbow_angle": "Good arm extension" if score >= 7 else"Elbow position could be improved",
        "spine_angle": "Solid balance and posture" if score >= 7 else "Posture needs improvement",
        "head_over_knee": "Head well -positioned over the front knee" if score >= 7 else "Head position could be more stable",
        "foot_direction": "Excellent foot placement"if score >=7 else "Footwork needs to be worked"
        }
    return {
        "score": score,
        "average_value": round(value,2),
        "comment": comment_dict.get(metric_name,"")
    }

def final_evaluation(all_elbow_angles, all_spine_angles,all_head_knee_dist, all_foot_directions):
    avg_elbow_angle = np.mean(all_elbow_angles)
    avg_spine_angle = np.mean(all_spine_angles)
    avg_head_knee = np.mean(all_head_knee_dist)
    avg_foot = np.mean(all_foot_directions)

    #1-10 score

    report = {
        "elbow_angle": player_report(avg_elbow_angle,"elbow_angle"),
        "spine_lean": player_report(avg_spine_angle,"spine_angle", smaller_is_better=True),
        "head_over_knee": player_report(avg_head_knee, "head_over_knee",smaller_is_better=True),
        "foot_direction": player_report(avg_foot,"foot_direction"),
        "summary": "A strong performance with great footwork and swing. Focus on keeping the head still and over the front knee for better balance and power"
    }
    #save the Report to json
    output_folder  = 'output'
    os.makedirs(output_folder,exist_ok=True)
    output_file = os.path.join(output_folder,'evaluation.json')
    with open(output_file,'w') as f:
        json.dump(report, f,indent=4)

    print(f"Evaluation saved to {output_file}")
    return report




