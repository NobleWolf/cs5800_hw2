def round(x):
    frac,whole = math.modf(x)
    if frac < 0.5:
        return whole
    else:
        return whole+1