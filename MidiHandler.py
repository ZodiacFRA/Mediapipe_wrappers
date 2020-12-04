import pygame.midi


class MidiHandler(object):
    def __init__(s):
        pygame.midi.init()

        device_idx = 2
        s.initialized = True
        try:
            print(f'{device_idx}:', pygame.midi.get_device_info(device_idx))
            s.output = pygame.midi.Output(device_idx)
        except pygame.midi.MidiException:
            print('[-] - Cound not connect to midi device')
            s.initialized = False

    def close_midi(s):
        if not s.initialized:
            return
        for note in range(0, 127):
            s.output.write_short(0x80, note, 0)
        s.output.close()

    def send(s, note, velo):
        if not s.initialized:
            return
        # Ox90 = note on
        # Ox80 = note off
        # print("sending", note, velo)
        # s.output.write_short(0x90, note, velo)
        midi_time = pygame.midi.time()
        s.output.write([[[0x90, note, velo], midi_time]])
        # s.output.write([[[0x90, note + 3, velo], midi_time]])
        # s.output.write([[[0x90, note + 7, velo], midi_time]])
        # s.output.write([[[0x90, note - 12, velo], midi_time]])
        # s.output.write_short(0x90, note, velo)



if __name__ == '__main__':
    midi_handler = MidiHandler()
