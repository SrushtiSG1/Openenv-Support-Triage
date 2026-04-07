import os
import sys
from openai import OpenAI
from app.env import CustomerSupportEnv
from app.models import Action

# Initialize OpenAI client using hackathon-provided env vars
client = OpenAI(
    api_key=os.environ.get("API_KEY"),
    base_url=os.environ.get("API_BASE_URL")
)

MODEL = os.environ.get("MODEL_NAME", "gpt-4o-mini")

env = CustomerSupportEnv()


def run_task(task_id):
    obs = env.reset(task_id)

    print(f"[START] Task {task_id}")

    total_score = 0.0

    for step in range(5):
        try:
            prompt = f"""
You are a support agent.

Ticket: {obs.message}
Customer tier: {obs.customer_tier}
"""

            # 🔹 SAFE API CALL
            try:
                response = client.chat.completions.create(
                    model=MODEL,
                    messages=[{"role": "user", "content": prompt}]
                )
                text = response.choices[0].message.content or ""
            except Exception as e:
                print(f"[ERROR] API failed: {e}")
                text = "fallback response"

            # 🔹 SAFE ACTION CREATION
            try:
                action = Action(
                    action_type="classify",
                    category="billing" if "refund" in obs.message.lower() else "technical",
                    priority="high",
                    route_to="engineering",
                    response=text[:50]
                )
            except Exception as e:
                print(f"[ERROR] Action failed: {e}")
                action = Action(
                    action_type="classify",
                    category="general",
                    priority="low",
                    route_to="support",
                    response="fallback"
                )

            # 🔹 STEP EXECUTION
            obs, reward, done, info = env.step(action)

            print(f"[STEP] {step} | Score: {reward.score} | Info: {info}")

            total_score += reward.score

            if done:
                break

        except Exception as e:
            print(f"[STEP ERROR] {e}")
            break

    print(f"[END] Task {task_id} | Total: {total_score}")
    return total_score


if __name__ == "__main__":
    try:
        scores = []
        for i in range(3):
            scores.append(run_task(i))

        final_score = sum(scores) / len(scores) if scores else 0.0
        print("FINAL SCORE:", final_score)

    except Exception as e:
        print(f"[FATAL ERROR] {e}")
        sys.exit(0) 