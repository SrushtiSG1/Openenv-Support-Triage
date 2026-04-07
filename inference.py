import os
from openai import OpenAI
from app.env import CustomerSupportEnv
from app.models import Action

client = OpenAI(
    api_key=os.environ["API_KEY"],
    base_url=os.environ["API_BASE_URL"]
)

MODEL = os.environ.get("MODEL_NAME", "gpt-4o-mini")

env = CustomerSupportEnv()


def run_task(task_id):
    obs = env.reset(task_id)

    print(f"[START] Task {task_id}")
    total_score = 0

    for step in range(5):

        prompt = f"""
You are a support agent.

Ticket: {obs.message}
Customer tier: {obs.customer_tier}
"""

        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}]
        )

        text = response.choices[0].message.content

        action = Action(
            action_type="classify",
            category="billing" if "refund" in obs.message.lower() else "technical",
            priority="high",
            route_to="engineering",
            response=text[:50]
        )

        obs, reward, done, info = env.step(action)

        print(f"[STEP] {step} | Score: {reward.score}")

        total_score += reward.score

        if done:
            break

    print(f"[END] Task {task_id} | Total: {total_score}")
    return total_score


if __name__ == "__main__":
    scores = []
    for i in range(3):
        scores.append(run_task(i))

    print("FINAL SCORE:", sum(scores)/len(scores))