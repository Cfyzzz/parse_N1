def strim_all(line):
    """Функция вырезает лишние пробелы и запятые"""
    _line = line.replace(",", "").replace(" -", "-").replace("- ", "-").strim()
    return _line



