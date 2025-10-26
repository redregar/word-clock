from PIL import Image
import time
from clock_display_hal import ClockDisplayHAL


def update_led_pixels(gif_pixels, new_size, clock_display_hal, background_color=(0, 0, 0)):
    """Setzt alle Pixel des Frames auf der Wortuhr."""
    for y in range(new_size[1]):
        for x in range(new_size[0]):
            pixel = gif_pixels[x, y]
            if len(pixel) == 4:
                r, g, b, a = pixel
                color = (r, g, b) if a > 0 else background_color
            else:
                r, g, b = pixel[:3]
                color = (r, g, b)
            clock_display_hal.set_pixel(x, y, color)


def display_gif(
    gif_path,
    clock_display_hal,
    display_gif_duration=4,
    background_color=(0, 0, 0)
):
    """Zeigt ein GIF auf der Wortuhr an, berücksichtigt Frametiming und Transparenz."""
    img = Image.open(gif_path)
    new_size = (ClockDisplayHAL.WIDTH, ClockDisplayHAL.HEIGHT)
    start_time = time.time()

    while time.time() < start_time + display_gif_duration:
        try:
            frame = img.convert("RGBA").resize(new_size, resample=Image.NEAREST)
            gif_pixels = frame.load()
            update_led_pixels(gif_pixels, new_size, clock_display_hal, background_color)
            clock_display_hal.show()

            # GIF-spezifisches Framedelay
            delay_ms = img.info.get('duration', 100)  # Default 100 ms
            time.sleep(delay_ms / 1000)

            # Nächstes Frame
            img.seek(img.tell() + 1)

        except EOFError:
            # Zurück zum ersten Frame
            img.seek(0)
