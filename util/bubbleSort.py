def bubbleSort(listx):
    lrange= len(listx)
    for i in range(lrange-1):  #外循环控制一共要比较多少次元素
        for j in range(lrange-1-i):      #内循环控制每一次元素的比对
            if listx[j]<listx[j+1]:
                listx[j+1],listx[j] = listx[j],listx[j+1]
    return listx

print(bubbleSort([1,28,6,39,2]))