# import requests
# import os

# # API 키 설정 (Google Cloud에서 발급받아야 함)
# API_KEY = "AIzaSyDGDSQwSDFG3u7HPROGPFhCkrgRsgDTr-w"
# QUERY = "COVID-19 vaccine microchips"

# # API 요청 URL
# url = f"https://factchecktools.googleapis.com/v1alpha1/claims:search?query={QUERY}&key={API_KEY}"

# # API 요청
# response = requests.get(url)

# # 응답 확인
# if response.status_code == 200:
#     data = response.json()
#     print("팩트체크 결과:")
#     for claim in data.get("claims", []):
#         print(f"출처: {claim['claimReview'][0]['publisher']['name']}")
#         print(f"팩트체크 내용: {claim['claimReview'][0]['textualRating']}")
#         print(f"링크: {claim['claimReview'][0]['url']}")
#         print("-" * 50)
# else:
#     print("API 요청 실패:", response.status_code, response.text)
