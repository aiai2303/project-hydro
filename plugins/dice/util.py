def prettier(user_rows):
    ranks = []
    emojis = ["🎲", "🍀", "☘️"]
    sorted_users = sorted(user_rows, key=lambda x: x[1], reverse=True)

    for i, row in enumerate(sorted_users[:10]):
        rank = f"{emojis[i]}" if i < len(emojis) else f"{i + 1}"
        user_info = [
            f"<b>{rank}) {row[0]}</b>",
            f"(`{row[1]}`)",
        ]
        ranks.append("  ".join(user_info))

    return ranks
