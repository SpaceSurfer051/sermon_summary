import os
import sys
import pytest
from fastapi.testclient import TestClient

# 프로젝트 루트 디렉토리를 Python 경로에 추가
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import app

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def sample_text():
    return """
    오늘은 하나님의 사랑에 대해 말씀드리겠습니다.
    하나님은 우리를 무한히 사랑하시는 분이십니다.
    우리의 모든 죄를 용서하시고, 우리를 자녀로 삼아주셨습니다.
    이 사랑을 우리도 이웃에게 나누어야 합니다.
    """ 