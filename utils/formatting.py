def format_large_number(value):
    if value is None:
        return "N/A"

    abs_value = abs(value)

    if abs_value >= 1e12:
        return f"{value / 1e12:.2f}T"
    if abs_value >= 1e9:
        return f"{value / 1e9:.2f}B"
    if abs_value >= 1e6:
        return f"{value / 1e6:.2f}M"
    if abs_value >= 1e3:
        return f"{value / 1e3:.2f}K"

    return f"{value:.2f}"
