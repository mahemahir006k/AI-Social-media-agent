from post_context import build_post_context


result = build_post_context()


print("\n================================")
print("TOPIC")
print("================================")

print(result["topic"])


print("\n================================")
print("NEWS")
print("================================")

print(result["article"]["title"])
print(result["article"]["source"])
print(result["article"]["published"])
print(result["article"]["url"])


print("\n================================")
print("XEN HRA KNOWLEDGE")
print("================================")

print(result["company_knowledge"])