import pysaves as psv


with open("test.psv", "r") as f:
    tbl = psv.load(f)

print(tbl)

print(len(tbl.where("key == 'value'")))
tbl.where("key == 'value'").set("key", lambda entry: "another value")

tbl.where("key == 'different value'").where("_entry['abc'] is None").set("abc", "exists")

tbl.append(psv.Entry.new({"key": "value"}))

with open("test.psv", "w") as f:
    psv.write(f, tbl)

