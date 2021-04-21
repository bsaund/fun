

leverage_factor = .5


principle = 100

uptick = .025
downtick = .024399


final = principle * (1 + uptick * leverage_factor) * (1 - downtick * leverage_factor)

print(final)
