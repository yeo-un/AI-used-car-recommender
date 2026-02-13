from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_reason(car):
    prompt = f"""
    다음 차량을 사용자에게 추천하는 이유를 설명해라.

    모델: {car["model"]}
    가격: {car["price"]}만원
    연식: {car["year"]}
    주행거리: {car["mileage"]}km
    점수: {car["score"]}점 (100점 만점)

    점수를 기준으로 합리적으로 설명해라.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
    )

    return response.choices[0].message.content
