import json
with open("sample-data.json") as f:
    text = f.read()

data = json.loads(text)

print("Interface Status")
print("="*80)
print(f"{'DN':50} {'Description':20} {'Speed':8} {'MTU':5}")
print("-"*80)

for item in data["imdata"]:
    a = item["l1PhysIf"]["attributes"]
    print(f"{a['dn']:50} {a['descr']:20} {a['speed']:8} {a['mtu']}")