import pandas as pd             #для загрузки из csv и работы с массивами
import numpy as np              #для нахождения линейной регрессии
import matplotlib.pyplot as plt #для построения графиков


def oil(fname):
    """
    08/07/2016 - Konstantin Gavrilov - gavrilovks@gmail.com

    1) берем csv файл
    2) загружаем данные в массив
    3) берем последовательно каждую точку массива
    4) делим массив на две части в этой точке
    5) находим отклонения линейной регресии (олр) для каждой части
    6) созадем массивы с олр
    7) считаем сумму квадратов ошибки олр для двух частей
    8) находим минимальную ошибку в массивеб берем номер точки
    9) строимм график для этой точки (на графике: два массива, две линии регрессии, коэффициенты)

    :param fname: путь до cvs файла с данными
    :return:
    """

    #1-2) загружаем дату из cvs файла fname
    #в файле три столбца q, Q и q/Q, без заголовка
    df = pd.read_csv(fname, names=['Well', 'ProdDays','q', 'Q', 'qQ'])

    fits1 = [] #массив с олр для первой части
    fits2 = [] #массив с олр для второй части
    output1 = []

    Wellnames = set(df['Well'].values) #array with unique wellnames
    for i in range(1, len(set(df['Well'].values))-2): # limiting database to one wellname
        Name = Wellnames.pop()
        df = (df[(df['Well'] == Name)])

        for i in range(3, len(df)-3): # 3) берем последовательно каждую точку массива
            # 4) делим массив на две части в этой точке
            y1 = df['qQ'][:i].values
            y2 = df['qQ'][i:].values

            x1 = list(range(len(y1)))
            x2 = list(range(len(y1), len(y1) + len(y2)))

            # 5) находим отклонения линейной регресии(олр) для каждой части
            fit1 = np.polyfit(x1, y1, 1, full=True)
            fit2 = np.polyfit(x2, y2, 1, full=True)



            # 6) созадем массивы с олр
            fits1.append(fit1[1][0]) # добавляем отклонения
            fits2.append(fit2[1][0])


        er2 = []  # массив квадратов отклонений
        # 7) считаем сумму квадратов ошибки олр для двух частей
        for i in range(len(fits1)):
            er2.append(fits1[i]*fits1[i]+fits2[i]*fits2[i]) #считаем сумму квадратов отклонений для каждой точки

        # 8) находим минимальную ошибку в массиве берем номер точки
        print(er2)  # отобразить массив ск отклонений
        gp = er2.index(min(er2)) + 3 # #находим индекс минимального значения ск отклонения, так как изначально массив разбивается с третьей точки добавляем 3



        # 9) строимм график для этой точки (на графике: два массива, две линии регрессии, коэффициенты)

        # разбиваем массив в найденной точке
        y1 = df['qQ'][:gp].values
        y2 = df['qQ'][gp:].values

        x1 = list(range(len(y1)))
        x2 = list(range(len(y1), len(y1) + len(y2)))

        # считаем значения отклонения
        fit1 = np.polyfit(x1, y1, 1, full=True)
        fit2 = np.polyfit(x2, y2, 1, full=True)

        fit_fn1 = np.poly1d(fit1[0])
        fit_fn2 = np.poly1d(fit2[0])

        #строим график
        #plt.yscale('log') # логарифмическая шкала y
        #plt.xscale('log') # логарифмическая шкала x
        plt.text(len(x1) / 2, y1.mean(), fit1[1][0]) #надпись первого отклонения
        plt.text(len(x1) + len(x2) / 2, y2.mean(), fit2[1][0]) #надпись второго отклонения
        plt.plot(x1, y1, '-', x1, fit_fn1(x1), '--k') #график первой части с регрессией
        plt.plot(x2, y2, '-', x2, fit_fn2(x2), '--k') #график второй части с регрессией
        plt.show()


    output1.append(df[(gp - 2):(gp + 2)])

print(output1)

oil('test_data2.csv') #передаем функции название файла


