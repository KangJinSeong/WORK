import csv
import matplotlib.pyplot as plt

# CSV 파일 경로
file_path = '/home/kwfi/CSV_Data/2024년/3월/15일/Result_2024-03-15 15:46:09_1_Station_4_Station.csv'

# 데이터를 저장할 리스트 초기화
x_data = []
y_data = []

# CSV 파일 읽기
with open(file_path, 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        x_data.append(row)

x_data[0][-1] = x_data[0][-1][1] 
result = [int(i) for i in x_data[0][4:]]
max_index = result.index(max(result))
print(f'MAX_INDEX : {max_index}')

plt.plot(result)
plt.grid()
plt.xlabel('Number of sample[N]')
plt.ylabel('Magnitude')
plt.show()
