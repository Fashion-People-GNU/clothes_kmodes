from server_api import run
import clothes_enum as CLTH
import config.config as cfg
import json

"""
user_info에 값을 넣을때는 "나이, 성별, 스타일, 일 평균 기온, 일 평균 기상, 일 평균 습도, 일 평균 풍속" 순서를 지켜서
"""
def data_sort(clothes, type):
    # 데이터 정렬
    # '상의 카테고리'와 '상의 색상'의 빈도수를 계산하여 데이터 프레임에 추가
    category_counts = clothes[f'{type} 카테고리'].value_counts()
    color_counts = clothes[f'{type} 색상'].value_counts()

    clothes['category_count'] = clothes[f'{type} 카테고리'].map(category_counts)
    clothes['color_count'] = clothes[f'{type} 색상'].map(color_counts)

    # 빈도수 기준으로 정렬
    df_sorted = clothes.sort_values(by=['category_count', 'color_count'], ascending=[False, False]).drop(columns=['category_count', 'color_count'])

    return df_sorted

def main(age, sex, style, temperatures, weather, humidity, wind_speed):
    top_id = ""
    top_color = ""
    top_print = ""
    top_material = ""
    top_length = ""
    top_category = ""

    bottom_id = ""
    bottom_color = ""
    bottom_print = ""
    bottom_material = ""
    bottom_length = ""
    bottom_category = ""

    user_info = (age, sex, style, temperatures, weather, humidity, wind_speed)
    # 하의를 먼저할지 상의를 먼저할지는 CLTH.TOP, CLTH.BOTTOM 으로 설정하면 됨

    # ==========================================================================================
    # 상의 추천
    top_clothes = run.predict(user_info, CLTH.TOP)

    # JSON 파일 경로
    json_file_path = cfg.json_path

    # JSON 파일 읽기
    with open(json_file_path, 'r', encoding='utf-8') as file:
        user_clothes = json.load(file)

    # 각 항목의 필요한 필드를 추출하여 2차원 배열로 저장
    clothes_attributes = [[item['type'], item['color'], item['length'], item['material'], item['printing'], item['id']] for item in user_clothes]

    # 데이터 정렬
    df_sorted = data_sort(top_clothes, "상의")

    for cloth in df_sorted.iloc:
        if cloth["나이"] == age and cloth["성별"] == sex and cloth["스타일"] == style:
            for attributes in clothes_attributes:
                if cloth["상의 카테고리"] == attributes[0] and cloth["상의 색상"] == attributes[1]:# and cloth["상의 기장"] == attributes[2] and cloth["상의 소재"] == attributes[3] and cloth["상의 프린트"] == attributes[4]:
                    top_id = attributes[5]
                    top_color = cloth["상의 색상"]
                    top_print = cloth["상의 프린트"]
                    top_material = cloth["상의 소재"]
                    top_length = cloth["상의 기장"]
                    top_category =  cloth["상의 카테고리"]
                    break

    print("상의 추천")
    print(top_color, top_print, top_material, top_length, top_category, top_id)

    # ==========================================================================================
    # 하의 추천
    top_clothes = (top_color, top_print, top_material, top_length, top_category)
    bottom_clothes = run.predict(user_info, top_clothes, CLTH.BOTTOM)

    # 데이터 정렬
    df_sorted = data_sort(bottom_clothes, "하의")

    for cloth in df_sorted.iloc:
        if cloth["나이"] == age and cloth["성별"] == sex and cloth["스타일"] == style:
            for attributes in clothes_attributes:
                if cloth["상의 카테고리"] == top_category and cloth["상의 색상"] == top_color:
                    #print(cloth)
                    if cloth["하의 카테고리"] == attributes[0] and cloth["하의 색상"] == attributes[1]:# and cloth["하의 기장"] == attributes[2] and cloth["하의 소재"] == attributes[3] and cloth["하의 프린트"] == attributes[4]:
                        bottom_id = attributes[5]
                        bottom_color = cloth["하의 색상"]
                        bottom_print = cloth["하의 프린트"]
                        bottom_material = cloth["하의 소재"]
                        bottom_length = cloth["하의 기장"]
                        bottom_category =  cloth["하의 카테고리"]
                        break
    
    print("하의 추천")
    print(bottom_color, bottom_print, bottom_material, bottom_length, bottom_category, bottom_id)

    return top_id, bottom_id

if __name__ == "__main__":
    age = "30대" # 사용자 입력 데이터
    sex = "남성" # 사용자 입력 데이터
    style = "스트리트" # 사용자 입력 데이터
    temperatures = "55.4" # 오늘 기온
    weather = "비" # 오늘 기상
    humidity = "77.3" # 오늘 습도
    wind_speed = "2.6" # 오늘 풍속
    result = main(age, sex, style, temperatures, weather, humidity, wind_speed)
    print(result)