def validate_row(row):
    if not row.get("upc"):
        return False
    if not isinstance(row.get("regular_price"), (int, float)):
        return False
    return True