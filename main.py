import time
import random

import cv2

from MidiHandler import MidiHandler
from MediapipeWrapper import MediapipeWrapper


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

    def run(s):
        while s.v_in.isOpened():
            frame = s.get_processed_frame()
            # Now process each wanted part
            # Reset the image as writable to display the results
            detection_data = s.m_wrapper.process(frame, detection_flags=['hands'])

            # Now reverse the frame transformations
            frame.flags.writeable = True
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            # Draw the annotations on the image.
            frame = s.m_wrapper.draw(frame, detection_data)
            # cv2.imshow('VideoMidi', frame)
            cv2.imshow('VideoMidi', frame)

            # s.midi_handler.send(random.randint(30, 110), 100)
            if cv2.waitKey(5) & 0xFF == 27:
                break
            s.handle_sleep()

        s.midi_handler.close_midi()
        s.v_in.release()

    def get_processed_frame(s):
        """ Get the frame, convert to RGB, mark as non writable for performance"""
        success, frame = s.v_in.read()
        if not success:
            return
        # Flip the image horizontally for a later selfie-view display
        frame = cv2.flip(frame, 1)
        # Convert the BGR image to RGB.
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # To improve performance, mark the image as not writeable (pass by reference)
        frame.flags.writeable = False
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
    app = App(fps=30)
    app.run()
    # ret, frame = app.cam.read()
    # cv2.imwrite('./images/hh.png', frame)
