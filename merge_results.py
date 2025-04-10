import json
import glob
from collections import defaultdict

def load_partial_results():
    hour_scores = defaultdict(float)
    user_scores = {}

    for file in glob.glob("partial_result_rank*.json"):
        with open(file, "r") as f:
            data = json.load(f)
            for hour, score in data.get("hour", {}).items():
                hour_scores[hour] += score
            for uid, info in data.get("user", {}).items():
                if uid not in user_scores:
                    user_scores[uid] = {"score": 0, "username": info["username"]}
                user_scores[uid]["score"] += info["score"]

    return hour_scores, user_scores

def display_top(title, data, key_func, top_n=5, is_user=False, is_hour=False):
    sorted_items = sorted(data.items(), key=key_func)
    print(f"\n{title} (Top {top_n}):")
    for i, (k, v) in enumerate(sorted_items[:top_n], 1):
        if is_user:
            print(f"{i}. ID: {k}, Username: {v['username']}, Score: {v['score']:.6f}")
        elif is_hour:
            print(f"{i}. {k} — Score: {v:.6f}")
        else:
            print(f"{i}. {k}: {v}")

def main():
    hour_scores, user_scores = load_partial_results()

    display_top("Happiest Hours", hour_scores, key_func=lambda x: -x[1], is_hour=True)
    display_top("Saddest Hours", hour_scores, key_func=lambda x: x[1], is_hour=True)

    display_top("Happiest Users", user_scores, key_func=lambda x: -x[1]["score"], is_user=True)
    display_top("Saddest Users", user_scores, key_func=lambda x: x[1]["score"], is_user=True)

if __name__ == "__main__":
    main()
