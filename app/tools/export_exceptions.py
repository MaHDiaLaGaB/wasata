import json

import cus_exceptions

exception_list = list(cus_exceptions.registry.KNOWN_EXCEPTIONS.values())

exception_list.sort(key=lambda e: e.error_code())

exception_json = {}

for exc in exception_list:
    class_name = exc.__name__
    error_code = exc.error_code()
    category_name = cus_exceptions.const.ExceptionCategory(exc.category_code).name
    description = exc.description
    print(f"{error_code}, {category_name}, {class_name}, {description}")
    exception_json[error_code] = {
        "error_code": error_code,
        "class_name": class_name,
        "category_name": category_name,
        "description": description,
    }

with open("exceptions.json", "w") as f:  # pylint: disable=W1514
    json.dump(exception_json, f, indent=4)
