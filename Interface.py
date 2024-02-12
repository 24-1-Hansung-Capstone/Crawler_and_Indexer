import requests
import bs4
import os
import selenium
import chromedriver_autoinstaller
from fake_useragent import UserAgent

class MethodNotImplementError(Exception) :
    def __init__(self, methodName=""):
        self.errorMsg = f"{methodName} Method is not implements."
        super().__init__(self.errorMsg)

class CrawlingInterface :

    """
    * @param       : (self), 타겟 url
    * @return type : str
    * @description : 해당 함수를 통해 본문의 내용을 가져온다. 이떄 태그
    *
    """
    def getText(self, url : str) -> str:
        # TODO : 본문 내용 가져오기
        mainBody = self.selectTag()

        # TODO : mainBody를 통해 문자열을 가져오도록 수정
        result = "본문 내용입니다."
        return result

    """
    * @param       : (self)
    * @return      : 정확하게 정하진 않았지만, html dom 객체를 반환하는 것으로 생각
    * @description : 타겟 url에서 본문의 위치를 찾아 해당하는 dom 객체를 반환(이 부분은 바뀔 수 있으나, 큰 흐름은 같음)
    *                해당 메서드를 구현해야한다. 구현하지 않은 상태로 호출시, MethodNotImplementError 예외를 raise함.
    """
    def selectTag(self):
        raise MethodNotImplementError("selectTag")

if __name__ == "__main__" :
    class TestCrawler(CrawlingInterface):
        def selectTa1g(self):
            return 1


    testCrawler = TestCrawler()
    target = testCrawler.getText("127.0.0.1:8080")
    print(target)