with open("2_4.txt", "r", encoding="utf-8") as file:
    lines = file.readlines()

# 각 줄에서 줄바꿈 문자 제거
lines = [line.strip() for line in lines]
result_1 = ','.join(lines)
result = '1,3,237312'+ result_1

237363

