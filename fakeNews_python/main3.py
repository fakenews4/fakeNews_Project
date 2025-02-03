# from handler.proposal import fetch_news_from_api, save_news_to_db, get_random_news_recommendations

# def main():
#     # Step 1: 키워드 정의
#     keywords = ["갤럭시s25"]  # 로컬스토리지 키워드 시뮬레이션

#     print("\n[키워드 목록]")
#     print(", ".join(keywords))
#     # input("위 키워드로 뉴스를 검색하려면 Enter를 누르세요...\n")

#     # Step 2: API에서 뉴스 가져오기
#     print("API에서 뉴스를 가져오고 있습니다...")
#     news_items = fetch_news_from_api(keywords)

#     # Step 3: 중복 확인 및 DB 저장
#     print("중복을 확인하고 DB에 저장 중입니다...")
#     save_news_to_db(news_items)
#     print("DB 저장 완료!\n")

#     while True:
#         # Step 4: 관련 기사 랜덤 추천
#         print("관련 기사를 랜덤으로 추천 중입니다...")
#         recommended_news = get_random_news_recommendations(keywords)

#         if recommended_news.empty:
#             print("관련된 기사가 없습니다. 다른 키워드를 사용해 보세요.")
#             break

#         print("\n[추천 뉴스 목록]")
#         for idx, row in recommended_news.iterrows():
#             print(f"{idx + 1}. 제목: {row['title']}")
#             print(f"   링크: {row['link']}")
#             print(f"   요약: {row['description']}\n")

#         # 사용자 입력 처리
#         print("1: 더 많은 추천 보기")
#         print("2: 종료")
#         action = input("원하는 작업을 선택하세요: ")

#         if action == "1":
#             print("\n새로운 추천 뉴스를 가져옵니다...\n")
#         elif action == "2":
#             print("\n프로그램을 종료합니다. 감사합니다!")
#             break
#         else:
#             print("\n잘못된 입력입니다. 다시 선택하세요.\n")

# if __name__ == "__main__":
#     main()
