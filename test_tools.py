from tools import search_packages, get_package_price

print("Short trips (max 7 days):")
for p in search_packages(max_days=7):
    print(" ", p["id"], p["name"], p["duration_days"], "days")

print("Keyword 'trek':", [p["name"] for p in search_packages(keyword="trek")])
print("Price for package 3:", get_package_price(3)["status"])
print("Price for package 5:", get_package_price(5)["status"])
