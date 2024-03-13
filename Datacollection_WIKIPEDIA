"""API refer : https://github.com/martin-majlis/Wikipedia-API/tree/master"""
import os
from datetime import datetime
from urllib.parse import quote
import openai
import uuid
import wikipediaapi
import json

def is_english(text):
    """
    Description: 주어진 텍스트가 영어인지 확인합니다.
    Argument:
    - text (str): 확인할 텍스트
    Return:
    - bool: 텍스트가 영어이면 True, 아니면 False
    """
    try:
        text.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True

def translate_to_korean(text, chatmodel):
    """
    Description: OpenAI API를 사용하여 영어 텍스트를 한국어로 번역합니다.
    Argument:
    - text (str): 번역할 영어 텍스트
    - chatmodel (str): 사용할 OpenAI 챗 모델
    Return:
    - str: 번역된 한국어 텍스트
    """
    response = openai.chat.completions.create(
        model=chatmodel,
        messages=[
            {"role": "system", "content": "Translate the following English text to Korean:"},
            {"role": "user", "content": text}
        ]
    )
    response_text = response.choices[0].message.content

    return response_text


def translate_to_english(text, chatmodel):
    """
    Description: OpenAI API를 사용하여 한국어 텍스트를 영어로 번역합니다.
    Argument:
    - text (str): 번역할 한국어 텍스트
    - chatmodel (str): 사용할 OpenAI Chat 모델
    Return:
    - str: 번역된 한국어 텍스트
    """
    response = openai.chat.completions.create(
        model=chatmodel,
        messages=[
            {"role": "system", "content": "Translate the following Korean text to English:"},
            {"role": "user", "content": text}
        ]
    )
    response_text = response.choices[0].message.content
    return response_text



def get_wikipedia_content(keyword, language):
    """
    Description: Wikipedia에서 키워드와 언어에 기반한 콘텐츠를 검색합니다.
    Argument:
    - keyword (str): 검색할 키워드
    - language (str): 사용할 언어 코드 (예: "en", "ko")
    Return:
    - dict: 검색된 콘텐츠와 메타데이터를 포함한 사전
    """
    encoded_keyword = quote(keyword)
    url = f"https://{language}.wikipedia.org/wiki/{encoded_keyword}"
    
    wiki_wiki = wikipediaapi.Wikipedia(
    user_agent='MyProjectName (merlin@example.com)',
        language=language,
        extract_format=wikipediaapi.ExtractFormat.WIKI
    )

    p_wiki = wiki_wiki.page(keyword)
    text_content = p_wiki.text

    if text_content:
        metadata = {
            "ID": str(uuid.uuid4()),
            "Topic": keyword,
            "Source URL": p_wiki.fullurl,
            "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Language": language
        }

        result = {
            "OriginalContent": text_content,
            "Metadata": metadata
        }

        return result
    else:
        return {"Error": "Page not found or other error occurred"}

def save_data_to_json(data, directory, filename):
    """
    Description: 주어진 데이터를 JSON 파일로 저장합니다.
    Argument:
    - data (dict): 저장할 데이터
    - directory (str): 저장할 디렉토리 경로
    - filename (str): 생성될 파일의 이름
    """
    if not os.path.exists(directory):
        os.makedirs(directory)

    filepath = os.path.join(directory, filename)
    with open(filepath, 'w', encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Data saved in {filepath}")
    

if __name__ == "__main__":
   

    TopicKeywords = {
        "Korean": ["사출성형"],
        "English": ["Injection Molding"]
    }

    
    OPENAI_API_KEY = "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"
    os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
    chatmodel = "gpt-3.5-turbo"

 

    for language, keywords in TopicKeywords.items():
        for keyword in keywords:
            data = get_wikipedia_content(keyword, "en" if language == "English" else "ko")
            
            if language == "English":
                translated_content = translate_to_korean(data["OriginalContent"], chatmodel)
                data["Translated Content"] = translated_content
           
            else:
                translated_content = translate_to_english(data["OriginalContent"], chatmodel)
                data["Translated Content"] = translated_content
                
                
            directory = os.path.join("Wikipedia_Content", keyword.replace(" ", "_"))
            filename = f"{keyword}_wikipedia_content.json"
            save_data_to_json(data, directory, filename)
