from pynput import mouse, keyboard
END = False

def on_click(x, y, button, pressed):
    if END == False:
        m = '{0}_{1}'.format(
            'Pressed' if pressed else 'Released',
            (x, y))
        print(m)
    else:
        return False

def on_release(key):
    if key == keyboard.Key.esc:
        global END
        END = True
        return False

with keyboard.Listener(on_release=on_release) as k_listener, mouse.Listener(on_click=on_click) as m_listener:
    k_listener.join()
    m_listener.join()
