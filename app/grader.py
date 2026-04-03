def grade_step(task, state, action):
    expected = task["expected"]

    score = 0.0
    breakdown = {}

    if action.category:
        if action.category == expected["category"]:
            score += 0.3
            breakdown["category"] = 0.3

    if action.priority:
        if action.priority == expected["priority"]:
            score += 0.2
            breakdown["priority"] = 0.2

    if action.route_to:
        if action.route_to == expected["route_to"]:
            score += 0.3
            breakdown["route"] = 0.3

    if action.response:
        score += 0.2
        breakdown["response"] = 0.2

    return score, breakdown