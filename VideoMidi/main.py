#!/usr/bin/env python3
import time
import random

import cv2

from MidiHandler import MidiHandler
from MediapipeWrapper import MediapipeWrapper
import musical_utils


class App(object):
    def __init__(s, fps, tempo):
        # FPS Handling
        s.frame_delta = 1 / fps
        s.last_fps_eval_time = time.time()
        # Tempo Handling
        s.tempo_delta = 60 / tempo
        s.last_tempo_tick = time.time()
        # CV2
        s.v_in = cv2.VideoCapture(0)
        # Midi
        s.midi_handler = MidiHandler()
        # Video Analysis
        s.m_wrapper = MediapipeWrapper()
        # Musical
        s.scale = musical_utils.get_minor_scale()
        s.root_key = 60

    def run(s):
        while s.v_in.isOpened():
            frame = s.get_processed_frame()
            if cv2.waitKey(5) & 0xFF == 27:
                break
            if s.handle_tempo():
                # Now process each wanted part
                frame, detection_data = s.m_wrapper.process(frame, detection_flags=['hands'], draw=True)
                s.transform_data_to_music(detection_data)
            # Show annotated image
            cv2.imshow('VideoMidi', frame)

            s.handle_framerate()

        s.midi_handler.close_midi()
        s.v_in.release()

    def transform_data_to_music(s, detection_data):
        if 'hands' in detection_data:
            s.hands_data_to_music(detection_data['hands'])
        # if 'face' in detection_data:
        #     s.face_data_to_music(detection_data['face'])
        # if 'pose' in detection_data:
        #     s.pose_data_to_music(detection_data['pose'])

    def hands_data_to_music(s, hands_data):
        if len(hands_data.multi_handedness) > 1:
            for hand_data_str in hands_data.multi_handedness:
                handedness_dict = MessageToDict(hand_handedness)
                for idx, hand_landmarks in enumerate(hands_data.multi_hand_landmarks):
                    pass
                key = s.transform_right_hand_ifp_to_key()
                # velo = s.transform_left_hand_ifp_to_velo()
        else:
            # Only one hand detected, switch single hand mode:
            # ifp height = velocity, ifp x_pos = key
            hand_landmarks = hands_data.multi_hand_landmarks[0]
            ifp_pos = hand_landmarks.landmark[s.m_wrapper.mp_hands.HandLandmark.INDEX_FINGER_TIP]
            key, velo = s.transform_hand_ifp_to_key(ifp_pos)

        s.midi_handler.send(key, velo)
        # s.midi_handler.send(key, velo, delta=0)

    def transform_hand_ifp_to_key(s, ifp_pos):
        """ All pos are between 0 and 1 """
        key = int(ifp_pos.x * 127)
        velo = int((1 - ifp_pos.y) * 127)
        return s.transform_to_scale(key), velo

    def transform_to_scale(s, key):
        return key

    def get_processed_frame(s):
        """ Get the frame, convert to RGB, mark as non writable for performance"""
        success, frame = s.v_in.read()
        if not success:
            return
        # Flip the image horizontally for a later selfie-view display
        frame = cv2.flip(frame, 1)
        return frame

    def handle_framerate(s):
        """Maintains the framerate"""
        to_sleep = s.frame_delta - (time.time() - s.last_fps_eval_time)
        if to_sleep > 0:
            time.sleep(to_sleep)
        elif (to_sleep < -0.1):
            print(f"[-] - Lagging {-to_sleep:.2f} seconds behind")
        s.last_fps_eval_time = time.time()

    def handle_tempo(s):
        """Maintains the tempo, return True if next beat is reached"""
        to_wait = s.tempo_delta - (time.time() - s.last_tempo_tick)
        if to_wait > 0:
            return False
        s.last_tempo_tick = time.time()
        return True


if __name__ == '__main__':
    app = App(fps=30, tempo=140)
    app.run()
    # ret, frame = app.cam.read()
    # cv2.imwrite('./images/hh.png', frame)
