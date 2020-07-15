from __future__ import print_function

# ips = []
# ips2 = []
# with open("D:\/flask\/test.txt") as f:
#     for line in f:
#         ips.append(line.split()[0])
#         ips2.append(line.split()[1])
#         data = zip(ips, ips2)
#
# print(dict(data))

ips = []

with open ("D:\/flask\/test.txt") as port:
    lines = port.readlines()
    scanport = [line.strip().split(" ")[1] for line in lines]
print(scanport)



