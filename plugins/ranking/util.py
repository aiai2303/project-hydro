import random


def get_level(exp):
    level = 0
    require_exp = 100
    while exp >= require_exp:
        exp -= require_exp
        level += 1
        if level % 2 == 0:
            require_exp *= 1.2

    remaining_exp_for_next_level = require_exp - exp
    return level, round(remaining_exp_for_next_level)


def ranks_prettier(user_rows):
    ranks = []
    emojis = ["🏆", "🏅", "🥇", "🥈", "🥉"]
    sorted_users = sorted(user_rows, key=lambda x: x[1], reverse=True)
    for i, row in enumerate(sorted_users[:20]):
        rank = f"{emojis[i]}" if i < len(emojis) else f"{i + 1}"
        user_info = [
            f"<b>{rank}) {row[0]}</b>",
            f"(Lv{row[2]})",
        ]
        ranks.append("  ".join(user_info))

    return ranks


def count_exp(m, level: int):
    exp = 1
    is_bonus = 0
    if m.text:
        exp = len(m.text)
        if exp == 4096:
            div = random.randint(1000, 9656)
            div = ((div + level) * 10) + 4096
            exp -= div
            is_bonus = exp
        elif exp > 4000:
            div = (level * 2) + 4000
            exp -= div
            is_bonus = exp
        if m.text.startswith("/share"):
            if any(scheme in m.text for scheme in ["http://", "https://"]):
                bonus = random.choice([10, level, 1000, level * 2, level * 10, level * level, level * 1000, level * level * level, level * 1000 * 1000, level * level * level * level])
                exp += exp * bonus + level
                is_bonus = bonus
    elif m.video or m.audio or m.document:
        exp += 500 + level
    elif m.photo:
        exp += 300 + level
    elif m.sticker:
        bonus = random.choice(
            [
                1,
                2,
                level,
                level * 2,
                level * 10,
                level * level,
                1000,
                10,
                6,
                1,
            ]
        )
        exp += 100 * bonus + level
        is_bonus = bonus
    if m.caption:
        exp += len(m.caption)
    return exp, is_bonus


def get_user_rank(user_rows, target_user_id):
    sorted_users = sorted(user_rows, key=lambda x: x[1], reverse=True)
    for i, (user_id, _) in enumerate(sorted_users, start=1):
        if user_id == target_user_id:
            return i
    return None


def get_title(level):
    if level < 20:
        return "Gà Mờ"
    elif level < 40:
        return "Nghiệp Dư"
    elif level < 60:
        return "Thành Thạo"
    elif level < 80:
        return "Bán Chuyên"
    elif level < 101:
        return "Chuyên Nghiệp"
    elif level < 201:
        return "Bậc Thầy"
    elif level < 301:
        return "Vô Địch"
    elif level < 401:
        return "Bất Tử"
    elif level < 501:
        return "Chiến Thần"
    else:
        return "Vĩnh Hằng"
