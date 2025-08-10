def insertion_sort(arr: list[int]) -> list[int]:
    arr_len = len(arr)
    for i in range(1, arr_len): # начинаем со второго элемента
        key = arr[i]
        j = i - 1

        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1

        arr[j+1] = key

    return arr


# Пример использования:
my_list = [64, 34, 25, 12, 22, 11, 90]
insertion_sort(my_list)
print("Отсортированный список:", my_list)