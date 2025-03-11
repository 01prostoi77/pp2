import json


with open("sample-data.json") as f:
    data = json.load(f)


print("Interface Status")
print("=" * 96)
print(f"{'DN':<50} {'Description':<20} {'Speed':<8} {'MTU':<6} {'Trunklog':<4}")
print("-" * 96)


for item in data["imdata"]:
    attributes = item["l1PhysIf"]["attributes"]
    dn = attributes["dn"]
    descr = attributes["descr"] if attributes["descr"] else " "
    speed = attributes["speed"]
    mtu = attributes["mtu"]
    trunklog = "True" if attributes["trunkLog"] == "default"  else "Error"
    
    print(f"{dn:<50} {descr:<20} {speed:<8} {mtu:<6} {trunklog:<4}")
