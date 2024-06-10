from server_api import run
import clothes_enum as CLTH

"""
user_info에 값을 넣을때는 "나이, 성별, 스타일, 일 평균 기온, 일 평균 기상, 일 평균 습도, 일 평균 풍속" 순서를 지켜서
"""
def main():
    # 임시 데이터
    user_info = ("20대", "남성", "스트리트", "15.0", "맑음", "51.3", "2.5")
    # 하의를 먼저할지 상의를 먼저할지는 CLTH.TOP, CLTH.BOTTOM 으로 설정하면 됨
    top_clothes = run.predict(user_info, CLTH.TOP)
    print(top_clothes)

    # bottom_clothes = run.predict(user_info, top_clothes, CLTH.BOTTOM)
    # print(bottom_clothes)

if __name__ == "__main__":
    main()