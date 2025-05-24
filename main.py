import os
import psutil
import time
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.documents import Document
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

# 환경 변수 로드
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

app = FastAPI(title="설교 요약 API", description="설교 원고를 요약하는 API입니다.")

# 템플릿 설정
templates = Jinja2Templates(directory="templates")

# 메트릭 정의
REQUEST_COUNT = Counter('request_count', 'Total number of requests')
REQUEST_LATENCY = Histogram('request_latency_seconds', 'Request latency in seconds')
MEMORY_USAGE = Histogram('memory_usage_bytes', 'Memory usage in bytes')
CPU_USAGE = Histogram('cpu_usage_percent', 'CPU usage percentage')

# Gemini 모델 초기화
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.7)

# 프롬프트 템플릿 정의
prompt = ChatPromptTemplate.from_template(
    """
    너는 다양한 연령대의 일반 성도들에게 말씀을 쉽게 전달하는 교회 콘텐츠 기획자야. 아래의 설교 원고 또는 영상 스크립트를 기반으로 성도들이 일상에서 바로 적용할 수 있는 
    짧고 공감 가는 말씀 요약을 작성해줘.
요약 방식은 다음과 같아:
오늘 말씀 핵심 요약 (1~10줄) 
오늘 설교의 주제 또는 핵심 메시지를 쉽게 요약
이해하기 쉬운 말, 기억에 남는 문장 중심으로
삶과 연결된 적용 (2~4줄)
직장, 가정, 인간관계 등 실생활에 연결된 적용 포인트 제시
비유나 예시가 있으면 좋고, 구체적이면 더 좋음
묵상 or 질문 또는 실천 (1줄)
"이 말씀 앞에서 나는 무엇을 결단할 수 있을까?"라는 질문
성도들이 한 주 동안 실천하거나 묵상할 수 있는 문장
반드시 신학적 용어는 쉽게 풀어서 말하고, 어린 아이부터 어른까지 공감할 수 있도록 작성해줘.:\n\n{context}
"""
)

# 요약 체인 생성
chain = create_stuff_documents_chain(llm, prompt)

class TextInput(BaseModel):
    text: str

@app.middleware("http")
async def monitor_requests(request: Request, call_next):
    start_time = time.time()
    REQUEST_COUNT.inc()
    
    # CPU 및 메모리 사용량 측정
    process = psutil.Process()
    cpu_percent = process.cpu_percent()
    memory_info = process.memory_info()
    
    CPU_USAGE.observe(cpu_percent)
    MEMORY_USAGE.observe(memory_info.rss)  # RSS: 실제 메모리 사용량
    
    response = await call_next(request)
    
    # 요청 처리 시간 측정
    REQUEST_LATENCY.observe(time.time() - start_time)
    
    return response

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/monitor", response_class=HTMLResponse)
async def monitor(request: Request):
    return templates.TemplateResponse("monitor.html", {"request": request})

@app.post("/summarize")
async def summarize_text(input_data: TextInput):
    try:
        # 문서 생성
        document = Document(page_content=input_data.text)
        
        # 요약 실행
        result = chain.invoke({"context": [document]})
        
        return JSONResponse(content={
            "status": "success",
            "summary": result
        })
    
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": str(e)
            }
        )

@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.get("/status")
async def status():
    process = psutil.Process()
    return {
        "cpu_percent": process.cpu_percent(),
        "memory_percent": process.memory_percent(),
        "memory_info": {
            "rss": process.memory_info().rss,  # 실제 메모리 사용량
            "vms": process.memory_info().vms,  # 가상 메모리 사용량
        },
        "num_threads": process.num_threads(),
        "create_time": process.create_time(),
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 