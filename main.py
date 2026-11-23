from pathlib import Path
import pandas as pd

data_folder = Path("data/raw/football_data_csv")

csv_files = sorted(data_folder.glob("EPL_*.csv"))
all_data = []

for file in csv_files:
    df = pd.read_csv(file)

    parts = file.stem.split("_", 2)
    df["season"] = int(parts[1])
    df["team"] = parts[2]
    all_data.append(df)
combined = pd.concat(all_data, ignore_index=True)

print("CSV files loaded", len(csv_files))
print("Total match records", len(combined))
print("toal columns:", len(combined.columns))
print(combined[["season","team","date","scored","missed","xG","xGA"]].head())



print("\nMissing values in important columns:")

important_columns = ["date", "h_a", "scored", "missed","xG", "xGA", "result", "team", "season"]
print(combined[important_columns].isnull().sum())


print("\nDuplicate team-match records:")

duplicate_count = combined.duplicated(
    subset=["season", "team", "date"],
    keep=False
).sum()

print("Records involved in duplicates:", duplicate_count)

duplicates = combined[
    combined.duplicated(
        subset=["season", "team", "date"],
        keep=False
    )
]

print(duplicates[["season", "team", "date"]].head(10))


print("\nRecords per season:")

season_counts = combined.groupby("season").size()

print(season_counts)


print("\nFiltering dataset to the seasons 2014-2021")
combined = combined[(combined["season"] >= 2014) & (combined["season"] <= 2021)].copy()
print("Records after filtering:", len(combined))
print("\nRecords per season after filtering:")
print(combined.groupby("season").size())

print("\nHome and away records per season:")

home_away_counts = combined.groupby(["season", "h_a"]).size().unstack(fill_value=0)

print(home_away_counts)


print("\nTeams per season:")

teams_per_season = combined.groupby("season")["team"].nunique()
print(teams_per_season)

print("\nTeams without exacly 38 games:")
team_match_counts = combined.groupby(["season", "team"]).size()
print(team_match_counts[team_match_counts != 38])


print("\nSort by team and date")
combined["date"] = pd.to_datetime(combined["date"])
combined = combined.sort_values(by=["season", "team", "date"]).reset_index(drop=True)

print(combined[["season","team","date","scored","xG"]].head(10))

