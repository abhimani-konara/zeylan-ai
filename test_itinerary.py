from itinerary import create_itinerary, modify_itinerary, get_itinerary, validate_itinerary

r1 = create_itinerary(["Colombo", "Sigiriya", "Kandy", "Ella"], {"interests": "wildlife", "budget_basis": "per person"})
iid = r1["itinerary_id"]
print("v1 nights:", r1["total_nights"], "| valid:", r1["validation"]["valid"])
print("v1 warnings:", r1["validation"]["warnings"])

r2 = modify_itinerary(iid, add=["Yala"], note="customer wants wildlife")
print("v2 stops:", [x["destination"] for x in r2["stops"]], "| nights:", r2["total_nights"])

r3 = modify_itinerary(iid, remove=["Colombo"], note="start from Sigiriya")
print("v3 stops:", [x["destination"] for x in r3["stops"]])
print("preferences kept:", r3["preferences"])
print("versions saved:", len(get_itinerary(iid)["versions"]))
print("bad route:", validate_itinerary([{"destination": "Atlantis", "nights": 1}])["problems"])
