import numpy as np

from scipy import linalg

import ipynb_importer

import new_topology as tp

import conductor_calculation as cc


# 可以统一计算AT和直供，AT下有两种合并方式：6根和10根，DT下有两种4根和10根
class ChainNetwork:

    def __init__(self,

                 name="",

                 h=1,  # 基波、谐波次数。h = 1,基波；h >1 ,谐波

                 delta_length=1,  # 基本分段长度（km）

                 m=6,  # 归并后的导线数

                 topology=tp.Topology,  # 供电网络拓扑结构数据

                 ):

        self.name = name

        self.topology = topology

        self.h = h

        self.m = m

        self.section_length = self.topology.section_length  # 供电臂总长度

        self.delta_length = delta_length  # 基本分段长度

        self.n = int(np.round(self.section_length / self.delta_length) + 1)  # 分割面数，即网络节点数

        # if np.round(self.section_length / self.delta_length)<(self.section_length / self.delta_length):

        # self.n = int(np.round(self.section_length / self.delta_length) + 1)

        # else:

        # self.n = int(np.round(self.section_length / self.delta_length))

        self.distances = self.__set_distances()  # 分割点位置距离

        self.segment_lengths = self.__set_segment_lengths()  # 各分割段长度

        self.z = np.zeros((self.n - 1, self.m, self.m), np.complex128)  # 网络纵向阻抗矩阵

        self.y = np.zeros((self.n, self.m, self.m), np.complex128)  # 网络横向导纳矩阵

        self.Un = np.zeros((self.n, self.m, 1), np.complex128)  # 节点电压向量

        self.In = np.zeros((self.n - 1, self.m, 1), np.complex128)  # 纵向导线电流向量

        # self.Gn = np.zeros((self.m, 1), np.complex128)     # 节点注入电流向量

        self.Gn = np.zeros((self.m * self.n, 1), np.complex128)

        # print(self.z)

        # print(self.z.shape)

        # print(self.n)

        # print(self.Gn.shape)

        # print(self.topology.lines_system)

    def reset(self, topology, h, m, delta_length):

        self.topology = topology

        self.h = h

        self.m = m

        self.delta_length = delta_length

        self.section_length = self.topology.section_length

        self.name = self.topology.name

        self.n = int(np.round(self.section_length / self.delta_length) + 1)  # 分割面数，即网络节点

        self.distances = self.__set_distances()  # 分割点位置距离

        self.segment_lengths = self.__set_segment_lengths()  # 各分割段长度

    def __set_distances(self):

        distances = np.arange(0, self.n, 1) * self.delta_length

        distances[self.n - 1] = self.section_length

        # print(distances)

        # print('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')

        return distances

    def __set_segment_lengths(self):

        segment_lengths = np.zeros(self.n - 1, np.float64)

        segment_lengths[:self.n - 1] = self.distances[1:self.n] - self.distances[0:self.n - 1]  # 分割段长度 （km）

        # print("segment_num = ", self.segment_lengths.shape)

        # print(segment_lengths)

        # print("bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb")

        return segment_lengths

    def set_z_y(self):

        unit_z = self.__calc_unit_z()

        unit_yc = self.__calc_unit_yc()

        for i in range(self.n - 1):
            self.z[i, :, :] = unit_z * self.segment_lengths[i]

        for i in range(1, self.n - 1):
            self.y[i, :, :] = unit_yc * (self.segment_lengths[i - 1] / 2 + self.segment_lengths[i] / 2)

            self.y[0, :, :] = unit_yc * (self.segment_lengths[0] / 2)

            self.y[self.n - 1, :, :] = unit_yc * (self.segment_lengths[self.n - 2] / 2)

        # print('lllllllllllllllllllllllllllllllllllllllllllllllllllllll')

        # print("y=", self.y[0, :, :])

        # print(self.z.shape)

    def construct_M(self):

        n = self.n

        m = self.m

        Dk = np.zeros((n, m, m), np.complex128)

        Mk = np.zeros((n, m, m), np.complex128)

        M = np.zeros((m * n, m * n), np.complex128)

        for k in range(1, n):  # 生产Dk元素矩阵

            Dk[k, :, :] = -linalg.inv(self.z[k - 1, :, :])

        for k in range(1, n - 1):  # 生成Mk元素矩阵

            Mk[k, :, :] = self.y[k, :, :] + linalg.inv(self.z[k, :, :]) + linalg.inv(self.z[k - 1, :, :])

        Mk[0, :, :] = self.y[0, :, :] + linalg.inv(self.z[0, :, :])

        Mk[n - 1, :, :] = self.y[n - 1, :, :] + linalg.inv(self.z[n - 2, :, :])

        for i in range(n):

            if i == 0:

                # self.M[0:m, 0:m] = Mk[:, :, 0]

                M[0:m, 0:m] = Mk[0, :, :]

            else:

                k = i * m  # 分块起点号

                M[k:k + m, k - m:k] = Dk[i, :, :]

                M[k - m: k, k:k + m] = Dk[i, :, :]

                M[k:k + m, k:k + m] = Mk[i, :, :]

        # print(M.shape)
        # print(M)

        return M

    def solution(self):

        # self.set_z_y()

        # self.add_y()

        # #self.add_G()

        M = self.construct_M()

        W = linalg.inv(M)  ##改动

        # G = self.source()

        U = np.dot(W, self.Gn)
        # print('显示U')
        # print(U)
        # print('U显示结束')

        # Un = U.reshape(self.m, self.n)

        Un = np.zeros((self.m, self.n), np.complex128)

        for i in range(self.n):
            k = int(i) * self.m

            j = int(i + 1) * self.m

            # print(U[k:j,0].shape)

            # print(U[k:j,0])

            Un[:, i] = U[k:j, 0]

        In = np.zeros((self.m, self.n - 1), np.complex128)  #

        for k in range(self.n - 1):

            z = self.z[k, :, :]

            z = linalg.inv(z)

            u = Un[:, k] - Un[:, k + 1]

            # print(u)

            u = np.mat(u)

            # print(u.shape)

            u = u.T

            # print(u)

            Ini = np.dot(z, u)

            Ini = np.mat(Ini)

            Ini = Ini.T
            # print('Ini的大小')
            # print(Ini.shape)

            for j in range(0, self.m, 1):
                In[j:, k] = Ini[0, j]

            # print('显示In的大小')
            # print(In.shape)
            # print('显示Un')
            # print(Un)
            # print('显示In')
            # print(In[:,1])
            # print('结束')

        return Un, In

    def add_y(self):

        # 添加各种横向元件，包括横向连接线、AT、牵引变压器等

        if self.m == 6:

            y_e1_g = cc.set_connction_matrix_g(self.m, 2)  # 综合地线e1连接大地g ，导纳关联矩阵

            y_e2_g = cc.set_connction_matrix_g(self.m, 5)  # 综合地线e2连接大地g ，导纳关联矩

            y_ra1_g = cc.set_connction_matrix_g(self.m, 1)  # 钢轨ra1连接大地g, 导纳关联矩阵

            y_ra3_g = cc.set_connction_matrix_g(self.m, 4)  # 钢轨ra3连接大地g, 导纳关联矩阵

            y_e1_ra1 = cc.set_connection_matrix(self.m, 1, 2)  # 钢轨ra1连接综合地线e1,导纳关联矩阵

            y_e2_ra3 = cc.set_connection_matrix(self.m, 4, 5)  # 钢轨ra2连接综合地线e2,导纳关联矩阵

            cross_connections = self.topology.cross_connections[0]

            y0 = 10 ** 8  # 连接导线的电导率

            for x in cross_connections.ra1_g:

                k = int(np.round(x / self.delta_length))

                if k < self.n:
                    rg = cross_connections.ra1_g.get(x)

                    # print('rg')
                    # print(rg)

                    self.y[k, :, :] = self.y[k, :, :] + y_ra1_g * (1 / rg)

            for x in cross_connections.ra3_g:

                k = int(np.round(x / self.delta_length))

                if k < self.n:
                    rg = cross_connections.ra3_g.get(x)

                    self.y[k, :, :] = self.y[k, :, :] + y_ra3_g * (1 / rg)

            for x in cross_connections.e1_g:

                k = int(np.round(x / self.delta_length))

                if k < self.n:
                    rg = cross_connections.e1_g.get(x)

                    self.y[k, :, :] = self.y[k, :, :] + y_e1_g * (1 / rg)

            for x in cross_connections.e2_g:

                k = int(np.round(x / self.delta_length))

                if k < self.n:
                    rg = cross_connections.e2_g.get(x)

                    self.y[k, :, :] = self.y[k, :, :] + y_e2_g * (1 / rg)

            for x in cross_connections.e1_ra1:

                k = int(np.round(x / self.delta_length))

                if k < self.n:
                    self.y[k, :, :] = self.y[k, :, :] + y_e1_ra1 * y0

            for x in cross_connections.e2_ra3:

                k = int(np.round(x / self.delta_length))

                if k < self.n:
                    self.y[k, :, :] = self.y[k, :, :] + y_e2_ra3 * y0

            if self.topology.lines_system == "AT":

                # print("yes")
                AT_matrix = cc.set_connction_matrix_AT(self.m, 0, 2, 1)

                ATs = self.topology.auto_transformers

                ATs_location = []

                ATs_num = len(ATs)

                for i in range(len(ATs)):
                    ATs_location.append(ATs[i].location)

                for i in range(ATs_num):

                    k = int(np.round(ATs_location[i] / self.delta_length))

                    if k < self.n:
                        self.y[k, :, :] = self.y[k, :, :] + AT_matrix * (
                                    1 / (ATs[i].zs * self.h))  # yg为折算至中点的漏导纳   ATs[i].zs

        if self.m == 10:

            y_e1_g = cc.set_connction_matrix_g(self.m, 4)  # 综合地线e1连接大地g ，导纳关联矩阵

            y_e2_g = cc.set_connction_matrix_g(self.m, 9)  # 综合地线e2连接大地g ，导纳关联矩

            y_ra1_g = cc.set_connction_matrix_g(self.m, 2)  # 钢轨ra1连接大地g, 导纳关联矩阵

            y_ra3_g = cc.set_connction_matrix_g(self.m, 7)  # 钢轨ra3连接大地g, 导纳关联矩阵

            y_e1_ra1 = cc.set_connection_matrix(self.m, 2, 4)  # 钢轨ra1连接综合地线e1,导纳关联矩阵

            y_e2_ra3 = cc.set_connection_matrix(self.m, 7, 9)  # 钢轨ra2连接综合地线e2,导纳关联矩阵

            cross_connections = self.topology.cross_connections[0]

            y0 = 10 ** 8  # 连接导线的电导率

            for x in cross_connections.ra1_g:

                k = int(np.round(x / self.delta_length))

                if k < self.n:
                    rg = cross_connections.ra1_g.get(x)

                    # print('rg')
                    # print(rg)

                    self.y[k, :, :] = self.y[k, :, :] + y_ra1_g * (1 / rg)

            for x in cross_connections.ra3_g:

                k = int(np.round(x / self.delta_length))

                if k < self.n:
                    rg = cross_connections.ra3_g.get(x)

                    self.y[k, :, :] = self.y[k, :, :] + y_ra3_g * (1 / rg)

            for x in cross_connections.e1_g:

                k = int(np.round(x / self.delta_length))

                if k < self.n:
                    rg = cross_connections.e1_g.get(x)

                    self.y[k, :, :] = self.y[k, :, :] + y_e1_g * (1 / rg)

            for x in cross_connections.e2_g:

                k = int(np.round(x / self.delta_length))

                if k < self.n:
                    rg = cross_connections.e2_g.get(x)

                    self.y[k, :, :] = self.y[k, :, :] + y_e2_g * (1 / rg)

            for x in cross_connections.e1_ra1:

                k = int(np.round(x / self.delta_length))

                if k < self.n:
                    self.y[k, :, :] = self.y[k, :, :] + y_e1_ra1 * y0

            for x in cross_connections.e2_ra3:

                k = int(np.round(x / self.delta_length))

                if k < self.n:
                    self.y[k, :, :] = self.y[k, :, :] + y_e2_ra3 * y0

            if self.topology.lines_system == "AT":
                AT_matrix = cc.set_connction_matrix_AT(self.m, 0, 2, 1)

                ATs = self.topology.auto_transformers

                ATs_location = []

                ATs_num = len(ATs)

                for i in range(len(ATs)):
                    ATs_location.append(ATs[i].location)

                for i in range(ATs_num):

                    k = int(np.round(ATs_location[i] / self.delta_length))

                    if k < self.n:
                        self.y[k, :, :] = self.y[k, :, :] + AT_matrix * (
                                    1 / (ATs[i].zs * self.h))  # yg为折算至中点的漏导纳   ATs[i].zs

        if self.m == 4:

            y_e1_g = cc.set_connction_matrix_g(self.m, 1)  # 综合地线e1连接大地g ，导纳关联矩阵

            y_e2_g = cc.set_connction_matrix_g(self.m, 3)  # 综合地线e2连接大地g ，导纳关联矩

            y_ra1_g = cc.set_connction_matrix_g(self.m, 1)  # 钢轨ra1连接大地g, 导纳关联矩阵

            y_ra3_g = cc.set_connction_matrix_g(self.m, 3)  # 钢轨ra3连接大地g, 导纳关联矩阵

            # y_e1_ra1 = dscc.set_connection_matrix(self.m, 2, 4) #钢轨ra1连接综合地线e1,导纳关联矩阵

            # y_e2_ra3 = dscc.set_connection_matrix(self.m, 7, 9) #钢轨ra2连接综合地线e2,导纳关联矩阵

            cross_connections = self.topology.cross_connections[0]

            y0 = 10 ** 8  # 连接导线的电导率

            for x in cross_connections.ra1_g:

                k = int(np.round(x / self.delta_length))

                if k < self.n:
                    rg = cross_connections.ra1_g.get(x)

                    # print('rg')
                    # print(rg)

                    self.y[k, :, :] = self.y[k, :, :] + y_ra1_g * (1 / rg)

            for x in cross_connections.ra3_g:

                k = int(np.round(x / self.delta_length))

                if k < self.n:
                    rg = cross_connections.ra3_g.get(x)

                    self.y[k, :, :] = self.y[k, :, :] + y_ra3_g * (1 / rg)

            for x in cross_connections.e1_g:

                k = int(np.round(x / self.delta_length))

                if k < self.n:
                    rg = cross_connections.e1_g.get(x)

                    self.y[k, :, :] = self.y[k, :, :] + y_e1_g * (1 / rg)

            for x in cross_connections.e2_g:

                k = int(np.round(x / self.delta_length))

                if k < self.n:
                    rg = cross_connections.e2_g.get(x)

                    self.y[k, :, :] = self.y[k, :, :] + y_e2_g * (1 / rg)

        traction = self.topology.traction_transformer

        if self.m == 10:
            self.y[0, 0, 0] = (1 / (1j * traction[0].zs * self.h)) + self.y[0, 0, 0]  # zs为牵引变压器内阻抗    traction[0].zs

            self.y[0, 2, 0] = - (1 / (1j * traction[0].zs * self.h)) + self.y[0, 2, 0]

            self.y[0, 0, 2] = - (1 / (1j * traction[0].zs * self.h)) + self.y[0, 0, 2]

            self.y[0, 2, 2] = (1 / (1j * traction[0].zs * self.h)) + self.y[0, 2, 2]

            self.y[0, 3, 0] = - (1 / (1j * traction[0].zs * self.h)) + self.y[0, 3, 0]

            self.y[0, 0, 3] = - (1 / (1j * traction[0].zs * self.h)) + self.y[0, 0, 3]

            self.y[0, 3, 3] = (1 / (1j * traction[0].zs * self.h)) + self.y[0, 3, 3]

            self.y[0, 0, 0] = self.y[0, 0, 0] + 10 ** 8

            self.y[0, 5, 0] = self.y[0, 5, 0] - 10 ** 8

            self.y[0, 0, 5] = self.y[0, 0, 5] - 10 ** 8

            self.y[0, 5, 5] = self.y[0, 5, 5] + 10 ** 8

            self.y[0, 2, 2] = self.y[0, 2, 2] + 10 ** 8

            self.y[0, 2, 7] = self.y[0, 2, 7] - 10 ** 8

            self.y[0, 7, 2] = self.y[0, 7, 2] - 10 ** 8

            self.y[0, 7, 7] = self.y[0, 7, 7] + 10 ** 8

            self.y[0, 3, 3] = self.y[0, 3, 3] + 10 ** 8

            self.y[0, 3, 8] = self.y[0, 3, 8] - 10 ** 8

            self.y[0, 8, 3] = self.y[0, 8, 3] - 10 ** 8

            self.y[0, 8, 8] = self.y[0, 8, 8] + 10 ** 8

        if self.m == 6:
            self.y[0, 0, 0] = (1 / (1j * traction[0].zs * self.h)) + self.y[0, 0, 0]  # zs为牵引变压器内阻抗    traction[0].zs

            self.y[0, 1, 0] = - (1 / (1j * traction[0].zs * self.h)) + self.y[0, 1, 0]

            self.y[0, 0, 1] = - (1 / (1j * traction[0].zs * self.h)) + self.y[0, 0, 1]

            self.y[0, 1, 1] = (1 / (1j * traction[0].zs * self.h)) + self.y[0, 1, 1]

            self.y[0, 0, 0] = 10 ** 8 + self.y[0, 0, 0]

            self.y[0, 0, 3] = - 10 ** 8 + self.y[0, 0, 3]

            self.y[0, 3, 0] = - 10 ** 8 + self.y[0, 3, 0]

            self.y[0, 3, 3] = 10 ** 8 + self.y[0, 3, 3]

            self.y[0, 1, 1] = (10 ** 8) + self.y[0, 1, 1]

            self.y[0, 1, 4] = - 10 ** 8 + self.y[0, 1, 4]

            self.y[0, 4, 1] = - 10 ** 8 + self.y[0, 4, 1]

            self.y[0, 4, 4] = 10 ** 8 + self.y[0, 4, 4]

        if self.m == 4:
            self.y[0, 0, 0] = (1 / (1j * traction[0].zs * self.h)) + self.y[0, 0, 0]  # zs为牵引变压器内阻抗    traction[0].zs

            self.y[0, 1, 0] = - (1 / (1j * traction[0].zs * self.h)) + self.y[0, 1, 0]

            self.y[0, 0, 1] = - (1 / (1j * traction[0].zs * self.h)) + self.y[0, 0, 1]

            self.y[0, 1, 1] = (1 / (1j * traction[0].zs * self.h)) + self.y[0, 1, 1]

        #
        return self.y

    def __get_line_parameter(self):  # 获取导线参数

        c_xy = []

        c_resistance = []

        c_mu_r = []

        c_radius = []

        c_equivalent_radius = []

        c_rho = []

        earth_rou = self.topology.earth_rou

        for line in self.topology.lines:
            c_xy.append([line.coordinater_x, line.coordinater_y])

            c_resistance.append(line.resistance)

            c_mu_r.append(line.mu_r)

            c_radius.append(line.radius)

            c_equivalent_radius.append(line.equivalent_radius)

            c_rho.append(line.rho)

        return c_xy, earth_rou, c_resistance, c_mu_r, c_radius, c_equivalent_radius, c_rho

    def __get_line_parameter_test(self):  # 设定测试导线参数

        c_xy = cc.conductors_coordinator

        c_resistance = cc.Rd

        c_mu_r = cc.mu_r

        c_radius = cc.conductors_calc_radius

        c_equivalent_radius = cc.conductors_equivalent_radius

        c_rho = cc.rho

        earth_rou = self.topology.earth_rou

        return c_xy, earth_rou, c_resistance, c_mu_r, c_radius, c_equivalent_radius, c_rho

    def __calc_unit_z(self):

        """

        计算平行导线原始单位阻抗矩阵

        :return:     阻抗矩阵

        """

        c_xy, earth_rou, c_resistance, c_mu_r, c_radius, c_equivalent_radius, c_rho = self.__get_line_parameter_test()

        f = 50 * self.h  # 频率

        z = cc.calc_Zf(f, c_xy, c_radius, c_resistance, c_rho, c_mu_r, earth_rou)

        if self.m == 6:
            z = cc.merge_z(z, 0, 1)

            z = cc.merge_z(z, 2, 3)

            z = cc.merge_z(z, 2, 3)

            z = cc.merge_z(z, 2, 3)

            z = cc.merge_z(z, 3, 4)

            z = cc.merge_z(z, 5, 6)

            z = cc.merge_z(z, 5, 6)

            z = cc.merge_z(z, 5, 6)

            Z = np.abs(z)

        # print("**************************************************************************")

        # print(abs(unit_z))
        # print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        if self.m == 4:
            z = cc.merge_z(z, 0, 1)

            z = cc.merge_z(z, 1, 2)

            z = cc.merge_z(z, 1, 2)

            z = cc.merge_z(z, 2, 3)

            z = cc.merge_z(z, 3, 4)

            z = cc.merge_z(z, 3, 4)

        if self.m == 10:
            z = cc.merge_z(z, 0, 1)

            z = cc.merge_z(z, 2, 3)

            z = cc.merge_z(z, 5, 6)

            z = cc.merge_z(z, 7, 8)

        unit_z = z

        return unit_z

    def __calc_unit_yc(self):

        """

        计算导线的单位电容导纳矩阵

        :return:

        """

        c_xy, earth_rou, c_resistance, c_mu_r, c_radius, c_equivalent_radius, c_rho = self.__get_line_parameter_test()

        p = cc.calc_potential_coefficient(c_xy, c_radius)

        if self.m == 6:
            p = cc.merge_potential_coefficient(p, 0, 1)  # 合并成8根导线

            p = cc.merge_potential_coefficient(p, 2, 3)

            p = cc.merge_potential_coefficient(p, 2, 3)

            p = cc.merge_potential_coefficient(p, 2, 3)

            p = cc.merge_potential_coefficient(p, 3, 4)

            p = cc.merge_potential_coefficient(p, 5, 6)

            p = cc.merge_potential_coefficient(p, 5, 6)

            p = cc.merge_potential_coefficient(p, 5, 6)

        if self.m == 4:
            p = cc.merge_potential_coefficient(p, 0, 1)  # 合并成4根导线

            p = cc.merge_potential_coefficient(p, 1, 2)

            p = cc.merge_potential_coefficient(p, 1, 2)

            p = cc.merge_potential_coefficient(p, 2, 3)

            p = cc.merge_potential_coefficient(p, 3, 4)

            p = cc.merge_potential_coefficient(p, 3, 4)

        if self.m == 10:
            p = cc.merge_potential_coefficient(p, 0, 1)  # 合并成4根导线

            p = cc.merge_potential_coefficient(p, 2, 3)

            p = cc.merge_potential_coefficient(p, 5, 6)

            p = cc.merge_potential_coefficient(p, 7, 8)

        b = cc.calc_B(p)  # 计算电容

        f = 50 * self.h

        # print("[[[[[[[[]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]")

        unit_yc = 1j * 2 * np.pi * f * b  # 计算电容导纳

        # print(unit_yc)

        # print("***********0000000000****************************************************")

        # print(abs(unit_yc))

        # print(unit_yc.shape)

        # print('**************************=============------------------------------')
        return unit_yc

    def source(self):

        # print(G.shape)

        # print(type(GG))

        ##电源

        if self.m == 6:
            traction = self.topology.traction_transformer

            self.Gn[0][0] = 27500 / (1j * traction[0].zs * self.h)

            self.Gn[1][0] = -27500 / (1j * traction[0].zs * self.h)

        if self.m == 10:
            traction = self.topology.traction_transformer

            self.Gn[1][0] = 27500 / (1j * traction[0].zs * self.h)

            self.Gn[2][0] = -27500 / (1j * traction[0].zs * self.h)

            self.Gn[3][0] = -27500 / (1j * traction[0].zs * self.h)

        if self.m == 4:
            traction = self.topology.traction_transformer

            self.Gn[1][0] = 27500 / (1j * traction[0].zs * self.h)

            self.Gn[2][0] = -27500 / (1j * traction[0].zs * self.h)

        return self.Gn

    def locomotives(self):

        locomotives = self.topology.locomotive

        locomotives_location = []

        locomotives_load = []

        locomotives_num = len(locomotives)

        for i in range(len(locomotives)):
            locomotives_location.append(locomotives[i].location)

            locomotives_load.append(locomotives[i].load)

        for i in range(locomotives_num):

            k = int(np.round(locomotives_location[i] / self.delta_length))

            if k < self.n:

                if self.m == 6:
                    self.Gn[k * self.m][0] = -1 * locomotives_load[i]

                    self.Gn[k * self.m + 1][0] = locomotives_load[i]  # locomotives_load[i]

                if self.m == 10:
                    self.Gn[k * self.m + 1][0] = -1 * locomotives_load[i]

                    self.Gn[k * self.m + 2][0] = locomotives_load[i]

                    self.Gn[k * self.m + 3][0] = locomotives_load[i]

                if self.m == 4:
                    self.Gn[k * self.m][0] = -1 * locomotives_load[i]

                    self.Gn[k * self.m + 1][0] = locomotives_load[i]  # locomotives_load[i]

                # In[:, k] = In[:, k] + Ini

            # G = G.T

            # G = np.mat(G)

        return self.Gn

# if __name__ == '__main__':


#     chen = ChainNetwork(h=1, m=6, delta_length=0.5)

#     chen.set_z_y()


#     YY = chen.add_y_source()

#     #print(YY.shape)


#     chen.add_y()

#     R = chen.source()

#     #print(R)

#     print(R.shape)

#     #print(chen.construct_M().shape)
#     print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
#     chen.locomotives()

#     #print(Q)

#     # print(chen.AT_matrix_6)

#     # print(chen.y6_to_all)

#     # print(chen.y6_e1_g)

#     #print(Q)

#     #print(Q.shape)
#     #print(Q)

#     #print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')

#     Q = chen.construct_M()
#     #print(Q)
#     #print(Q.shape)
#     #print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')

#     UU,II = chen.solution()
#     print('UU**********************************************************55555555555555555555555555')
#     print(UU)
#     print('II*************************************************************55555555555555555555555555')
#     print(II)
#     #print('*************************************************************55555555555555555555555555')
#     #print(UU.shape)

#     #print(II.shape)
#     #print('电流矩阵')
#     #print(II)
#     #print(chen.delta_length)