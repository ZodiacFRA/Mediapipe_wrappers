#!/usr/bin/env python3
import cv2
import mediapipe as mp


class MediapipeWrapper(object):
    def __init__(s):
        # Mediapipe util
        s.mp_drawing = mp.solutions.drawing_utils
        s.drawing_spec = s.mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
        # Hands tracking
        s.mp_hands = mp.solutions.hands
        s.hands = s.mp_hands.Hands(
                            min_detection_confidence=0.7,
                            min_tracking_confidence=0.5
                        )
        # Face mesh
        s.mp_face_mesh = mp.solutions.face_mesh
        s.face_mesh = s.mp_face_mesh.FaceMesh(
                            min_detection_confidence=0.5,
                            min_tracking_confidence=0.5
                        )
        s.mp_pose = mp.solutions.pose
        s.pose = s.mp_pose.Pose(
                            min_detection_confidence=0.5,
                            min_tracking_confidence=0.5
                        )

    def process(s, frame, detection_flags, draw=True):
        ### Prepare frame for detection
        # Convert the BGR image to RGB.
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # To improve performance, mark the image as not writeable (pass by reference)
        frame.flags.writeable = False

        res = {}
        if 'hands' in detection_flags:
            res['hands'] = s.get_hands_data(frame)
        if 'face' in detection_flags:
            res['face'] = s.get_face_data(frame)
        if 'pose' in detection_flags:
            res['pose'] = s.get_pose_data(frame)

        if draw:
            # Reverse the frame transformations
            frame.flags.writeable = True
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            # Draw the annotations on the image.
            frame = s.draw(frame, res)
        return frame, res

    def draw(s, frame, detection_data):
        if not detection_data:
            return
        f_height, f_width, _ = frame.shape
        if 'hands' in detection_data and detection_data['hands'] and detection_data['hands'].multi_hand_landmarks:
            frame = s.draw_hands_data(frame, detection_data['hands'], f_height, f_width)
        if 'face' in detection_data and detection_data['face'] and detection_data['face'].multi_face_landmarks:
            frame = s.draw_face_data(frame, detection_data['face'], f_height, f_width)
        if 'pose' in detection_data:
            frame = s.draw_pose_data(frame, detection_data['pose'], f_height, f_width)
        return frame

    def get_hands_data(s, frame):
        return s.hands.process(frame)

    def draw_hands_data(s, frame, results, f_height, f_width):
        for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
            # ifp = hand_landmarks.landmark[s.mp_hands.HandLandmark.INDEX_FINGER_TIP]
            # print(f'Hand {idx} index finger tip x={ifp.x * image_width}, y={ifp.y * image_ehight}')
            s.mp_drawing.draw_landmarks(frame, hand_landmarks, s.mp_hands.HAND_CONNECTIONS)
        return frame

    def get_face_data(s, frame):
        return s.face_mesh.process(frame)

    def draw_face_data(s, frame, results, f_height, f_width):
        for face_landmarks in results.multi_face_landmarks:
            s.mp_drawing.draw_landmarks(
                                image=frame,
                                landmark_list=face_landmarks,
                                connections=s.mp_face_mesh.FACE_CONNECTIONS,
                                landmark_drawing_spec=s.drawing_spec,
                                connection_drawing_spec=s.drawing_spec
                            )
        return frame

    def get_pose_data(s, frame):
        return s.pose.process(frame)

    def draw_pose_data(s, frame, results, f_height, f_width):
        s.mp_drawing.draw_landmarks(frame, results.pose_landmarks, s.mp_pose.POSE_CONNECTIONS)
        return frame

    def __del__(s):
        s.hands.close()
        s.face_mesh.close()
        s.pose.close()
