import os
import json
import csv

contest_dir = "contests_details"

edges = []

# Go through each year
for year in range(2016, 2025):
    contest_path = os.path.join(contest_dir, f"contest_{year}.json")
    if not os.path.exists(contest_path):
        print(f"Contest file for {year} not found.")
        continue

    with open(contest_path, "r", encoding="utf-8") as f:
        contest_data = json.load(f)

    final_round = None
    for rnd in contest_data.get("rounds", []):
        if rnd.get("name", "").lower() == "final":
            final_round = rnd
            break

    if not final_round:
        print(f"No final round for {year}")
        continue

    if final_round.get("performances", []) == None:
        print(f"No perforamance round for {year}")
        continue

    for perf in final_round.get("performances", []):
        contestant_id = perf["contestantId"]

        # Find the public score
        for score in perf.get("scores", []):
            if score.get("name") == "public":
                votes = score.get("votes", {})
                target_code = contestant_id

                for source_code, num_votes in votes.items():
                    edges.append((source_code, target_code, num_votes))

print(f"Total public vote edges from 2016–2024 finals: {len(edges)}")

# Save to CSV
with open("eurovision_public_votes_2016_2024_finals.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["source", "target", "votes"])
    writer.writerows(edges)

print("Edge list saved to eurovision_public_votes_2016_2024_finals.csv")
