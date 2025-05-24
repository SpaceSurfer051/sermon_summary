import os
import sys
import pytest
from langchain_core.documents import Document

# 프로젝트 루트 디렉토리를 Python 경로에 추가
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import chain

def test_document_creation():
    text = "테스트 텍스트입니다."
    doc = Document(page_content=text)
    assert doc.page_content == text

def test_chain_invocation():
    text = """
    오늘은 하나님의 사랑에 대해 말씀드리겠습니다.
    하나님은 우리를 무한히 사랑하시는 분이십니다.
    """
    result = chain.invoke({"context": [Document(page_content=text)]})
    assert isinstance(result, str)
    assert len(result) > 0

def test_chain_with_empty_text():
    text = ""
    with pytest.raises(Exception):
        chain.invoke({"context": [Document(page_content=text)]}) 