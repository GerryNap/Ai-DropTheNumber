COLORS = {0: (204, 192, 179),
          1: (204, 192, 179),
          2: (238, 228, 218),
          4: (237, 224, 200),
          8: (242, 177, 121),
          16: (245, 149, 99),
          32: (246, 124, 95),
          64: (246, 94, 59),
          128: (237, 207, 114),
          256: (237, 204, 97),
          512: (237, 200, 80),
          1024: (237, 197, 63),
          2048: (237, 194, 46),
          'light': (249, 246, 242),
          'dark': (119, 110, 101),
          'other': (0, 0, 0),
          'bg': (187, 173, 160)}

class Color:
    def get(index):
        return COLORS[index]