# helper method for type conversions
def is_number(n):
    try:
        # Type-casting the string to `float`. If string is not a valid `float`, 
        float(n)
    # it will raise `ValueError` exception
    except ValueError: return False
    except Exception: return False
    return True