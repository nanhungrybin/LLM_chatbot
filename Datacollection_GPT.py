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


# 세부 질문 생성 프롬프트 함수
def create_DetailQuestion_with_keyword(answer,keyword, language="Korean"):
    if language == "English":
        System_role = f"You are a professor teaching '{keyword}'. After reading the presented content, you should conduct lectures as detailed and accurate as possible on topics students are curious about, and for as long as possible."
        prompt = f"Please create a question based on the following description: '{answer}'. The question should include content related to '{keyword}' and must be formulated in sentence form. The question should be in English."
    else:  
        System_role = f"당신은 '{keyword}'를 가르치는 교수입니다. 제시되는 내용을 읽고 학생들이 궁금해할 내용에 대해 상세하고 정확하게 최대한 오랜 시간 동안 강의를 진행해야 합니다. "
        prompt = f"다음 설명에 대해 질문을 생성해주세요:'{answer}'. 이때 '{keyword}'와 관련된 내용을 포함해야 하며, 문장형식으로 질문을 작성해주세요. 질문은 한국어로 진행되어야 합니다."
        
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


# 생성한 질문에서 답변을 만드는 함수
def generate_detail_contents(contents, chatmodel, detailcontents, language="Korean") :
    
    for i in range(len(contents)):
        answer = contents[i]["Answer"] # 하나의 답변콘텐츠 뽑기
        System_role, prompt = create_DetailQuestion_with_keyword(answer,keyword)  # 컨텐츠에서 질문 생성 사용할 프롬프트 생성
        Q_text = generate_response(System_role, prompt, chatmodel,language="Korean")  # 프롬프트로 질문 생성
        
        detailcontents = generate_contents(Q_text, chatmodel, detailcontents, language="Korean")
        
    return detailcontents
    
        
def save_json_file(directory, file_name, data):
    if not os.path.exists(directory):
        os.makedirs(directory)
    file_path = os.path.join(directory, file_name)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"File saved: {file_path}")

if __name__ == "__main__":

    """ Config """
    OPENAI_API_KEY = "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"
    os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
    
    chat_model = "gpt-3.5-turbo-1106"
    language = "Korean"

    TopicKeywords = {
        "Korean": ["사출성형", "용접", "단조", "프레스"],
        "English": ["Injection Molding", "Welding", "Forging", "Pressing"]
    }

    selected_keywords = TopicKeywords["Korean"] if language == "Korean" else TopicKeywords["English"]
    
    for keyword in selected_keywords:
        
        contents = []
        detail_contents = []

        """ main """
        System_role, prompt = create_prompt_with_keyword(keyword)
        response_text = generate_response(System_role, prompt, chat_model, language=language)
        contents = generate_contents(response_text, chat_model, contents, language=language)
        
        detail_contents = generate_detail_contents(contents, chat_model, detail_contents, language=language)
        
        response_dict = {
            "keyword": keyword,
            "contents": contents,
            "source": chat_model,
            "date": datetime.now().strftime("%Y-%m-%d %H_%M_%S"),
            "language": language
        }
        
        directory_name = f"output/{keyword}"
        file_name = f"QnA_{keyword}_{chat_model}_{language}_{datetime.now().strftime('%Y-%m-%d_%H_%M_%S')}.json"
        save_json_file(directory_name, file_name, response_dict)
    
    print("All keyword processing completed.")
