import numpy as np
import new_topology as tp
import calculation as ca
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

font_set = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=10)


class ChainNetwork_impel(ca.ChainNetwork):
    # def __init__(self,name="",h=1,delta_length=1,m=6,topology=tp.Topology(name="AT_System"):
    def __init__(self, name="", h=1, delta_length=1, m=6, topology=tp.Topology("测试供电臂"), ):
        super().__init__(name, h, delta_length, m, topology)

    def impel(self,impel_index):

        impel = self.topology.locomotive

        impel_num = len(impel)

        impel_locations = []  # 所有激励的位置
        for i in range(impel_num):
            # print(topology.locomotive[i].harmonic,topology.locomotive[i].name,topology.locomotive[i].load,topology.locomotive[i].location)
            impel_locations.append(impel[i].location)
        for i in impel_locations:
            k = int(np.round(i / self.delta_length))

            if k < self.n:
                self.Gn[k * self.m][0] = -1

                self.Gn[k * self.m + 1][0] = 1

        # print(self.Gn)
        # return self.Gn

class simple_harmonic_U:#每次谐波下的电压
    def __init__(self,
                 order = 0,#谐波次数
                 value = [],#该次谐波下的电压值
                 ):
        self.order = order
        self.value = value
class simple_harmonic_I:#每次谐波下的电流
    def __init__(self,

                 order = 0,#谐波次数
                 value = [],#该次谐波下的电流值
                 ):
        self.order = order
        self.value = value

class harmonic_calculation:
    def __init__(self,

                 num=99,  # 最大谐波次数。2~num次

                 U = [],#各次谐波的电压

                 I = [],#各次谐波下电流

                 U_MAX = [],#各次谐波下的最大电压

                 I_MAX = [],#各次谐波下的最大电流

                 topology = tp.Topology, #读取topology信息

                 chainnetwork = ChainNetwork_impel,
                 ):

        self.num = num

        self.U = U

        self.I = I

        self.U_MAX = U_MAX

        self.I_MAX = I_MAX

        self.topology = topology

        self.chainnetwork = chainnetwork
        
    def __set_impel_location(self):

        self.topology = tp.Topology(name="测试供电臂")
        #############################################################################################
        self.topology.set_topology(db_file_name="DT-system.db")
        ##########激励位置#############################################
        impel_locations = []  # 所有激励位置
        for i in range(1):
            impel_locations.append(self.topology.locomotive[i].location)

        return impel_locations

###############谐波电流电压#################################################################
    def harmonic_solution(self,m=4):
        impel_locations = self.__set_impel_location()
        for i in range(len(impel_locations)):
            for l in range(2, self.num):
                chen = ChainNetwork_impel(l, m=4, delta_length=0.5)
                chen.reset(self.topology, l, 4, 0.5)
                chen.impel(i)
                #print('[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]')
                chen.set_z_y()

                chen.add_y()

                chen.construct_M()
                U, I = chen.solution()

                simple_U = np.zeros((U.shape[0], U.shape[1]), np.float64)
                simple_I= np.zeros((I.shape[0], I.shape[1]), np.float64)
                for i in range(simple_U.shape[0]):
                    for j in range(simple_U.shape[1]):
                        simple_U[i][j] = abs(U[i][j])

                for i in range(I.shape[0]):
                    for j in range(I.shape[1]):
                        simple_I[i][j] = abs(I[i][j])

                self.U.append(simple_U)
                self.I.append(simple_I)

                if self.topology.lines_system == 'AT':
                    simple_harmonic_U_MAX = np.zeros((m, 1))
                    simple_harmonic_I_MAX = np.zeros((m, 1))
                    for i in range(0,m):
                        ##找电流电压最大值#######################
                        temp_U = self.U[l-2][i, :].tolist()
                        for j in range(0, len(temp_U)):
                            for k in range(j + 1, len(temp_U)):
                                first = int(abs(temp_U[i]))
                                second = int(abs(temp_U[j]))
                                if first < second:
                                    temp_U[i] = temp_U[j]
                                    temp_U[j] = first
                        temp_U_MAX = temp_U[0]
                        simple_harmonic_U_MAX[i][0] = temp_U_MAX

                        temp_I = self.I[l-2][i, :].tolist()
                        for j in range(0, len(temp_I)):
                            for k in range(j + 1, len(temp_I)):
                                first = int(abs(temp_I[i]))
                                second = int(abs(temp_I[j]))
                                if first < second:
                                    temp_I[i] = temp_I[j]
                                    temp_I[j] = first
                        temp_I_MAX = temp_I[0]
                        simple_harmonic_I_MAX[i][0] = temp_I_MAX
                    self.I_MAX.append(simple_harmonic_I_MAX)
                    self.U_MAX.append(simple_harmonic_U_MAX)
                elif self.topology.lines_system == 'DT':
                    simple_harmonic_U_MAX = np.zeros((m, 1))
                    simple_harmonic_I_MAX = np.zeros((m, 1))
                    ##找电流电压最大值#######################
                    for i in range(0, m):
                        temp_U = self.U[l-2][i, :].tolist()
                        for j in range(0, len(temp_U)):
                            for k in range(j + 1, len(temp_U)):
                                first = int(abs(temp_U[i]))
                                second = int(abs(temp_U[j]))
                                if first < second:
                                    temp_U[i] = temp_U[j]
                                    temp_U[j] = first
                        temp_U_MAX = temp_U[0]
                        simple_harmonic_U_MAX[i][0] = temp_U_MAX

                        temp_I = self.I[l-2][i, :].tolist()
                        for j in range(0, len(temp_I)):
                            for k in range(j + 1, len(temp_I)):
                                first = int(abs(temp_I[i]))
                                second = int(abs(temp_I[j]))
                                if first < second:
                                    temp_I[i] = temp_I[j]
                                    temp_I[j] = first
                        temp_I_MAX = temp_I[0]
                        simple_harmonic_I_MAX[i][0] = temp_I_MAX
                    self.I_MAX.append(simple_harmonic_I_MAX)
                    self.U_MAX.append(simple_harmonic_U_MAX)
    def plotting(self,line_model="",m=4,h=2,delta_length=0.5,supply_model="",total=0):
        if total == 0:  #total=0为h次谐波下某根导线上的电流电压特性曲线图；=1为2~n次谐波下某根导线最大电流电压特性曲线

            if m == 6:
                if line_model == "上行接触线":
                    i = 0
                elif line_model == "上行馈线":
                    i = 1
                elif line_model == "上行钢轨":
                    i = 2
                elif line_model == "下行接触线":
                    i = 3
                elif line_model == "下行馈线":
                    i = 4
                elif line_model == "下行钢轨":
                    i = 5
            elif m == 4:
                if line_model == "上行接触线":
                    i = 0
                elif line_model == "上行钢轨":
                    i = 1
                elif line_model == "下行接触线":
                    i = 2
                elif line_model == "下行钢轨":
                    i = 3
            elif m == 10:
                if line_model == "上行接触线":
                    i == 0
                elif line_model == "上行馈线":
                    i == 1
                elif line_model == "上行钢轨":
                    i == 2
                elif line_model == "上行保护线":
                    i == 3
                elif line_model == "上行综合地线":
                    i == 4
                elif line_model == "上行接触线":
                    i == 5
                elif line_model == "上行馈线":
                    i == 6
                elif line_model == "上行钢轨":
                    i == 7
                elif line_model == "上行保护线":
                    i == 8
                elif line_model == "上行综合地线":
                    i == 9
            elif m == 4:
                if line_model == "上行接触线":
                    i == 0
                elif line_model == "上行钢轨":
                    i == 1
                elif line_model == "下行接触线":
                    i == 2
                elif line_model == "下行钢轨":
                    i == 3
            #绘制某次谐波下的电流特性曲线
            Distances = ChainNetwork_impel(h, m, delta_length).distances
            plt.plot(Distances[:-1].tolist(), self.I[h-2][i, :].tolist(), color='red')
            plt.title(u'' +supply_model+ str(h) + '次谐波下'+line_model+'电流特性曲线', fontproperties=font_set)
            plt.xlabel(u'距离h', fontproperties=font_set)
            plt.ylabel(u''+line_model+'电流i(A)', fontproperties=font_set)
            plt.show()

            plt.plot(Distances.tolist(), self.U[h-2][i, :].tolist(), color='red')
            plt.title(u'' + supply_model + str(h) + '次谐波下' + line_model + '电压特性曲线', fontproperties=font_set)
            plt.xlabel(u'距离h', fontproperties=font_set)
            plt.ylabel(u'' + line_model + '电压u(V)', fontproperties=font_set)
            plt.show()

        else:
            harmonic_num = []
            for i in range(2, self.num):
                harmonic_num.append(i)
            if m == 6:
                if line_model == "上行接触线":
                    i = 0
                elif line_model == "上行馈线":
                    i = 1
                elif line_model == "上行钢轨":
                    i = 2
                elif line_model == "下行接触线":
                    i = 3
                elif line_model == "下行馈线":
                    i = 4
                elif line_model == "下行钢轨":
                    i = 5
            elif m == 4:
                if line_model == "上行接触线":
                    i = 0
                elif line_model == "上行钢轨":
                    i = 1
                elif line_model == "下行接触线":
                    i = 2
                elif line_model == "下行钢轨":
                    i = 3
            elif m == 10:
                if line_model == "上行接触线":
                    i == 0
                elif line_model == "上行馈线":
                    i == 1
                elif line_model == "上行钢轨":
                    i == 2
                elif line_model == "上行保护线":
                    i == 3
                elif line_model == "上行综合地线":
                    i == 4
                elif line_model == "上行接触线":
                    i == 5
                elif line_model == "上行馈线":
                    i == 6
                elif line_model == "上行钢轨":
                    i == 7
                elif line_model == "上行保护线":
                    i == 8
                elif line_model == "上行综合地线":
                    i == 9
            elif m == 4:
                if line_model == "上行接触线":
                    i == 0
                elif line_model == "上行钢轨":
                    i == 1
                elif line_model == "下行接触线":
                    i == 2
                elif line_model == "下行钢轨":
                    i == 3
            temp_simple_U_MAX = []
            temp_simple_I_MAX = []
            for j in range(len(self.U_MAX)):
                temp_simple_U_MAX.append(self.U_MAX[j][i][0])
                temp_simple_I_MAX.append(self.I_MAX[j][i][0])
            plt.plot(harmonic_num, temp_simple_U_MAX, color='red')
            plt.title(u''+line_model + '2~' + str(self.num) + '次不同次数谐波下接触线最大电压特性曲线', fontproperties=font_set)
            plt.xlabel(u'谐波次数h', fontproperties=font_set)
            plt.ylabel(u''+line_model+'最大电压u(V)', fontproperties=font_set)
            plt.show()

            plt.plot(harmonic_num, temp_simple_I_MAX, color='red')
            plt.title(u'' + line_model + '2~' + str(self.num) + '次不同次数谐波下接触线最大电流特性曲线', fontproperties=font_set)
            plt.xlabel(u'谐波次数h', fontproperties=font_set)
            plt.ylabel(u'' + line_model + '最大电流i(A)', fontproperties=font_set)
            plt.show()

if __name__ == '__main__':

    wei = harmonic_calculation()

    wei.harmonic_solution(m=4)
    wei.plotting(line_model="上行接触线",m=4,h=75,delta_length = 0.5,supply_model="直供",total=0)
    wei.plotting(line_model="上行接触线",m=4,h=75,delta_length = 0.5,supply_model="直供",total=1)