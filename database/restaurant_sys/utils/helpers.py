""" some useful functions """

def convert_to_string_format(data):
    if not data:
        return ""

    menu_string = ""
    for item in data:
        menu_string += "{"
        for field, value in item.items():
            # "cost_price" -> "Cost Price"
            formatted_field = field.replace('_', ' ').capitalize()
            menu_string += f"{formatted_field}: {value}, "
        menu_string += "}\n"
    return menu_string
