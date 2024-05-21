import os
from datetime import datetime
from urllib.parse import quote

import uuid
import json


from openai import AzureOpenAI

# 환경 변수 설정
os.environ["OPENAI_API_VERSION"] = "2024-02-15-preview"
os.environ["AZURE_OPENAI_ENDPOINT"] = "https://ix-genai.openai.azure.com/"
os.environ["AZURE_OPENAI_API_KEY"] = "24dfb271047e40c4aa018120db0671b0"

# openai 패키지의 API 키 및 엔드포인트 설정
client = AzureOpenAI(
  api_key = os.getenv("AZURE_OPENAI_API_KEY"),  
  api_version = os.getenv("OPENAI_API_VERSION"),
  azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")  # Your Azure OpenAI resource's endpoint value.
)

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
        if is_english(chunk) == True:
            translated_chunk = translate_to_korean(chunk, chatmodel)
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

    response = client.chat.completions.create(
        model="gpt-4",  # Azure에서 사용 가능한 모델 이름 명시
        messages=[
            {"role": "system", "content": "Translate the every following English text into Korean perfectly without summarizing:"},
            {"role": "user", "content": text}
        ],
        max_tokens=100,
        temperature=0.7
    )


    response_text = response.choices[0].message.content
    
    return response_text


def save_to_file(data, path, filename, language):
    if not os.path.exists(path):
        os.makedirs(path)
    file_path = os.path.join(path, filename)
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(f"Language: {language}\n")
        file.write(data)
    

def process_text(file_path, chatmodel):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    # "author:", "text:", "reference:" 부분을 분리
    sections = {"author": "", "text": "", "references": ""}
    current_section = None
    
    for line in text.splitlines():
        if line.lower().startswith("author:"):
            current_section = "author"
        elif line.lower().startswith("text:"):
            current_section = "text"
        elif line.lower().startswith("references:"):
            current_section = "references"
        
        if current_section:
            sections[current_section] += line + "\n"
    
    # "text:" 부분만 번역
    text_to_translate = sections["text"].replace("text:", "").strip()
    
    titleofDB = os.path.basename(file_path)
    
    language = "ko" if not is_english(titleofDB) else "en"
    
    if is_english(text_to_translate):
        chunks = chunk_text(text_to_translate)
        translated_text = translate_chunks(chunks, chatmodel)
        sections["text"] = "text:\n" + translated_text + "\n"
        translated_filename = f"translated_{titleofDB}"
    else:
        translated_filename = titleofDB

    output_dir = "/home/azureuser/cloudfiles/code/Users/hb.suh/0521번역_사출성형"
    
    # 모든 섹션을 합쳐서 저장
    final_text = sections["author"] + sections["text"] + sections["references"]
    save_to_file(final_text, output_dir, translated_filename, language)
    
    # 원본 파일도 저장
    original_filename = titleofDB
    save_to_file(text, output_dir, original_filename, "original")


chatmodel = "gpt-4"


output_base_path = "/home/azureuser/cloudfiles/code/Users/hb.suh/OUR_BERT/CODE/사출성형/split_사출성형"
for file in os.listdir(output_base_path):
    file_path = os.path.join(output_base_path, file)
    process_text(file_path, chatmodel)
