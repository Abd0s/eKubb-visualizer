"""Configuration for simulation parameters

"""

# Debug enable
debug: bool = True
# Game elements
block_count: int = 5
stick_height: float = 2.5
stick_radius: float = 0.4
# Playing field
playing_field_padding: float = 10.0
playing_field_size: tuple[float, float] = (80.0, 50.0)
calibration_point_a: tuple[float, float, float] = (-60.0, 0.0, stick_height / 2)
calibration_point_b: tuple[float, float, float] = (60.0, 0.0, stick_height / 2)
# TCP connection
TCP_IP: str = "localhost"
TCP_PORT: int = 51001
