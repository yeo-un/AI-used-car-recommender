import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_reasons_batch(cars: list, preferences: dict) -> dict:
    cars_info = []
    for car in cars:
        cars_info.append(
            {
                "id": car.get("id"),
                "model": car.get("model"),
                "price": car.get("price"),
                "year": car.get("year"),
                "mileage": car.get("mileage"),
                "options": car.get("options"),
                "score": car.get("score"),
            }
        )

    prompt = f"""
            사용자의 선호 조건에 맞춰 각 차량에 대한 추천 이유를 작성하세요.

            사용자 조건:
            - 최소 연식: {preferences.get("min_year")}
            - 선호 옵션: {preferences.get("preferred_options")}

            차량 목록:
            {json.dumps(cars_info, ensure_ascii=False)}

            각 차량 id를 key로 하고,
            값은 3문장 이내 추천 이유인 JSON만 반환하세요.
            """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
        response_format={"type": "json_object"},
    )

    content = response.choices[0].message.content

    try:
        return json.loads(content)
    except Exception as e:
        print("JSON 파싱 실패:", content)
        return {}
