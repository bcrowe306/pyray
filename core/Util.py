def lerp(value, i_min, i_max, o_min, o_max) -> float | int:
    """
    Linear interpolation function.
    """
    return (value - i_min) / (i_max - i_min) * (o_max - o_min) + o_min
