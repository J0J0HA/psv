import psv


with open("test.psv", "r") as f:
    tbl = psv.load(f)

print(tbl)
for etr in tbl.where("key and key == 'value'"):
    print(etr.uuid, etr.data)

tbl.append(psv.Entry.new({"key": "value"}))

with open("test.psv", "w") as f:
    psv.write(f, tbl)

