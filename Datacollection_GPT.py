import os
import openai
import json
from datetime import datetime


# 목차 생성 프롬프트 함수
def create_prompt_with_keyword(keyword, language="Korean"):
    if language == "English":
        System_role = f"You are a professor teaching '{keyword}'. You must conduct the lecture with detailed and accurate content for as long as possible."
        prompt = f"Please create the table of contents for the textbook. It must include content related to '{keyword}', and be written in sentence form.The lecture should be conducted in English."
    else:  
        System_role = f"당신은 '{keyword}'를 가르치는 교수입니다. 상세하고 정확한 내용으로 최대한 오랜 시간 동안 강의를 진행해야 합니다."
        prompt = f"교재의 목차를 생성해주세요. '{keyword}'와 관련된 내용을 포함해야 하며, 문장형식으로 작성해주세요. 강의는 한국어로 진행되어야 합니다."
        
    return System_role, prompt

# 내용을 생성 프롬프트 함수
def create_contents_with_keyword(keyword, language="Korean"):
    if language == "English":
        System_role = f"You are a professor teaching '{keyword}'. You must conduct the lecture with detailed and accurate content for as long as possible."
        prompt = f"Please create content for the textbook. It must include content related to '{keyword}', and be written in sentence form.The lecture should be conducted in English."
    else:
        System_role = f"당신은 '{keyword}'를 가르치는 교수입니다. 상세하고 정확한 내용으로 최대한 오랜 시간 동안 강의를 진행해야 합니다."
        prompt = f"교재의 내용을 생성해주세요. '{keyword}'와 관련된 내용을 포함해야 하며, 문장형식으로 작성해주세요. 강의는 한국어로 진행되어야 합니다."
        
    return System_role, prompt

# 생성된 목차에 따라 내용을 생성하는 함수
def generate_response(System_role, prompt, chatmodel, language="Korean"):
    
    response = openai.chat.completions.create(
        model= chatmodel ,
        messages=[  {"role": "system", "content": System_role}, # 답변
            {"role": "user", "content": prompt},] # 질문
        #max_tokens=2048
        ,temperature=0
        
    )
    # Get the response text from the API response
    response_text = response.choices[0].message.content

    return response_text


# 생성한 목차를 하나씩 읽어서 내용을 A4용지 2장 이내로 생성하는 코드
def generate_contents(response_text, chatmodel, contents, language="Korean"):
     
    topics = response_text.split("\n")

    for one_topic in topics:
        topic = one_topic.split(". ")[1]
        System_role, prompt = create_contents_with_keyword(topic)  # 사용할 프롬프트 생성
        content_text = generate_response(System_role, prompt, chatmodel,language="Korean")  # 콘텐츠 생성
        contents.append({"Question": topic, "Answer": content_text.strip()})
    
    return contents



    
    
if __name__ == "__main__":

    """ Config """
    OPENAI_API_KEY = "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"
    os.environ["OPENAI_API_KEY"]=OPENAI_API_KEY
    
    chatmodel = "gpt-3.5-turbo"
    
    language = "Korean"  # Choose between "korean" and "english"

    keyword = "사출성형" if language == "Korean" else "Injection Molding"

    contents = []
    
    """ main """
    System_role, prompt = create_prompt_with_keyword(keyword)
    response_text = generate_response(System_role, prompt, chatmodel, language="Korean")
    contents = generate_contents(response_text, chatmodel, contents, language="Korean")
    
    
    """ 생성 데이터 정리 """
    # 질문, 답변, 생성 시간, 사용한 모델 소스, 사용한 언어를 받는 딕셔너리
    response_dict = {
        "contents": contents,
        "source" : chatmodel,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "language": "English" if language == "English" else "Korean"
    }
    
    # JSON으로 직렬화
    with open(f'QnA_contents_{language}.json', 'w', encoding='utf-8') as f:
        json.dump(response_dict, f, ensure_ascii=False, indent=4)
    
    print(response_dict)
    print("JSON file has been created.")
