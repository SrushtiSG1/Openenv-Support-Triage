import requests
from app.env import CustomerSupportEnv
from app.models import Action

# 🔑 PUT YOUR HUGGING FACE TOKEN HERE
HF_TOKEN = "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"

API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-large"
HEADERS = {
    "Authorization": f"Bearer {HF_TOKEN}"
}

env = CustomerSupportEnv()


def query(prompt):
    try:
        response = requests.post(
            API_URL,
            headers=HEADERS,
            json={"inputs": prompt},
            timeout=30
        )
        return response.json()
    except Exception as e:
        print("API Error:", e)
        return None


def create_action(obs, model_output):
    text = obs.message.lower()

    # Simple mapping logic (important for scoring)
    if "refund" in text:
        return Action(
            action_type="classify",
            category="billing",
            priority="medium",
            route_to="billing_team",
            response=model_output[:50]
        )

    elif "crash" in text:
        return Action(
            action_type="classify",
            category="technical",
            priority="high",
            route_to="engineering",
            response=model_output[:50]
        )

    else:
        return Action(
            action_type="classify",
            category="multi_issue",
            priority="critical",
            route_to="priority_support",
            response=model_output[:50]
        )


def run_task(task_id):
    obs = env.reset(task_id)

    print(f"[START] Task {task_id}")

    total_score = 0

    for step in range(5):

        prompt = f"""
You are a helpful customer support agent.

Ticket: {obs.message}
Customer tier: {obs.customer_tier}

Write a short helpful response.
"""

        result = query(prompt)

        if result and isinstance(result, list):
            try:
                model_output = result[0].get("generated_text", "We will help you.")
            except:
                model_output = "We will help you."
        else:
            model_output = "We will help you."

        action = create_action(obs, model_output)

        obs, reward, done, info = env.step(action)

        print(f"[STEP] {step} | Score: {reward.score} | Info: {info}")

        total_score += reward.score

        if done:
            break

    print(f"[END] Task {task_id} | Total: {total_score}")
    return total_score


if __name__ == "__main__":
    scores = []

    for i in range(3):
        scores.append(run_task(i))

    final_score = sum(scores) / len(scores)
    print(f"FINAL SCORE: {final_score}")