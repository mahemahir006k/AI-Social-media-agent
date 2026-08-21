import json
import sys

filename = sys.argv[1] if len(sys.argv) > 1 else "myflow.json"

with open(filename, "r", encoding="utf-8") as f:
    data = json.load(f)

fixed = False
for node in data.get("nodes", []):
    name = node.get("data", {}).get("name", "")
    label = node.get("data", {}).get("label", "")
    
    if name == "requestsPost" and label == "Preview Post":
        inputs = node["data"].get("inputs", {})
        old_body = inputs.get("requestPostBody", "")
        if old_body:
            inputs["requestPostBody"] = ""
            fixed = True
            print(f"Fixed '{label}' node (id: {node['id']})")
            print(f"   Removed body content: {old_body[:60]}...")

outname = filename.replace(".json", "_FIXED.json")
with open(outname, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

if fixed:
    print(f"\nDone! Import this file into Flowise: {outname}")
else:
    print(f"\nNo fix needed. File saved as: {outname}")