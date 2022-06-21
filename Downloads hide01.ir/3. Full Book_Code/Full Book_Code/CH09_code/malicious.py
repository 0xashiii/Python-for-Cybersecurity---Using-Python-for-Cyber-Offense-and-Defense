import os
print("Malicious file executed")
with open("out.txt","w") as f:
    f.write("Executed")