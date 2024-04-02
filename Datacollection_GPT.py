import os
import openai
import json
from datetime import datetime
import re

# 목차 생성 프롬프트 함수
def create_prompt_with_keyword(keyword, language="Korean"):
    if language == "English":
        System_role = f"You are a professor teaching '{keyword}'. You must conduct the lecture with detailed and accurate content for as long as possible."
        prompt = f"Please create the table of contents for the textbook. It must include content related to '{keyword}', and be written in sentence form.The lecture should be conducted in English."
    else:  
        System_role = f"당신은 '{keyword}'를 가르치는 교수입니다. 학생들을 가르치기 위한 교재를 집필해야 합니다. 최대한 상세하고 많은 내용을 포함하고 있는 두꺼운 교재를 집필해야 합니다."
        prompt = f"교재의 목차를 생성해주세요. '{keyword}'와 관련된 내용을 포함해야 하며, 문장형식으로 작성해주세요. 교재 집필은 한국어로 진행되어야 합니다."
        
    return System_role, prompt

# 내용 생성 프롬프트 함수 수정본
def create_contents_with_keyword(keyword, language="Korean"):
    if language == "English":
        System_role = f"You are a professor teaching '{keyword}'. You must provide an in-depth explanation and analysis on the topic, avoiding a structured list format."
        prompt = f"Write a detailed explanation about '{keyword}', including its importance, applications, and any relevant theories or concepts. Avoid using a structured list format. The explanation should be conducted in English."
    else:
        System_role = f"당신은 '{keyword}'를 학생들에게 가르치는 교수입니다. 구조화된 목록 형식을 피하면서 주제에 대한 심층적인 설명과 분석을 제공해야 합니다."
        prompt = f"'{keyword}'에 대해 그 중요성, 응용 분야, 관련 이론이나 개념을 포함하여 상세한 설명을 작성해주세요. 구조화된 목록 형식을 사용하지 말아주세요. 설명은 한국어로 진행되어야 합니다."

    return System_role, prompt



# 세부 질문 생성 프롬프트 함수
def create_DetailQuestion_with_keyword(answer, keyword, language="Korean"):
    if language == "English":
        System_role = f"You are a professor teaching '{keyword}'. After reading the presented content, you should conduct lectures as detailed and accurate as possible on topics students are curious about, and for as long as possible."
        prompt = f"Please create a question based on the following description: '{answer}'. The question should include content related to '{keyword}' and must be formulated in sentence form. The question should be in English."
    else:  
        System_role = f"당신은 '{keyword}'를 가르치는 교수입니다. 제시되는 교재 내용을 읽고 학생들이 궁금해하거나 이해하기 힘든 내용에 대해 상세하고 아주 길게 해설지를 작성해야 합니다. "
        prompt = f"다음 설명에 대해 질문을 여러개 많이 생성해주세요:'{answer}'. 이때 '{keyword}'와 관련된 내용을 포함해야 하며, 문장형식으로 질문을 작성해주세요. 질문은 한국어로 진행되어야 합니다."
        
    return System_role, prompt

# 질문 답변 프롬프트 함수
def Qanswering(answer,keyword, language="Korean"):
    if language == "English":
        System_role = f"You are a professor teaching '{keyword}'. You need to teach your students about the question '{answer}'."
        prompt = f"Please generate a long and detailed response to the following question: '{answer}'. Include content related to {keyword} and ensure the answer is written in complete sentences and in detail."

    else:  
        System_role = f"당신은 '{keyword}'를 가르치는 교수입니다. {answer} 라는 질문에 대해 학생들에게 가르쳐야 합니다."
        prompt = f"다음 질문에 대해 답변을 길고 상세히 생성해주세요:'{answer}'. {keyword}와 관련된 내용을 포함해야 하며, 문장형식으로 길고 상세히 답변을 작성해주세요. "
        
    return System_role, prompt



# 생성된 내용에 따라 목차를 생성하는 함수
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
        # 1. 형식으로 시작하는 경우 처리
        if one_topic.strip().startswith(tuple(str(i) for i in range(10))) and ". " in one_topic:
            topic = one_topic.split(". ", 1)[1]
        # 하이픈(-)으로 시작하는 경우 처리
        elif one_topic.strip().startswith("-"):
            topic = one_topic.strip('- ').strip()
        else:
            topic = one_topic.strip()

        System_role, prompt = create_contents_with_keyword(topic)  # 사용할 프롬프트 생성
        content_text = generate_response(System_role, prompt, chatmodel,language="Korean")  # 콘텐츠 생성
        
        contents.append({"Question": topic, "Answer": content_text.strip()})
    
    return contents


# 질문을 생성하고 생성한 질문에서 답변을 만드는 함수
def generate_detail_contents(contents, chatmodel, detailcontents, language="Korean") :
        
    answer = contents["Answer"] # 목차에 따른 내용임

    System_role, prompt = create_DetailQuestion_with_keyword(answer,keyword)  # 컨텐츠에서 질문 생성 사용할 프롬프트 생성
    Q_text = generate_response(System_role, prompt, chatmodel,language="Korean")  # 프롬프트로 질문 생성


    # detailcontents = generate_contents(one_Q, chatmodel, detailcontents, language="Korean")
    pattern = r'\d+\.\s*(.*?)\s*(?=\d+\.|$)'
    questions = [match.group(1) for match in re.finditer(pattern, Q_text, re.DOTALL)]

    # 각 질문을 출력하여 확인합니다.
    # for question in questions:
        
    # 생성된 질문을 쪼개서 하나의 질문에서 하나의 답변을 얻기 """
    System_role, prompt =  Qanswering(Q_text, keyword, language)  # 사용할 프롬프트 생성
    content_text = generate_response(System_role, prompt, chatmodel,language="Korean")  # 콘텐츠 생성
    
    detailcontents.append({"Question": Q_text, "Answer": content_text.strip()})
        
    return detailcontents
    
    
if __name__ == "__main__":

    """ Config """
    OPENAI_API_KEY = ""
    os.environ["OPENAI_API_KEY"]=OPENAI_API_KEY
    
    chatmodel = "gpt-3.5-turbo-1106" # 향상된 최신 GPT-3.5 Turbo 모델. 최대 4,096개의 출력 토큰을 반환
    
    language = "english"  # Choose between "korean" and "english"

    keyword = "사출성형" if language == "Korean" else "Injection Molding"

    contents = []
    Q_contents = []
    forMakeQ = []
    
    detailcontents = []
    
    """ main """
    System_role, prompt = create_prompt_with_keyword(keyword)
    response_text = generate_response(System_role, prompt, chatmodel, language="Korean")
    
    contents = generate_contents(response_text, chatmodel, contents, language="Korean")
    
    for item in contents:
        if item['Question'].strip() :
            forMakeQ.append(item)  # 정제하는 것 " "제외시키려고
 
    
    # 디렉토리 설정
    date = datetime.now().strftime("%Y-%m-%d %H_%M_%S")
    directory_name = f"{keyword}"

    if not os.path.exists(directory_name):
        os.makedirs(directory_name)
    

    response_dict = {
        "contents": forMakeQ,   # 리스트임
        "source" : chatmodel,
        "date": date,
        "language": language
    }

    # JSON으로 직렬화
    with open(f'{directory_name}/QnA_{chatmodel}_{language}.json', 'w', encoding='utf-8') as f:
        json.dump(response_dict, f, ensure_ascii=False, indent=4)


    detail_QnA_results = []  # 모든 결과를 저장할 리스트

    for i, content in enumerate(forMakeQ):
        # 상세 질문 생성
        detailcontent = generate_detail_contents(content, chatmodel, detailcontents, language="Korean")
        
        QnAs = []  # 현재 내용에 대한 질문-답변 쌍을 저장할 리스트
        
        # 각 질문에 대해 답변 생성
        questions = detailcontent[i]["Question"].split('\n')
        
        for question in questions:
            System_role, prompt = Qanswering(question, keyword, language)
            detailans_text = generate_response(System_role, prompt, chatmodel, language="Korean")
            
            QnAs.append({"question": question, "answer": detailans_text})
        
        # 현재 내용에 대한 결과를 detail_QnA_results에 추가
        detail_Q_response_dict = {
            "contents": QnAs,
            "source": chatmodel,
            "date": date,
            "language": language
        }
        detail_QnA_results.append(detail_Q_response_dict)

        # 결과 저장
        filename = f"{directory_name}/Detail_QnA_{i+1}_{chatmodel}_{language}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(detail_Q_response_dict, f, ensure_ascii=False, indent=4)
            print(f"파일 '{filename}'에 성공적으로 저장되었습니다.")
