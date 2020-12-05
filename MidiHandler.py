import pygame.midi


class MidiHandler(object):
    def __init__(s):
        pygame.midi.init()

        device_idx = 2
        s.initialized = True
        try:
            print(f'{device_idx}:', pygame.midi.get_device_info(device_idx))
            # latency=1 is needed for pygame to take the timestamps into account
            s.output = pygame.midi.Output(device_idx, latency=1)
        except pygame.midi.MidiException:
            print('[-] - Cound not connect to midi device')
            s.initialized = False
        s.previous_note = None

    def close_midi(s):
        if not s.initialized:
            return
        for note in range(0, 127):
            s.output.write_short(0x80, note, 0)
        s.output.close()

    def send(s, note, velo, delta=0, stop_previous=True):
        if not s.initialized:
            return
        # Ox90 = note on, Ox80 = note off

        # s.output.write_short(0x90, note, velo)

        # 1000 = 1sec
        midi_time = pygame.midi.time()

        if s.previous_note:
            s.output.write([[[0x80, s.previous_note, velo], midi_time]])
        s.previous_note = note

        s.output.write([[[0x90, note, velo], midi_time + delta]])




if __name__ == '__main__':
    midi_handler = MidiHandler()
