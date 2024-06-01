# LLM_chatbot

## 📁 Data collection : 

<img width="821" alt="image" src="https://github.com/nanhungrybin/LLM_chatbot/assets/97181397/4ddab2a2-cf41-43d4-86d7-710a85dc56a4">


## 📁 Retrival model Finetuning ( Domain Adaptation & Text embedding model Fintuning ) : 

<img width="821" alt="image" src="https://github.com/nanhungrybin/LLM_chatbot/assets/97181397/abb16bf1-1d91-4b07-beff-17a1092256d2">


## 📁 Generation model Fintuning :
- 한국어에 특화된 Saltlux/Ko-Llama3-Luxia-8B 활용
- GPT-4o를 이용한 Q & A dataset생성 (현재 생성 용량: 16.76MB) 
   - input: Relevant Document, output: Q & A
   -  Q&A dataset (train: 4269개, validation: 1641개)
     
- Fintuning Method
  - QuantizedLoRA + FSDP(Fully Shared Data Parallel) 방법 활용
  - Instruction Tuning on 사출성형 (Injection Molding) dataset
    - {Question: Relevant Document } -> Answer
      
- 평가 지표 : 코사인 유사도
  - 질문이 주어졌을 때, GPT-4o가 생성한 답변 (A)와 각 모델이 생성한 답변(B) 간의 유사도 측정

- 파인튜닝 결과
<img width="925" alt="image" src="https://github.com/nanhungrybin/LLM_chatbot/assets/97181397/cb1c8557-bac2-4b42-9af0-9cfef61c1f49">

      
