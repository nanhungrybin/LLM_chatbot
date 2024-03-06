import os
import openai


def create_prompt_with_keyword(keyword):
    System_role = f"당신은 '{keyword}'를 가르치는 교수입니다. 상세하고 정확한 내용으로 10시간 동안 강의를 진행해야 합니다."
    prompt = f"교재의 목차를 생성해주세요. '{keyword}'와 관련된 내용을 포함해야 하며, 문장형식으로 작성해주세요. "
    return System_role, prompt


def generate_response(System_role,prompt):
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[  {"role": "system", "content": System_role},
            {"role": "user", "content": prompt},],
        max_tokens=2048,
        temperature=0,
        
    )
    # Get the response text from the API response
    response_text = response.choices[0].message.content

    return response_text
    
    
if __name__ == "__main__":

    # 변경 가능 정보
    OPENAI_API_KEY = "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"
    os.environ["OPENAI_API_KEY"]=OPENAI_API_KEY

    keyword = "사출성형"
    System_role, prompt = create_prompt_with_keyword(keyword)
    response_text = generate_response(System_role,prompt)
    print(response_text)
