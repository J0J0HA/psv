import psv


with open("test.psv", "r") as f:
    tbl = psv.load(f)

print(tbl)

tbl.where("_entry['abc']").where("_entry['xyz']").others()["xyz"] = "ananas"
print(tbl.where("_entry['abc']").where("_entry['xyz']").others())

tbl.append(psv.Entry.new({"key": "value"}))

for etr in tbl:
    print(etr.uuid, etr.data)

print(tbl)


with open("test.psv", "w") as f:
    psv.write(f, tbl)
    f.flush()
    f.close()
psv.share_table(tbl, "localhost", autosave="test.psv")
