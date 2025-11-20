import random
from datetime import datetime
from gif import display_gif

class WordClock:
    # 3x5 Font Definitionen (1 = Pixel An, 0 = Pixel Aus)
    FONT = {
        '0': [[1, 1, 1], [1, 0, 1], [1, 0, 1], [1, 0, 1], [1, 1, 1]],
        '1': [[0, 1, 0], [0, 1, 0], [0, 1, 0], [0, 1, 0], [0, 1, 0]],
        '2': [[1, 1, 1], [0, 0, 1], [1, 1, 1], [1, 0, 0], [1, 1, 1]],
        '3': [[1, 1, 1], [0, 0, 1], [1, 1, 1], [0, 0, 1], [1, 1, 1]],
        '4': [[1, 0, 1], [1, 0, 1], [1, 1, 1], [0, 0, 1], [0, 0, 1]],
        '5': [[1, 1, 1], [1, 0, 0], [1, 1, 1], [0, 0, 1], [1, 1, 1]],
        '6': [[1, 1, 1], [1, 0, 0], [1, 1, 1], [1, 0, 1], [1, 1, 1]],
        '7': [[1, 1, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1]],
        '8': [[1, 1, 1], [1, 0, 1], [1, 1, 1], [1, 0, 1], [1, 1, 1]],
        '9': [[1, 1, 1], [1, 0, 1], [1, 1, 1], [0, 0, 1], [1, 1, 1]],
        ':': [[0], [1], [0], [1], [0]] # Doppelpunkt
    }

    COLORS = [
        (255, 0, 0),    # Rot
        (0, 255, 0),    # Grün
        (0, 0, 255),    # Blau
        (255, 255, 0),  # Gelb
        (255, 0, 255),  # Magenta
        (0, 255, 255),  # Cyan
        (255, 255, 255),# Weiß
        (255, 140, 0),  # Orange
    ]

    def __init__(self, clock_display_hal, gif_path):
        self.last_hour = -1
        self.last_minute = -1
        self.clock_display_hal = clock_display_hal
        self.gif_path = gif_path
        self.current_color = (255, 255, 255)

    def get_random_color(self):
        return random.choice(WordClock.COLORS)

    def draw_character(self, start_x, start_y, char_key, color):
        """Zeichnet ein Zeichen aus der FONT Definition."""
        if char_key not in self.FONT:
            return
            
        char_matrix = self.FONT[char_key]
        height = len(char_matrix)
        width = len(char_matrix[0])

        for y in range(height):
            for x in range(width):
                if char_matrix[y][x] == 1:
                    # KORREKTUR FÜR SPIEGELUNG:
                    # Breite ist 17 (Index 0 bis 16). 
                    # Wir invertieren die X-Achse: 16 - berechnete Position.
                    original_x = start_x + x
                    mirrored_x = 16 - original_x
                    
                    self.clock_display_hal.set_pixel(mirrored_x, start_y + y, color)

    def display_time(self):
        now = datetime.now()
        hour = now.hour
        minute = now.minute

        # Trigger GIF beim Start einer neuen Stunde
        if hour != self.last_hour and self.last_hour != -1 and self.gif_path:
            if minute == 0:
                display_gif(self.gif_path, self.clock_display_hal)
                self.clock_display_hal.clear_pixels(show=False)
                self.last_hour = hour

        # Update nur wenn sich die Minute ändert (oder beim ersten Start)
        if minute != self.last_minute:
            self.clock_display_hal.clear_pixels(show=False)
            
            # Neue Zufallsfarbe für diese Minute wählen
            self.current_color = self.get_random_color()
            
            time_str = f"{hour:02d}:{minute:02d}"
            
            # Layout Berechnung für 17x17 Grid
            # Font Höhe ist 5. Vertikale Mitte ist 6 (da (17-5)/2 = 6).
            start_y = 6
            
            # Zeichne Stunde Zehner (start bei x=0)
            self.draw_character(0, start_y, time_str[0], self.current_color)
            # Zeichne Stunde Einer (start bei x=4)
            self.draw_character(4, start_y, time_str[1], self.current_color)
            # Zeichne Doppelpunkt (start bei x=8)
            self.draw_character(8, start_y, ":", self.current_color)
            # Zeichne Minute Zehner (start bei x=10)
            self.draw_character(10, start_y, time_str[3], self.current_color)
            # Zeichne Minute Einer (start bei x=14)
            self.draw_character(14, start_y, time_str[4], self.current_color)

            self.clock_display_hal.show()
            self.last_minute = minute
            self.last_hour = hour