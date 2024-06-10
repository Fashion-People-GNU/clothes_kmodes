import pandas as pd
from kmodes.kprototypes import KPrototypes
import joblib

from config import config as cfg

# 데이터 로드
df = pd.read_csv(r'D:\Development\Pycharm Projects\FashionPeople\datasets\final_result.csv')

# 범주형과 수치형 컬럼 분리
categorical_cols = ['나이', '성별', '스타일', '일 평균 기상',
                    '상의 색상', '상의 프린트', '상의 소재', '상의 기장', '상의 카테고리',
                    '하의 색상', '하의 프린트', '하의 소재', '하의 기장', '하의 카테고리']

numerical_cols = ['일 평균 기온', '일 평균 습도', '일 평균 풍속']

# 범주형과 수치형 컬럼 인덱스 확인
categorical_cols_indices = [df.columns.get_loc(col) for col in categorical_cols]

# 모델을 저장할 파일 경로
model_path = r'D:\Development\Pycharm Projects\FashionPeople\datasets\kproto_model.joblib'

# 클러스터의 수를 줄이고, 초기화 방법을 'Cao'로 변경하며, 초기화 시도 횟수를 증가
kproto = KPrototypes(n_clusters=20, init='Cao', n_init=10, verbose=2)
clusters = kproto.fit_predict(df, categorical=categorical_cols_indices)

# 클러스터 할당 결과
df['Cluster'] = clusters

# 학습된 모델 저장
joblib.dump(kproto, model_path)
print("모델이 성공적으로 학습되고 저장되었습니다.")

# 클러스터가 추가된 데이터프레임 저장
final_result_with_clusters_path = cfg.final_result_with_cluster_path
df.to_csv(final_result_with_clusters_path, index=False)
print("클러스터가 추가된 데이터프레임이 성공적으로 저장되었습니다.")

# 클러스터 중심점 출력
print(kproto.cluster_centroids_)

# 데이터프레임의 생략 없이 모든 행과 열을 출력하도록 설정
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# 데이터프레임의 첫 몇 줄을 출력하여 클러스터 할당 확인
print(df.head())

# 각 클러스터별로 데이터 출력
for cluster in range(kproto.n_clusters):
    print(f"클러스터 {cluster}의 데이터:")
    cluster_data = df[df['Cluster'] == cluster]
    print(cluster_data)
    print("\n")  # 클러스터별로 구분하기 위해 줄바꿈 추가

print("모델 학습 및 저장이 완료되었습니다.")
