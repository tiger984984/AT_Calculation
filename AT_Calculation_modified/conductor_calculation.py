import numpy as np

from scipy import linalg

from scipy import constants as C

from scipy import special

from sqlite3 import connect

import pandas as pd

import numpy as np

import ipynb_importer

import new_topology as tp

# 导线定义

topology = tp.Topology(name="测试供电臂")
#############################################################################################
topology.set_topology(db_file_name="DT-system.db")
############测试lines对象##################################################
print('====================================================================================')
# for i in range(14):
# print(topology.lines[i].name, topology.lines[i].type_name, topology.lines[i].resistance, topology.lines[i].radius, topology.lines[i].equivalent_radius, topology.lines[i].rho, topology.lines[i].mu_r, topology.lines[i].coordinate_x, topology.lines[i].coordinate_y)

"""

1. 接触线（CW1）; 2.承力索（MW1）; 3.钢轨1（RA1）;4.钢轨2（RA2）;5.综合地线（E1）

6. 接触线（CW2）; 7.承力索（MW2）; 8.钢轨3（RA3）;9.钢轨4（RA4）;10.综合地线（E2）
###
1. 接触线（CW1）; 2.承力索（MW1）; 3.正馈线（PF1）; 4.钢轨1（RA1）;5.钢轨2（RA2）;6.保护线（PW1）;7.综合地线（E1）

8. 接触线（CW2）; 9.承力索（MW2）; 10.正馈线（PF2）; 11.钢轨3（RA3）;12.钢轨4（RA4）;13.保护线（PW2）;14.综合地线（E2）

"""
###判断AT和DT
if topology.lines_system == "AT":
    N = 14
elif topology.lines_system == "DT":
    N = 10
conductors_coordinator = np.zeros(shape=(N, 2))

for i in range(0, N):
    conductors_coordinator[i][0] = topology.lines[i].coordinate_x

    conductors_coordinator[i][1] = topology.lines[i].coordinate_y


conductors_coordinator = conductors_coordinator * 0.001


print('坐标')
print(conductors_coordinator)
print('*************************************')

conductors_calc_radius = np.zeros(N, np.float)

for i in range(0, N):
    conductors_calc_radius[i] = topology.lines[i].radius


conductors_calc_radius = conductors_calc_radius * 0.001

print('计算半径')
print(conductors_calc_radius)
print('++++++++++++++++++++++++++++++++++++++++')

conductors_equivalent_radius = np.zeros(N, np.float)

for i in range(0, N):
    conductors_equivalent_radius[i] = topology.lines[i].equivalent_radius
conductors_equivalent_radius = conductors_equivalent_radius * 0.001
print('等效半径')
print(conductors_equivalent_radius)
print('//////////////////////////////////////////')
mu_r = np.zeros(N, np.float)

for i in range(0, N):
    mu_r[i] = topology.lines[i].mu_r

print('磁导率')
print(mu_r)
print('[[[[[[[[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]]]]]]]]')
rho = np.zeros(N, np.float)

for i in range(0, N):
    rho[i] = topology.lines[i].rho

print('电阻率')
rho = rho * 0.01777 * 10 ** -6
print(rho)
print("--------------------------------------------")


Rd = np.zeros(N, np.float)

for i in range(0, N):
    Rd[i] = topology.lines[i].resistance

print('直流电阻')
print(Rd)
print('###########################################')


def calc_potential_coefficient(c_xy, r):  # 计算电位系数矩阵

    """ 计算电位系数矩阵P

    """

    n = np.shape(c_xy)[0]

    P = np.zeros((n, n), np.float64)

    for i in range(n):

        for j in range(n):

            if i == j:

                P[i, i] = 18 * 10 ** +6 * np.log(2 * c_xy[i, 1] / r[i])

            else:

                Dij = np.sqrt((c_xy[i, 0] - c_xy[j, 0]) ** 2 + (c_xy[i, 1] + c_xy[j, 1]) ** 2)

                dij = np.sqrt((c_xy[i, 0] - c_xy[j, 0]) ** 2 + (c_xy[i, 1] - c_xy[j, 1]) ** 2)

                P[i, j] = 18 * 10 ** +6 * np.log(Dij / dij)

    return P


def merge_potential_coefficient(P, m, k):  # 电位系数矩阵归并，k线归并到m线

    n = np.shape(P)[0]

    for i in range(n):
        P[i, k] = P[i, k] - P[i, m]

    for i in range(n):

        for j in range(n):

            if i != k and j != k:
                P[i, j] = P[i, j] - P[i, k] / (P[k, k] - P[m, k]) * (P[k, j] - P[m, j])

    E = np.empty((n - 1, n - 1), np.float64)

    for i in range(n):

        for j in range(n):

            if i < k:

                if j < k:
                    E[i, j] = P[i, j]

                if j > k:
                    E[i, j - 1] = P[i, j]

            if i > k:

                if j < k:
                    E[i - 1, j] = P[i, j]

                if j > k:
                    E[i - 1, j - 1] = P[i, j]

    return E


if __name__ == '__main__':
    # 测试

    P = calc_potential_coefficient(conductors_coordinator, conductors_calc_radius)

    P = merge_potential_coefficient(P, 0, 1)

    P = merge_potential_coefficient(P, 1, 2)

    P = merge_potential_coefficient(P, 3, 4)

    P = merge_potential_coefficient(P, 4, 5)

    np.set_printoptions(precision=3, linewidth=214, suppress=True)

    print('P矩阵 e+7 : \n {}'.format(P * 10 ** -7))


def calc_B(P):
    """ 计算电容系数矩阵"""

    B = linalg.inv(P)

    return B


if __name__ == '__main__':
    B = calc_B(P)

    np.set_printoptions(precision=3, linewidth=214, suppress=True)

    print('B矩阵(×e-9) : \n {}'.format(B * 10 ** 9))


def calc_L(c_xy, r):
    n = np.shape(c_xy)[0]

    L = np.empty((n, n), np.float64)

    # 计算导线外自感和互电感

    for i in range(n):

        for j in range(n):

            if i == j:

                L[i, i] = 2 * 10 ** -4 * np.log(2 * c_xy[i, 1] / r[i])

            else:

                Dij = np.sqrt((c_xy[i, 0] - c_xy[j, 0]) ** 2 + (c_xy[i, 1] + c_xy[j, 1]) ** 2)

                dij = np.sqrt((c_xy[i, 0] - c_xy[j, 0]) ** 2 + (c_xy[i, 1] - c_xy[j, 1]) ** 2)

                L[i, j] = 2 * 10 ** -4 * np.log(Dij / dij)

    return L


if __name__ == '__main__':
    # 函数测试

    f = 50

    c_xy = conductors_coordinator

    r = conductors_calc_radius

    L = calc_L(c_xy, r)

    np.set_printoptions(precision=4, linewidth=214, suppress=True)

    print('L矩阵(×e-3) : \n {}'.format(L * 10 ** 3))


def calc_Zc1(f, Rd, r, mu_r, rho):
    n = np.shape(Rd)[0]

    Zc = np.zeros(n, np.complex128)

    for i in range(n):
        m = np.sqrt(2 * np.pi * f * mu_r[i] * 4 * np.pi * 10 ** -7 / rho[i])

        mr = m * r[i]

        #    print(mr)

        a = special.ber(mr) + 1j * special.bei(mr)

        b = special.berp(mr) + 1j * special.beip(mr)

        c = 1j * a / b

        #    print('a=',a)

        #    print('b=',b)

        #    print('c=',c)

        alphaR = (mr / 2) * np.real(c)

        alphaL = (4 / mr) * np.imag(c)

        #    print('alphaL = ',alphaL)

        Rc = Rd[i] * alphaR

        Xc = np.pi * f * 10 ** -4 * mu_r[i] * alphaL

        Zc[i] = Rc + 1j * Xc

        print(Zc[i])

    return Zc


def calc_Zc(f, Rd, r, mu_r, rho):  # 计算导线内阻抗

    """



    :param f:     频率

    :param Rd:    直流电阻

    :param r:     计算半径

    :param mu_r:  相对磁导率

    :param rho:   电导率

    :return:      内阻抗

    """

    n = np.shape(Rd)[0]

    Zc = np.zeros(n, np.complex128)

    for i in range(n):
        m = np.sqrt(2 * np.pi * f * mu_r[i] * 4 * np.pi * 10 ** -7 / rho[i])

        mr = m * r[i]

        # print(mr)

        A = special.ber(mr) * special.beip(mr) - special.bei(mr) * special.berp(mr)

        B = special.bei(mr) * special.beip(mr) + special.ber(mr) * special.berp(mr)

        C = special.berp(mr) ** 2 + special.beip(mr) ** 2

        # print('B/C=',B/C,'A/C=',A/C)

        # print('A/C=',A/C)

        alphaR = (mr / 2) * (A / C)

        alphaL = (4 / mr) * (B / C)

        #     print('alphaL = ',alphaL)

        Rc = Rd[i] * alphaR

        Xc = np.pi * f * 10 ** -4 * mu_r[i] * alphaL

        Zc[i] = Rc + 1j * Xc

        print(Zc[i])

    return Zc


if __name__ == '__main__':
    # 测试

    # dd = np.empty((5),np.float64)

    # print(dd)

    f = 5000

    re = conductors_calc_radius

    print('Zc=')

    Zc = calc_Zc(f, Rd, re, mu_r, rho)

    # print('Zc矩阵 : \n {}'.format(Zc))

    print('Zc1=')

    Zc1 = calc_Zc1(f, Rd, re, mu_r, rho)


    # print('Zc1矩阵 : \n {}'.format(Zc1))

# print(Zc1)


def calc_Zgm(f, c_xy, rou):  # 计算大地阻抗矩阵

    n = np.shape(c_xy)[0]

    Rgm = np.zeros((n, n), np.float64)

    Xgm = np.zeros((n, n), np.float64)

    for i in range(n):

        for j in range(n):
            Dij = np.sqrt((c_xy[i, 0] - c_xy[j, 0]) ** 2 + (c_xy[i, 1] + c_xy[j, 1]) ** 2)

            xij = np.abs(c_xy[i, 0] - c_xy[j, 0])

            theta = np.arcsin(xij / Dij)

            k = 4 * np.pi * np.sqrt(5) * 10 ** -4 * Dij * np.sqrt(f / rou)

            Rgm[i, j] = calc_Rg(f, k, theta)

            Xgm[i, j] = calc_Xg(f, k, theta)

    return Rgm + 1j * Xgm


def calc_Rg(f, k, theta):  # 计算大地电阻

    b1 = np.sqrt(2) / 6

    b2 = 1 / 16

    b3 = b1 / (3 * 5)

    b4 = b2 / (4 * 6)

    b5 = -b3 / (5 * 7)

    b6 = -b4 / (6 * 8)

    b7 = -b5 / (7 * 9)

    b8 = -b6 / (8 * 10)

    c2 = 1.3659315

    c4 = c2 + 1 / 4 + 1 / 6

    c6 = c4 + 1 / 6 + 1 / 8

    d4 = np.pi / 4 * b4

    d6 = np.pi / 4 * b6

    d8 = np.pi / 4 * b8

    if k < 5.1:

        Rg = np.pi / 8 - b1 * k * np.cos(theta) + b1 * k * np.cos(theta) + b2 * (
                    (c2 - np.log(k)) * k ** 2 * np.cos(2 * theta) + theta * k ** 2 * np.sin(
                2 * theta)) + b3 * k ** 3 * np.cos(3 * theta) - d4 * k ** 4 * np.cos(4 * theta) - b5 * k ** 5 * np.cos(
            5 * theta) + b6 * ((c6 - np.log(k)) * k ** 2 * np.cos(6 * theta) + theta * k ** 6 * np.sin(
            6 * theta)) + b7 * np.cos(7 * theta) - d8 * k ** 8 * np.cos(8 * theta)

    else:

        Rg = np.cos(theta) / k - np.sqrt(2) * np.cos(2 * theta) / k ** 2 + np.cos(3 * theta) / k ** 3 + 3 * np.cos(
            5 * theta) / k ** 5 - 45 * np.cos(7 * theta)

        Rg = Rg / np.sqrt(2)

    Rg = 4 * 2 * np.pi * f * 10 ** -4 * Rg

    return Rg


def calc_Xg(f, k, theta):  # 计算大地回路电感

    b1 = np.sqrt(2) / 6

    b2 = 1 / 16

    b3 = b1 / (3 * 5)

    b4 = b2 / (4 * 6)

    b5 = -b3 / (5 * 7)

    b6 = -b4 / (6 * 8)

    b7 = -b5 / (7 * 9)

    b8 = -b6 / (8 * 10)

    c2 = 1.3659315

    c4 = c2 + 1 / 4 + 1 / 6

    c6 = c4 + 1 / 6 + 1 / 8

    c8 = c4 + 1 / 8 + 1 / 10

    d2 = np.pi / 4 * b2

    d4 = np.pi / 4 * b4

    d6 = np.pi / 4 * b6

    d8 = np.pi / 4 * b8

    if k < 5.1:

        Xg = 0.5 * (0.6159315 - np.log(k)) + b1 * k * np.cos(theta) - d2 * k * k * np.cos(
            2 * theta) + b3 * k ** 3 * np.cos(3 * theta) - b4 * (
                         (c4 - np.log(k)) * k ** 4 * np.cos(4 * theta) + theta * k ** 4 * np.sin(
                     4 * theta)) + b5 * k ** 5 * np.cos(5 * theta) - d6 * k ** 6 * np.cos(
            6 * theta) + b7 * k ** 7 * np.cos(7 * theta) - b8 * (
                         (c8 - np.log(k)) * k ** 8 * np.cos(8 * theta) + theta * k ** 8 * np.sin(8 * theta))

    else:

        Xg = np.cos(theta) / k - np.cos(3 * theta) / k ** 3 + 3 * np.cos(5 * theta) - 45 * np.cos(7 * theta)

        Xg = Xg / np.sqrt(2)

    Xg = 4 * 2 * np.pi * f * 10 ** -4 * Xg

    return Xg


# 测试


if __name__ == '__main__':
    f = 50

    rou = 10 ** 6

    c_xy = conductors_coordinator

    Zgm = calc_Zgm(f, c_xy, rou)

    np.set_printoptions(precision=4, linewidth=214, suppress=True)

    print('Zgm 矩阵 : \n {}'.format(Zgm))

if __name__ == '__main__':  # 测试

    f = 2000

    rou = 10 ** 6

    c_xy = conductors_coordinator

    n = np.shape(c_xy)[0]

    for i in range(n):

        # 计算导线与大地回路电阻和电感rou=10**6

        for j in range(n):
            Dij = np.sqrt((c_xy[i, 0] - c_xy[j, 0]) ** 2 + (c_xy[i, 1] + c_xy[j, 1]) ** 2)

            xij = np.abs(c_xy[i, 0] - c_xy[j, 0])

            theta = np.arcsin(xij / Dij)

            k = 4 * np.pi * np.sqrt(5) * 10 ** -4 * Dij * np.sqrt(f / rou)

        # print(k)


def calc_Zf(f, c_xy, r, Rd, rho, mu_r, rou):  # 计算综合阻抗矩阵

    """



    :param f:     频率

    :param c_xy:  导线坐标

    :param r:     导线计算半径

    :param Rd:    导线电阻

    :param rho:   导线

    :param mu_r:  导线相对磁导率

    :param rou:   大地导电率

    :return:      阻抗矩阵

    """

    Zgm = calc_Zgm(f, c_xy, rou)  # 计算线路大地回路阻抗

    L = calc_L(c_xy, r)  # 计算线路自感与外感

    Zc = calc_Zc(f, Rd, r, mu_r, rho)  # 计算线路内阻抗

    Zf = Zgm + 1j * 2 * np.pi * f * L

    n = np.shape(c_xy)[0]

    for i in range(n):
        Zf[i, i] = Zf[i, i] + Zc[i]

    return Zf


if __name__ == '__main__':
    # 测试

    f = 50

    rou = 10 ** 6

    r = conductors_calc_radius

    c_xy = conductors_coordinator

    Zf = calc_Zf(f, c_xy, r, Rd, rho, mu_r, rou)

    print('Zf = ', Zf)


def calc_z(f, c_xy, re, Rd, rou):  # 简化计算综合阻抗矩阵

    n = np.shape(c_xy)[0]

    R = np.empty((n, n), np.float64)

    X = np.empty((n, n), np.float64)

    z = np.empty((n, n), np.complex128)

    Rg = np.pi ** 2 * f * 10 ** -4

    Dg = 660 * np.sqrt(rou / f)

    for i in range(n):  #

        for j in range(n):

            if i == j:

                R[i, j] = Rg + Rd[i]

                X[i, j] = 2 * 2 * np.pi * f * 10 ** -4 * np.log(Dg / re[i])

            else:

                dij = np.sqrt((c_xy[i, 0] - c_xy[j, 0]) ** 2 + (c_xy[i, 1] - c_xy[j, 1]) ** 2)

                R[i, j] = Rg

                X[i, j] = 2 * 2 * np.pi * f * 10 ** -4 * np.log(Dg / dij)

    z = R + 1j * X

    return R, X, z


if __name__ == '__main__':
    # 测试该函数

    f = 50

    c_xy = conductors_coordinator

    re = conductors_equivalent_radius

    rou = 10 ** 6

    R, X, z = calc_z(f, c_xy, re, Rd, rou)

    np.set_printoptions(precision=4, linewidth=214, suppress=True)

    # print('R 矩阵 : \n {}'.format(R))

    # print('X 矩阵 : \n {}'.format(X))

    print('z 矩阵 : \n {}'.format(z))


def merge_z(z, m, k):  # 阻抗矩阵归并，k导线归并到m导线

    n = np.shape(z)[0]

    for i in range(n):
        z[i, k] = z[i, k] - z[i, m]

    for i in range(n):

        for j in range(n):

            if i != k and j != k:
                z[i, j] = z[i, j] - z[i, k] / (z[k, k] - z[m, k]) * (z[k, j] - z[m, j])

    E = np.empty((n - 1, n - 1), np.complex128)

    for i in range(n):

        for j in range(n):

            if i < k:

                if j < k:
                    E[i, j] = z[i, j]

                if j > k:
                    E[i, j - 1] = z[i, j]

            if i > k:

                if j < k:
                    E[i - 1, j] = z[i, j]

                if j > k:
                    E[i - 1, j - 1] = z[i, j]

    return E


if __name__ == '__main__':
    # 测试

    f = 50

    c_xy = conductors_coordinator

    re = conductors_equivalent_radius

    rou = 10 ** 6

    R, X, z = calc_z(f, c_xy, re, Rd, rou)

    np.set_printoptions(precision=3, linewidth=214, suppress=True)

    print('阻抗矩阵z （Ω/km）: \n {}'.format(z))

    z = merge_z(z, 0, 1)

    z = merge_z(z, 1, 2)

    z = merge_z(z, 3, 4)

    z = merge_z(z, 4, 5)

    Z = np.abs(z)

    np.set_printoptions(precision=4, linewidth=214, suppress=True)

    print('阻抗矩阵z （Ω/km）: \n {}'.format(z))

    print('阻抗矩阵Z （Ω/km）: \n {}'.format(Z))


def set_connection_matrix(m, i, j):  # 设置导线横向连接矩阵，m根导线，i和j 连接

    connection_matrix = np.zeros((m, m), np.complex128)

    if i > m or j > m or i == j:

        print("connection_matrix导线标号出错")

    else:

        connection_matrix[i, i] = 1

        connection_matrix[j, j] = 1

        connection_matrix[i, j] = -1

        connection_matrix[j, i] = -1

    return connection_matrix


def set_connction_matrix_g(m, i):  # 设置导线接地矩阵，m根导线，i接地

    connection_matrix_g = np.zeros((m, m), np.complex128)

    if i >= m:

        print("connction_matrix_g导线 标号 出错")

    else:

        connection_matrix_g[i, i] = 1

    return connection_matrix_g


def set_connction_matrix_AT(m, i, j, k):  # 设置AT变压器横向连接矩阵

    connction_matrix_AT = np.zeros((m, m), np.complex128)

    connction_matrix_AT[i, i] = 0.25

    connction_matrix_AT[i, j] = -0.5

    connction_matrix_AT[i, k] = 0.25

    connction_matrix_AT[j, i] = -0.5

    connction_matrix_AT[j, j] = 1.0

    connction_matrix_AT[j, k] = -0.5

    connction_matrix_AT[k, i] = 0.25

    connction_matrix_AT[k, j] = -0.5

    connction_matrix_AT[k, k] = 0.25

    return connction_matrix_AT








