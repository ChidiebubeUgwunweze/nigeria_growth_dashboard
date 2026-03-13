from dash import ctx

# This function returns a dictionary containing the centers of each state in Nigera
def state_centers():
    state_centers = { "Abia": {"lat": 5.45, "lon": 7.52},
                      "Adamawa": {"lat": 9.33, "lon": 12.45},
                      "Akwa Ibom": {"lat": 5.00, "lon": 7.85},
                      "Anambra": {"lat": 6.20, "lon": 7.00},
                      "Bauchi": {"lat": 10.30, "lon": 9.84},
                      "Bayelsa": {"lat": 4.75, "lon": 6.05},
                      "Benue": {"lat": 7.33, "lon": 8.75},
                      "Borno": {"lat": 11.83, "lon": 13.15},
                      "Cross River": {"lat": 5.75, "lon": 8.30},
                      "Delta": {"lat": 5.50, "lon": 5.75},
                      "Ebonyi": {"lat": 6.25, "lon": 8.05},
                      "Edo": {"lat": 6.30, "lon": 5.60},
                      "Ekiti": {"lat": 7.63, "lon": 5.22},
                      "Enugu": {"lat": 6.50, "lon": 7.50},
                      "FCT": {"lat": 8.85, "lon": 7.15},
                      "Gombe": {"lat": 10.28, "lon": 11.17},
                      "Imo": {"lat": 5.50, "lon": 7.03},
                      "Jigawa": {"lat": 12.56, "lon": 9.50},
                      "Kaduna": {"lat": 10.52, "lon": 7.70},
                      "Kano": {"lat": 12.00, "lon": 8.52},
                      "Katsina": {"lat": 12.98, "lon": 7.60},
                      "Kebbi": {"lat": 11.50, "lon": 4.00},
                      "Kogi": {"lat": 7.50, "lon": 6.73},
                      "Kwara": {"lat": 8.50, "lon": 4.90},
                      "Lagos": {"lat": 6.50, "lon": 3.35},
                      "Nasarawa": {"lat": 8.50, "lon": 7.70},
                      "Niger": {"lat": 9.60, "lon": 6.50},
                      "Ogun": {"lat": 7.00, "lon": 3.35},
                      "Ondo": {"lat": 7.25, "lon": 5.20},
                      "Osun": {"lat": 7.50, "lon": 4.50},
                      "Oyo": {"lat": 8.00, "lon": 3.50},
                      "Plateau": {"lat": 9.23, "lon": 9.50},
                      "Rivers": {"lat": 4.75, "lon": 7.00},
                      "Sokoto": {"lat": 13.06, "lon": 5.24},
                      "Taraba": {"lat": 8.00, "lon": 10.50},
                      "Yobe": {"lat": 12.00, "lon": 11.50},
                      "Zamfara": {"lat": 12.17, "lon": 6.66} }
    return state_centers
 


def update_value(plus_clicks, minus_clicks, current_values):

    triggered = ctx.triggered_id   # e.g. {"type": "plus", "index": 1}

    if triggered is None:
        return current_values

    idx = triggered["index"] - 1   # convert to list position

    new_values = current_values.copy()

    if triggered["type"] == "plus":
        new_values[idx] += 1
    elif triggered["type"] == "minus":
        new_values[idx] -= 1

    return new_values


# Formatting average apperance in column chart
def human_format(num):
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    # add more suffixes if you need Quadrillion, etc.
    return '{:.3f}{}'.format(num, ['', 'K', 'M', 'B', 'T','Q'][magnitude])