import time
import random

import cv2

from MidiHandler import MidiHandler
from MediapipeWrapper import MediapipeWrapper
import musical_utils


class App(object):
    def __init__(s, fps):
        # FPS Handling
        s.delta = 1 / fps
        s.frame_start_time = time.time()
        # CV2
        s.v_in = cv2.VideoCapture(0)
        # Midi
        s.midi_handler = MidiHandler()
        # Video Analysis
        s.m_wrapper = MediapipeWrapper()
        # Musical
        s.scale = musical_utils.get_minor_scale()

    def run(s):
        while s.v_in.isOpened():
            frame = s.get_processed_frame()
            # Now process each wanted part
            # Reset the image as writable to display the results
            detection_data = s.m_wrapper.process(frame, detection_flags=['hands'], draw=True)
            s.transform_data_to_music(detection_data)

            if cv2.waitKey(5) & 0xFF == 27:
                break
            s.handle_sleep()

        s.midi_handler.close_midi()
        s.v_in.release()

    def transform_data_to_music(s, detection_data):
        s.midi_handler.send(60 + random.choice(s.scale), 100, delta=0)
        s.midi_handler.send(60 + random.choice(s.scale), 100, delta=100, stop_previous=False)
        s.midi_handler.send(60 + random.choice(s.scale), 100, delta=200, stop_previous=False)

    def get_processed_frame(s):
        """ Get the frame, convert to RGB, mark as non writable for performance"""
        success, frame = s.v_in.read()
        if not success:
            return
        # Flip the image horizontally for a later selfie-view display
        frame = cv2.flip(frame, 1)
        return frame

    def handle_sleep(s):
        """Maintains the framerate"""
        to_sleep = s.delta - (time.time() - s.frame_start_time)
        if to_sleep > 0:
            time.sleep(to_sleep)
        elif (to_sleep < -0.1):
            print(f"[-] - Lagging {-to_sleep:.2f} seconds behind")
        s.frame_start_time = time.time()


if __name__ == '__main__':
    app = App(fps=1)
    app.run()
    # ret, frame = app.cam.read()
    # cv2.imwrite('./images/hh.png', frame)
