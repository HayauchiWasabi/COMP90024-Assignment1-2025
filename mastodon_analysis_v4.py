import json
from datetime import datetime
from collections import defaultdict
from mpi4py import MPI

def process_line(line, hour_scores, user_scores):
    try:
        post = json.loads(line).get("doc", {})
        created_at = post.get("createdAt")
        sentiment = post.get("sentiment")
        user = post.get("account", {})
        user_id, username = user.get("id"), user.get("username")

        if sentiment is None or not created_at or user_id is None:
            return

        dt = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%S.%fZ")
        hour_key = dt.strftime("%Y-%m-%d %H:00")
        hour_scores[hour_key] += sentiment

        if user_id not in user_scores:
            user_scores[user_id] = {"score": 0, "username": username}
        user_scores[user_id]["score"] += sentiment

    except Exception:
        pass

def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    import sys
    if len(sys.argv) < 2:
        if rank == 0:
            print("Usage: python mastodon_analysis.py <file_path>")
        return
    file_path = sys.argv[1]

    hour_scores = defaultdict(float)
    user_scores = {}

    with open(file_path, encoding="utf-8") as f:
        for i, line in enumerate(f):
            if i % size == rank:
                process_line(line, hour_scores, user_scores)

    # each rank writes its own partial result
    with open(f"partial_result_rank{rank}.json", "w") as out:
        json.dump({"hour": hour_scores, "user": user_scores}, out)

    if rank == 0:
        print(f"[Rank {rank}] distributed processing completed")
    else:
        print(f"[Rank {rank}] writing partial result completed")

if __name__ == "__main__":
    main()
