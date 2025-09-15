import numpy as np
# logic to calculate the angle

def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360 - angle
    return angle


# for elbow(front elbow angle)
def elbow_angle(keypoints):
    if keypoints['left_shoulder'] and keypoints['left_elbow'] and keypoints['left_wrist']:
        return calculate_angle(
            keypoints['left_shoulder'][:2],
            keypoints['left_elbow'][:2],
            keypoints['left_wrist'][:2]
        )
    return None


# for spine(angle between hip and shoulder)

def spine_angle(keypoints):
    if keypoints['left_hip'] and keypoints['left_shoulder']:
        hip = np.array(keypoints['left_hip'][:2])
        shoulder = np.array(keypoints['left_shoulder'][:2])
        vertical_axis = [hip[0], hip[1] - 0.1]

        return calculate_angle(shoulder, hip, vertical_axis)
    return None


# for ead-over-knee vertical alignment (distance between head and knee)

def head_over_knee(keypoints):
    if keypoints['head'] and keypoints['left_knee']:
        return abs(keypoints['head'][0] - keypoints['left_knee'][0])
    return None

    # for Front Foot directions(ankle to toe direction)


def foot_direction(keypoints):
    if keypoints['left_ankle'] and keypoints['left_knee']:
        return calculate_angle([keypoints['left_ankle'][0] - 0.1, keypoints['left_ankle'][1]],
                               keypoints['left_ankle'][:2],
                               keypoints['left_knee'][:2]
                               )
    return None