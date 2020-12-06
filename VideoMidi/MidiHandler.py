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
        s.playing_keys = []

    def close_midi(s):
        if not s.initialized:
            return
        for key in range(0, 127):
            s.output.write_short(0x80, key, 127)
        s.output.close()
        pygame.midi.quit()

    def send(s, key, velo, delta=0, stop_previous=True):
        """ Ox90 = key on, Ox80 = key off, timestamp: 1000 = 1sec"""
        if not s.initialized:
            print('[-] - Cound not connect to midi device')
            return
        if stop_previous and s.playing_keys:
            for tmp in s.playing_keys:
                s.output.write_short(0x80, tmp, 127)
            s.playing_keys.clear()

        midi_time = pygame.midi.time()
        s.playing_keys.append(key)
        s.output.write([[[0x90, key, velo], midi_time + delta]])


if __name__ == '__main__':
    midi_handler = MidiHandler()
