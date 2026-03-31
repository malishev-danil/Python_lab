def get_matrix_size():
    # Запрашивает у пользователя размер квадратной матрицы. Осуществляет проверку введённых данных.
    while True:
        try:
            n = int(input("Enter square matrix size: "))
            if n > 0:
                return n
            print("Error: size must be a positive number.")
        except ValueError:
            print("Error: please enter an integer.")


def get_matrix_rows(n):
    # Запрашивает у пользователя элементы матрицы построчно. Проверяет количество элементов в каждой строке.
    matrix = []
    print("Enter matrix elements:")
    
    for i in range(n):
        while True:
            try:
                row = list(map(int, input("Row " + str(i + 1) + ": ").split()))
                if len(row) == n:
                    matrix.append(row)
                    break
                print("Error: row must have exactly " + str(n) + " elements.")
            except ValueError:
                print("Error: please enter integers only.")
    
    return matrix


def swap_diagonals(matrix, n):
    # Меняет местами элементы главной и побочной диагоналей матрицы.
    for i in range(n):
        temp = matrix[i][i]
        matrix[i][i] = matrix[i][n - 1 - i]
        matrix[i][n - 1 - i] = temp


def print_matrix(matrix, title):
    # Выводит матрицу на экран с заголовком.
    print("")
    print(title)
    for row in matrix:
        for element in row:
            print(str(element), end=" ")
        print("")


def main():
    n = get_matrix_size()
    matrix = get_matrix_rows(n)
    print_matrix(matrix, "Original matrix:")
    swap_diagonals(matrix, n)
    print_matrix(matrix, "Matrix after swapping diagonals:")


if __name__ == "__main__":
    main()