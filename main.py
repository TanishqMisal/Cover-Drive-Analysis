from time import process_time_ns
import cv2 as cv
import  mediapipe as mp
from metrics import elbow_angle,spine_angle,head_over_knee,foot_direction
import time
from fontTools.misc.cython import returns
from numpy.ma.core import left_shift
from scipy.cluster.hierarchy import from_mlab_linkage
from evaluation import final_evaluation
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose


all_elbow_angles = []
all_spine_angles = []
all_head_knee_dist = []
all_foot_directions = []
Video = 'C:\Cover-Drive-Analysis\downloaded_video.mp4'
output_video = "C:\Cover-Drive-Analysis\output"
cap = cv.VideoCapture(Video)

fps = int(cap.get(cv.CAP_PROP_FPS))
width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))

fourcc = cv.VideoWriter_fourcc(*"mp4v")
out = cv.VideoWriter(output_video+"\\annotated_video.mp4", fourcc, fps, (width, height))

#frame counter
frame_counter = 0
frame_time= 0
final_time =0

with mp_pose.Pose(min_detection_confidence=0.5,min_tracking_confidence=0.5)as pose:
    while cap.isOpened():
        start_time= time.time()
        ret, frame = cap.read()

        if not ret:
            print("Failed to grab frame, Video might ended")
            break

        #recolor:- format RGB
        image = cv.cvtColor(frame,cv.COLOR_BGR2RGB)
        image.flags.writeable = False#save memory

        #Making detection:- saved in array
        res = pose.process(image)

        #Color back to original
        image.flags.writeable = True
        image = cv.cvtColor(image, cv.COLOR_RGB2BGR)
        #Extrack landmarks

        try:
            #extracting co-ordinate from the video
            if res.pose_landmarks:
                landmarks = res.pose_landmarks.landmark

                def get_keypoint(name):
                    lm = landmarks[mp_pose.PoseLandmark[name].value]
                    if lm.visibility>= 0.3:
                        return[lm.x,lm.y,lm.z]

                    else:
                        return None
                #The keypoints stored in tuples:
                keypoints = {
                    'head': get_keypoint('NOSE'),
                    'left_shoulder': get_keypoint('LEFT_SHOULDER'),
                    'right_shoulder':get_keypoint('RIGHT_SHOULDER'),
                    'left_elbow':get_keypoint('LEFT_ELBOW'),
                    'right_elbow':get_keypoint('RIGHT_ELBOW'),
                    'left_wrist':get_keypoint('LEFT_WRIST'),
                    'right_wrist':get_keypoint('RIGHT_WRIST'),
                    'left_hip':get_keypoint('LEFT_HIP'),
                    'right_hip':get_keypoint('RIGHT_HIP'),
                    'left_knee':get_keypoint('LEFT_KNEE'),
                    'left_ankle':get_keypoint('LEFT_ANKLE'),
                    'right_ankle':get_keypoint('RIGHT_ANKLE'),
                }
                ''' ''#display the coordinates
                for part, coords in keypoints.items():
                    if coords:
                        print(f"{part}: x = {coords[0]:.3f},y={coords[1]:.3},z = {coords[2]:.3f}")
                    else:
                        print(f"{part}: Low visibility")'''



                value_elbow_angle = elbow_angle(keypoints)
                value_spine = spine_angle(keypoints)
                value_knee_align = head_over_knee(keypoints)
                value_foot = foot_direction(keypoints)

                if value_elbow_angle is not None:
                    all_elbow_angles.append(value_elbow_angle)
                if value_spine is not None:
                    all_spine_angles.append(value_spine)
                if value_knee_align is not None:
                    all_head_knee_dist.append(value_knee_align)
                if value_foot is not None:
                    all_foot_directions.append(value_foot)

                cv.putText(image, f"Elbow Angle : {value_elbow_angle}",(10,30),cv.FONT_HERSHEY_SIMPLEX,0.7,(0,225,0),2)
                cv.putText(image,f"Spine Lean : {value_spine}",(10,60),cv.FONT_HERSHEY_SIMPLEX,0.7,(0,255,0),2)
                cv.putText(image,f"Head and knee : {value_knee_align}",(10,90),cv.FONT_HERSHEY_SIMPLEX,0.7,(0,255,0),2)
                cv.putText(image,f"Foot Directions : {value_foot}",(10,120),cv.FONT_HERSHEY_SIMPLEX,0.7,(0,255,0),2)

                #Threshold to be check for a good cover drive
                Thresholds = {
                    'elbow_angle':150,
                    'head_over_knee':0.05,
                    'spine_angle': 15,
                    'foot_direction':80,
                }

                #Feedback or tips
                Improve = {
                    'elbow_angle':["Elbow too low","Good elbow"],
                    'head_over_knee':["Head not over front knee","Head aligned over knee"],
                    'spine_angle':['Spine leaning to much','Spine alignment good'],
                    'foot_direction':['Foot misaligned','good Footwork']
                }

                #functino to create feedback as per performance
                def get_feedback(metric_name, value):
                    if value is None:
                        return ""

                    threshold = Thresholds[metric_name]

                    if metric_name == 'head_over_knee':
                        return Improve[metric_name][1] if value <= threshold else Improve[metric_name][0]
                    else:
                        return Improve[metric_name][1] if value >= threshold else Improve[metric_name][0]

                #Get the feedback
                tip_elbow = get_feedback('elbow_angle',value_elbow_angle)
                tip_head = get_feedback('head_over_knee',value_knee_align)
                tip_spine = get_feedback('spine_angle',value_spine)
                tip_foot = get_feedback('foot_direction',value_foot)

                cv.putText(image,tip_elbow,(10,150),cv.FONT_HERSHEY_SIMPLEX,0.7,(0,255,255),2)
                cv.putText(image,tip_head,(10,180),cv.FONT_HERSHEY_SIMPLEX,0.7,(0,255,255),2)
                cv.putText(image,tip_spine,(10,210),cv.FONT_HERSHEY_SIMPLEX,0.7,(0,255,255),2)
                cv.putText(image,tip_foot,(10,240),cv.FONT_HERSHEY_SIMPLEX,0.7,(0,255,255),2)
        except:
            print('Error')
        # render detections
        mp_drawing.draw_landmarks(image,
                                  res.pose_landmarks,
                                  mp_pose.POSE_CONNECTIONS,
                                  mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=4),
                                  mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2),
                                  )
        frame = cv.flip(frame,1)
        cv.imshow("Mediapipe",image)
        out.write(image)

        frame_counter +=1
        end_time = time.time()

        pass_time = end_time-start_time
        final_time += pass_time

        if frame_counter % 30==0:
            fps = frame_counter/final_time
            print(f"Performacne: Average FPS:{fps:2f}")

        if cv.waitKey(10)&0xFF == ord('q'):
            break


cap.release()
cv.destroyAllWindows()
print("[: Program finished")

summary = final_evaluation(all_elbow_angles,all_spine_angles,all_head_knee_dist,all_foot_directions)
print(summary)

