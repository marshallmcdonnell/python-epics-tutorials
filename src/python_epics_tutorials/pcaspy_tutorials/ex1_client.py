from epics import caget, caput, cainfo

caput("MTEST:RAND", 0)
cainfo("MTEST:RAND")

caput("MTEST:RAND", -1.23)
cainfo("MTEST:RAND")

out = caget("MTEST:RAND")
print("CAGET output:", out)



