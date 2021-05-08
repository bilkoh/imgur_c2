def generate_tag_name(utc_date):
    d = utc_date
    (year, month, day) = (d.year, d.month, d.day)
    tag = ""

    for i in range(16):
        year = ((year ^ 8 * year) >> 11) ^ ((year & 0xFFFFFFF0) << 17)
        month = ((month ^ 4 * month) >> 25) ^ 16 * (month & 0xFFFFFFF8)
        day = ((day ^ (day << 13)) >> 19) ^ ((day & 0xFFFFFFFE) << 12)
        tag += chr(((year ^ month ^ day) % 25) + 97)

    return tag
