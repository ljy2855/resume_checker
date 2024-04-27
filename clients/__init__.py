from abc import ABC, abstractmethod


class BaseClient(ABC):
    """
    LLM 클라이언트들의 베이스 클래스
    """

    @abstractmethod
    def evaluate_text(self, text):
        """
        주어진 텍스트를 평가하는 메소드
        """
        pass
