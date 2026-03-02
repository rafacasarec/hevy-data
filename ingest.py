import os
import json
import requests
from datetime import datetime, timezone

API_KEY = os.environ["HEVY_API_KEY"]
BASE_URL = "https://api.hevyapp.com/v1"
HEADERS = {"api-key": API_KEY}


def get_all_workouts():
    workouts = []
    page = 1
    while True:
        response = requests.get(
            f"{BASE_URL}/workouts",
            headers=HEADERS,
            params={"page": page, "pageSize": 10}
        )
        response.raise_for_status()
        data = response.json()
        batch = data.get("workouts", [])
        if not batch:
            break
        workouts.extend(batch)
        print(f"  Página {page}: {len(batch)} workouts")
        if len(batch) < 10:
            break
        page += 1
    return workouts


def get_workout_count():
    response = requests.get(f"{BASE_URL}/workouts/count", headers=HEADERS)
    response.raise_for_status()
    return response.json()


def main():
    print("Iniciando ingesta de Hevy...")
    count = get_workout_count()
    workouts = get_all_workouts()

    output = {
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "workout_count": count,
        "workouts": workouts
    }

    os.makedirs("data", exist_ok=True)
    with open("data/workouts.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"✅ {len(workouts)} workouts guardados en data/workouts.json")


if __name__ == "__main__":
    main()
