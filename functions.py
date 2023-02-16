import cv2
import mediapipe as mp
import matplotlib.pyplot as plt
import numpy as np
import bpy

mp_pose = mp.solutions.pose
pose_image = mp_pose.Pose(static_image_mode=True, 
                          min_detection_confidence=0.5)
pose_video = mp_pose.Pose(static_image_mode=False, 
                          min_detection_confidence=0.7,
                          min_tracking_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose()

def detectPose(image_pose, pose, draw=False, display=False):
    original_image = image_pose.copy()
    image_in_RGB = cv2.cvtColor(image_pose, cv2.COLOR_BGR2RGB)
    resultant = pose.process(image_in_RGB)
    if resultant.pose_landmarks and draw:    
        mp_drawing.draw_landmarks(image=original_image, 
                                  landmark_list=resultant.pose_landmarks,
                                  connections=mp_pose.POSE_CONNECTIONS,
                                  landmark_drawing_spec=mp_drawing.DrawingSpec(color=(255,255,255),
                                                                               thickness=2, circle_radius=2),
                                  connection_drawing_spec=mp_drawing.DrawingSpec(color=(49,125,237),
                                                                               thickness=2, circle_radius=2))
    if display:
            plt.figure(figsize=[22,22])
            plt.subplot(121);plt.imshow(image_pose[:,:,::-1])
            plt.title("Input Image",size=14)
            plt.axis('off');
            plt.subplot(122);plt.imshow(original_image[:,:,::-1])
            plt.title("Pose detected Image",size=14)
            plt.axis('off');
 
    else:        
        return original_image, resultant

# PREPARING IMAGE
image = cv2.imread("test_slika.jpg")
slika, res = detectPose(image, pose, True)
slika = cv2.cvtColor(slika, cv2.COLOR_BGR2RGB)


def createSpinePoints(res):
    # PREPARING DATA - DICTIONARY WITH POINTS ON ALL AXIS
    points = []
    for data_point in res.pose_landmarks.landmark:
        points.append({
                        'X': data_point.x,
                        'Y': data_point.y,
                        'Z': data_point.z,
                        'Visibility': data_point.visibility})

    spineTopX1 = points[11]["X"]
    spineTopY1 = points[11]["Y"]
    spineTopZ1 = points[11]["Z"]

    spineTopX2 = points[12]["X"]
    spineTopY2 = points[12]["Y"]
    spineTopZ2 = points[12]["Z"]

    spineBotX1 = points[23]["X"]
    spineBotY1 = points[23]["Y"]
    spineBotZ1 = points[23]["Z"]

    spineBotX2 = points[24]["X"]
    spineBotY2 = points[24]["Y"]
    spineBotZ2 = points[24]["Z"]

    vec1 = np.array([spineTopX1, spineTopY1, spineTopZ1])
    vec2 = np.array([spineTopX2, spineTopY2, spineTopZ2])

    vec3 = np.array([spineBotX1, spineBotY1, spineBotZ1])
    vec4 = np.array([spineBotX2, spineBotY2, spineBotZ2])

    spineTop = (vec1 + vec2) / 2
    spineBot = (vec3 + vec4) / 2

    return spineTop, spineBot

