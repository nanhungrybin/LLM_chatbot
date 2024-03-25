"""API refer : https://github.com/martin-majlis/Wikipedia-API/tree/master"""
import os
from datetime import datetime
from urllib.parse import quote
import openai
import uuid
import wikipediaapi
import json
import Credential
import Model

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
    
def chunk_text(text, chunk_size = 500):
    """
    Description: 주어진 텍스트를 지정된 크기의 청크로 나눕니다.
    Argument:
    - text (str): 청킹할 텍스트
    - chunk_size (int): 각 청크의 최대 문자 수
    Return:
    - list of str: 청크로 나눠진 텍스트 리스트
    """    
    sentences = text.split('. ')
    current_chunk = ""
    chunks = []
    
    for sentence in sentences:
        if len(current_chunk) + len(sentence) > chunk_size : # 나눌 수 있다면
            chunks.append(current_chunk)
            current_chunk = sentence
        else:
            current_chunk += sentence + '. ' # 나눌 수 없다면
    
    chunks.append(current_chunk) # 마지막 청크 추가
    
    return chunks


def translate_chunks(chunks, chatmodel):
    """
    Description: 텍스트 청크 리스트를 번역합니다.
    Argument:
    - chunks (list of str): 번역할 텍스트 청크 리스트
    - chatmodel (str): 사용할 OpenAI 챗 모델
    Return:
    - str: 번역된 전체 텍스트
    """    
    translated_chunks = []
    
    for chunk in chunks :
        if language == "ko":
            translated_chunk = translate_to_korean(chunk, chatmodel)
            translated_chunks.append(translated_chunk)
        else:
            translated_chunk = translate_to_english(chunk, chatmodel)
            translated_chunks.append(translated_chunk)
        
    return "".join(translated_chunks)

# 전체 텍스트를 청크로 나누고, 각 청크를 순차적으로 번역한 후 이어 붙이는 과정을 진행
    

def translate_to_korean(text, chatmodel):
    
    # 각 청크를 번역한 다음, 결과를 합치는 역할
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
            {"role": "system", "content": "Translate the every following English text into Korean perfectly without summarizing:"},
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
            {"role": "system", "content": "Translate the every following Korean text into English perfectly without summarizing:"},
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

    os.environ["OPENAI_API_KEY"] = Credential.OPENAI_API_KEY
    chatmodel = Model.CHAT_MODEL

    
    for language, keywords in TopicKeywords.items():
        for keyword in keywords:
            
            data = get_wikipedia_content(keyword, "en" if language == "English" else "ko")
            
            print(f"Translating content for '{keyword}'...")
            
            ##################### 전체 텍스트를 청크로 나눔 #####################
            chunks = chunk_text(data["OriginalContent"])
            
            # 청크를 번역
            if language == "English":
                translated_chunks = [translate_to_korean(chunk, chatmodel) for chunk in chunks]
            else:
                translated_chunks = [translate_to_english(chunk, chatmodel) for chunk in chunks]
            
            # 번역된 청크들을 합침
            translated_content = "".join(translated_chunks)
            data["Translated Content"] = translated_content
            
            directory = os.path.join("Wikipedia_Content", keyword.replace(" ", "_"))
            filename = f"{keyword}_wikipedia_content.json"
            save_data_to_json(data, directory, filename)
