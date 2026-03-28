from time import strptime

def is_valid_format(time_string, format_code="%Y-%m-%d"):
    try:
        strptime(time_string, format_code)
        return True
    except ValueError:
        return False