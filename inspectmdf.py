from asammdf import MDF

mdf = MDF("input.mf4")
for name in mdf.channels_db:
    if name.startswith("BMC"):
        print(name)