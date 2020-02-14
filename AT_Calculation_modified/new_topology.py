from sqlite3 import connect
import pandas as pd
import numpy as np


# encoding=utf-8

class Line:
    def __init__(self,
                 name="",  # 导线名
                 type_name="",  # 导线型号名
                 resistance=0,  # 导线电阻
                 radius=1,  # 导线计算半径
                 equivalent_radius=1,  # 导线等效半径
                 rho=1,  # 导线电导率
                 mu_r=1,  # 相对磁导率
                 coordinate_x=0,  # 导线坐标 x
                 coordinate_y=0):  # 导线坐标 y
        self.name = name
        self.type_name = type_name
        self.resistance = resistance
        self.radius = radius
        self.rho = rho
        self.mu_r = mu_r
        self.equivalent_radius = equivalent_radius
        self.coordinate_x = coordinate_x
        self.coordinate_y = coordinate_y

    def set_parameter(self,
                      resistance=0,
                      radius=1,
                      equivalent_radius=1,
                      rho=1,
                      mu_r=1,
                      coordinate_x=0,
                      coordinate_y=0
                      ):
        self.resistance = resistance
        self.radius = radius
        self.rho = rho
        self.mu_r = mu_r
        self.equivalent_radius = equivalent_radius
        self.coordinate_x = coordinate_x
        self.coordinate_y = coordinate_y


# class ATLines:
#     lines_type = "AT System"

#     def __init__(self,
#                  name="",lines_type=""
#                  ):
#         self.name = name
#         self.lines_type = lines_type
#         self.lines = []
#     def set_lines(self):
#         if self.lines_type == "AT System":
#             self.lines.append(Line(name="cw1"))
#             self.lines.append(Line(name="mw1"))
#             self.lines.append(Line(name="pf1"))
#             self.lines.append(Line(name="ra1"))
#             self.lines.append(Line(name="ra2"))
#             self.lines.append(Line(name="pw1"))
#             self.lines.append(Line(name="e1"))
#             self.lines.append(Line(name="cw2"))
#             self.lines.append(Line(name="mw2"))
#             self.lines.append(Line(name="pf2"))
#             self.lines.append(Line(name="ra3"))
#             self.lines.append(Line(name="ra4"))
#             self.lines.append(Line(name="pw2"))
#             self.lines.append(Line(name="e2"))
#         else:
#             self.lines.append(Line(name="cw1"))
#             self.lines.append(Line(name="mw1"))
#             self.lines.append(Line(name="ra1"))
#             self.lines.append(Line(name="ra2"))
#             self.lines.append(Line(name="e1"))
#             self.lines.append(Line(name="cw2"))
#             self.lines.append(Line(name="mw2"))
#             self.lines.append(Line(name="ra3"))
#             self.lines.append(Line(name="ra4"))
#             self.lines.append(Line(name="e2"))
# #class DTlines:
#     lines_type = "DT System"

#     def __init__(self,name=""):
#         self.name = name
#         self.lines = []
#         self.lines.append(Line(name="cw1"))
#         self.lines.append(Line(name="mw1"))
#         self.lines.append(Line(name="ra1"))
#         self.lines.append(Line(name="ra2"))
#         self.lines.append(Line(name="e1"))
#         self.lines.append(Line(name="cw2"))
#         self.lines.append(Line(name="mw2"))
#         self.lines.append(Line(name="ra3"))
#         self.lines.append(Line(name="ra4"))
#         self.lines.append(Line(name="e2"))
#  def __setattr__(self, file_name=""):
# for line in lines:
#     pass
# def set_accodinater(self):
#        pass


# if __name__ == '__main__':


class TractionTransformer:  # 牵引变压器类
    def __init__(self,
                 name="",
                 alias_name="",  # 牵引变压器型号
                 zs=1 + 1j,  # 系统内阻抗
                 location=0,  # 安装位置（公里)

                 ):
        self.name = name
        self.alias_name = alias_name
        self.zs = zs
        self.location = location


class AutoTransformer:  # 自耦变压器类
    def __init__(self,
                 name="",
                 alias_name="",  # 变压器型号
                 zs=1 + 1j,  # 漏抗（欧）
                 location=0  # 安装位置(公里）
                 ):
        self.name = name
        self.alias_name = alias_name
        self.zs = zs
        self.location = location


class Locomotive:  # 机车类
    def __init__(self,
                 name="",  #
                 load=0,  # 负荷电流（安 ,A）
                 harmonic={},  # 谐波含量 （fn, %）
                 location=0,  # 运行位置 （公里，km）
                 at_upline=1  # 位于上行线=1；位于下行线=0
                 ):
        self.name = name
        self.load = load
        self.harmonic = harmonic
        self.location = location
        self.at_upline = at_upline


class CrossConnection:
    """
    """

    def __init__(self,
                 name="",
                 ):
        self.name = name
        self.to_all = []  # 上下行全并联，( km）
        self.e1_ra1 = []  # 综合地线e1连接钢轨ra1，( km）
        self.e1_g = {}  # 综合地线e1连接大地g ，{ km, 欧}
        self.e2_ra3 = []  # 综合地线e2连接钢轨ra3，( km）
        self.e2_g = {}  # 综合地线e2连接大地g，{ km, 欧}
        self.ra1_g = {}  # 钢轨ra1连接大地g
        self.ra3_g = {}  # 钢轨ra3连接大地g


class Topology:
    def __init__(self,
                 name="",
                 alias_name="",
                 section_length=30.6,
                 earth_rou=10 ** 6,
                 traction_transformer=[],
                 lines=[],
                 cross_connections=[],
                 auto_transformers=[],
                 locomotive=[],
                 lines_system=[]
                 ):
        self.name = name
        self.alias_name = alias_name
        self.section_length = section_length
        self.earth_rou = earth_rou
        self.traction_transformer = traction_transformer
        self.lines = lines
        self.cross_connections = cross_connections
        self.auto_transformers = auto_transformers
        self.locomotive = locomotive
        self.lines_system = lines_system

    def set_topology(self,
                     db_file_name="default.db"  # 系统拓扑结构 sqlite数据库文件名
                     ):
        con = connect(db_file_name)  # 取得数据库连接对象
        cur = con.cursor()  # 取得数据库游标对象

        # 确定系统类型
        sqlcom_linetype = 'select mode from base'  # 系统类型
        df1_sqlcom_linetype = pd.read_sql(sqlcom_linetype, con)
        df2_sqlcom_linetype = np.array(df1_sqlcom_linetype)
        df3_sqlcom_linetype = df2_sqlcom_linetype.tolist()
        # print(df3_sqlcom_linetype)

        # 导线选型
        sqlcom_area_line = 'select area_line from star_lines'  # 截面积
        sqlcom_m_line = 'select m_line from star_lines'  # 单位质量
        sqlcom_rou_line = 'select rou_line from star_lines'  # 导电率
        sqlcom_i_line = 'select i_line from star_lines'  # 持续载流量
        sqlcom_cal_r = 'select cal_r from star_lines'  # 计算半径
        sqlcom_q_r = 'select q_r from star_lines'  # 等效半径
        sqlcom_axis_x = 'select axis_x from star_lines'
        sqlcom_axis_y = 'select axis_y from star_lines'
        sqlcom_resistance = 'select Rd from star_lines'  # 直流电阻
        sqlcom_mu_r = 'select mu_r from star_lines'  # 磁导率
        sqlcom_rho = 'select rho from star_lines'  # 电阻率

        df1_sqlcom_area_line = pd.read_sql(sqlcom_area_line, con)
        df1_sqlcom_m_line = pd.read_sql(sqlcom_m_line, con)
        df1_sqlcom_rou_line = pd.read_sql(sqlcom_rou_line, con)
        df1_sqlcom_i_line = pd.read_sql(sqlcom_i_line, con)
        df1_sqlcom_cal_r = pd.read_sql(sqlcom_cal_r, con)
        df1_sqlcom_q_r = pd.read_sql(sqlcom_q_r, con)
        df1_sqlcom_axis_x = pd.read_sql(sqlcom_axis_x, con)
        df1_sqlcom_axis_y = pd.read_sql(sqlcom_axis_y, con)
        df1_sqlcom_resistance = pd.read_sql(sqlcom_resistance, con)
        df1_sqlcom_mu_r = pd.read_sql(sqlcom_mu_r, con)
        df1_sqlcom_rho = pd.read_sql(sqlcom_rho, con)

        df2_sqlcom_area_line = np.array(df1_sqlcom_area_line)  # 先使用array()
        # print(df2_sqlcom_area_line)
        df2_sqlcom_m_line = np.array(df1_sqlcom_m_line)  # 先使用array()将DataFrame转换一下
        df2_sqlcom_rou_line = np.array(df1_sqlcom_rou_line)  # 先使用array()将DataFrame转换一下
        df2_sqlcom_i_line = np.array(df1_sqlcom_i_line)  # 先使用array()将DataFrame转换一下
        df2_sqlcom_cal_r = np.array(df1_sqlcom_cal_r)  # 先使用array()将DataFrame转换一下
        df2_sqlcom_q_r = np.array(df1_sqlcom_q_r)  # 先使用array()将DataFrame转换一下
        df2_sqlcom_axis_x = np.array(df1_sqlcom_axis_x)  # 先使用array()将DataFrame转换一下
        df2_sqlcom_axis_y = np.array(df1_sqlcom_axis_y)  # 先使用array()将DataFrame转换一下
        df2_sqlcom_resistance = np.array(df1_sqlcom_resistance)
        df2_sqlcom_mu_r = np.array(df1_sqlcom_mu_r)
        df2_sqlcom_rho = np.array(df1_sqlcom_rho)

        df3_sqlcom_area_line = df2_sqlcom_area_line.tolist()
        # print( df3_sqlcom_area_line )
        df3_sqlcom_m_line = df2_sqlcom_m_line.tolist()
        df3_sqlcom_rou_line = df2_sqlcom_rou_line.tolist()
        df3_sqlcom_i_line = df2_sqlcom_i_line.tolist()
        df3_sqlcom_cal_r = df2_sqlcom_cal_r.tolist()
        df3_sqlcom_q_r = df2_sqlcom_q_r.tolist()
        df3_sqlcom_axis_x = df2_sqlcom_axis_x.tolist()
        df3_sqlcom_axis_y = df2_sqlcom_axis_y.tolist()
        df3_sqlcom_resistance = df2_sqlcom_resistance.tolist()
        df3_sqlcom_mu_r = df2_sqlcom_mu_r.tolist()
        df3_sqlcom_rho = df2_sqlcom_rho.tolist()

        # print(df3_sqlcom_area_line)
        # print(df3_sqlcom_m_line)
        # print(df3_sqlcom_rou_line)
        # print(df3_sqlcom_i_line)
        # print(df3_sqlcom_cal_r)
        # print(df3_sqlcom_q_r)
        # print(df3_sqlcom_axis_x)
        # print(df3_sqlcom_axis_y)
        # print(df3_sqlcom_rho)
        # print(df3_sqlcom_mu_r)
        ##########导线属性数据处理#######################
        lines_cal_r = []
        lines_q_r = []
        lines_rho = []
        lines_mu_r = []
        lines_axis_x = []
        lines_axis_y = []
        lines_resistance = []
        for i in df3_sqlcom_cal_r:
            lines_cal_r.append(i[0])
        for i in df3_sqlcom_q_r:
            lines_q_r.append(i[0])
        for i in df3_sqlcom_rho:
            lines_rho.append(i[0])
        for i in df3_sqlcom_mu_r:
            lines_mu_r.append(i[0])
        for i in df3_sqlcom_axis_x:
            lines_axis_x.append(i[0])
        for i in df3_sqlcom_axis_y:
            lines_axis_y.append(i[0])
        for i in df3_sqlcom_resistance:
            lines_resistance.append(i[0])
        # print(len(lines_cal_r))
        # 牵引变压器##########################################
        sqlcom_name_qianyin = 'select name_qianyin from star_qianyin'
        sqlcom_model_qianyin = 'select model_qianyin from star_qianyin'
        sqlcom_neizukang_qianyin_real = 'select neizukang_qianyin_real from star_qianyin'
        sqlcom_neizukang_qianyin_imag = 'select neizukang_qianyin_imag from star_qianyin'
        sqlcom_location_qianyin = 'select location_qianyin from star_qianyin'

        df1_sqlcom_name_qianyin = pd.read_sql(sqlcom_name_qianyin, con)
        df1_sqlcom_model_qianyin = pd.read_sql(sqlcom_model_qianyin, con)
        df1_sqlcom_neizukang_qianyin_real = pd.read_sql(sqlcom_neizukang_qianyin_real, con)
        df1_sqlcom_neizukang_qianyin_imag = pd.read_sql(sqlcom_neizukang_qianyin_imag, con)
        df1_sqlcom_location_qianyin = pd.read_sql(sqlcom_location_qianyin, con)

        df2_sqlcom_name_qianyin = np.array(df1_sqlcom_name_qianyin)  # 先使用array()将DataFrame转换一下
        df2_sqlcom_model_qianyin = np.array(df1_sqlcom_model_qianyin)  # 先使用array()将DataFrame转换一下
        df2_sqlcom_neizukang_qianyin_real = np.array(df1_sqlcom_neizukang_qianyin_real)  # 先使用array()将DataFrame转换一下
        df2_sqlcom_neizukang_qianyin_imag = np.array(df1_sqlcom_neizukang_qianyin_imag)
        df2_sqlcom_location_qianyin = np.array(df1_sqlcom_location_qianyin)  # 先使用array()将DataFrame转换一下

        df3_sqlcom_name_qianyin = df2_sqlcom_name_qianyin.tolist()
        df3_sqlcom_model_qianyin = df2_sqlcom_model_qianyin.tolist()
        df3_sqlcom_neizukang_qianyin_real = df2_sqlcom_neizukang_qianyin_real.tolist()
        df3_sqlcom_neizukang_qianyin_imag = df2_sqlcom_neizukang_qianyin_imag.tolist()
        df3_sqlcom_location_qianyin = df2_sqlcom_location_qianyin.tolist()

        # print(df3_sqlcom_name_qianyin)
        # print(df3_sqlcom_model_qianyin)
        # print(df3_sqlcom_neizukang_qianyin)
        # print(df3_sqlcom_location_qianyin)

        # AT变压器##################################
        self.lines_system = df3_sqlcom_linetype[0][0]
        if self.lines_system == "AT":
            sqlcom_name_AT = 'select name_AT from star_AT'
            sqlcom_model_AT = 'select model_AT from star_AT'
            sqlcom_location_AT = 'select location_AT from star_AT'
            sqlcom_lou_AT_real = 'select lou_real from star_AT'
            sqlcom_lou_AT_imag = 'select lou_imag from star_AT'

            df1_sqlcom_name_AT = pd.read_sql(sqlcom_name_AT, con)
            df1_sqlcom_model_AT = pd.read_sql(sqlcom_model_AT, con)
            df1_sqlcom_location_AT = pd.read_sql(sqlcom_location_AT, con)
            df1_sqlcom_lou_AT_real = pd.read_sql(sqlcom_lou_AT_real, con)
            df1_sqlcom_lou_AT_imag = pd.read_sql(sqlcom_lou_AT_imag, con)

            df2_sqlcom_name_AT = np.array(df1_sqlcom_name_AT)  # 先使用array()将DataFrame转换一下
            df2_sqlcom_model_AT = np.array(df1_sqlcom_model_AT)  # 先使用array()将DataFrame转换一下
            df2_sqlcom_location_AT = np.array(df1_sqlcom_location_AT)  # 先使用array()将DataFrame转换一下
            df2_sqlcom_lou_AT_real = np.array(df1_sqlcom_lou_AT_real)  # 先使用array()将DataFrame转换一下
            df2_sqlcom_lou_AT_imag = np.array(df1_sqlcom_lou_AT_imag)

            df3_sqlcom_name_AT = df2_sqlcom_name_AT.tolist()
            df3_sqlcom_model_AT = df2_sqlcom_model_AT.tolist()
            df3_sqlcom_location_AT = df2_sqlcom_location_AT.tolist()
            df3_sqlcom_lou_AT_real = df2_sqlcom_lou_AT_real.tolist()
            df3_sqlcom_lou_AT_imag = df2_sqlcom_lou_AT_imag.tolist()

        # e1和ra1##########
        sqlcom_location_star_e1_ra1 = 'select location_star_e1_ra1 from star_e1_ra1'
        df1_sqlcom_location_star_e1_ra1 = pd.read_sql(sqlcom_location_star_e1_ra1, con)

        df2_sqlcom_location_star_e1_ra1 = np.array(df1_sqlcom_location_star_e1_ra1)  # 先使用array()将DataFrame转换一下

        df3_sqlcom_location_star_e1_ra1 = df2_sqlcom_location_star_e1_ra1.tolist()

        # print(df3_sqlcom_location_star_e1_ra1)

        # e1和g
        sqlcom_location_star_e1_g = 'select location_star_e1_g from star_e1_g'
        sqlcom_Z_star_e1_g = 'select Z_star_e1_g from star_e1_g'

        df1_sqlcom_location_star_e1_g = pd.read_sql(sqlcom_location_star_e1_g, con)
        df1_sqlcom_Z_star_e1_g = pd.read_sql(sqlcom_Z_star_e1_g, con)

        df2_sqlcom_location_star_e1_g = np.array(df1_sqlcom_location_star_e1_g)  # 先使用array()将DataFrame转换一下
        df2_sqlcom_Z_star_e1_g = np.array(df1_sqlcom_Z_star_e1_g)  # 先使用array()将DataFrame转换一下

        df3_sqlcom_location_star_e1_g = df2_sqlcom_location_star_e1_g.tolist()
        df3_sqlcom_Z_star_e1_g = df2_sqlcom_Z_star_e1_g.tolist()

        # print(df3_sqlcom_location_star_e1_g)
        # print(df3_sqlcom_Z_star_e1_g)

        # e2和ra3
        sqlcom_location_star_e2_ra3 = 'select location_star_e2_ra3 from star_e2_ra3'
        df1_sqlcom_location_star_e2_ra3 = pd.read_sql(sqlcom_location_star_e2_ra3, con)

        df2_sqlcom_location_star_e2_ra3 = np.array(df1_sqlcom_location_star_e2_ra3)  # 先使用array()将DataFrame转换一下

        df3_sqlcom_location_star_e2_ra3 = df2_sqlcom_location_star_e2_ra3.tolist()

        # print(df3_sqlcom_location_star_e2_ra3)

        # e2和g
        sqlcom_location_star_e2_g = 'select location_star_e2_g from star_e2_g'
        sqlcom_Z_star_e2_g = 'select Z_star_e2_g from star_e2_g'

        df1_sqlcom_location_star_e2_g = pd.read_sql(sqlcom_location_star_e2_g, con)
        df1_sqlcom_Z_star_e2_g = pd.read_sql(sqlcom_Z_star_e2_g, con)

        df2_sqlcom_location_star_e2_g = np.array(df1_sqlcom_location_star_e2_g)  # 先使用array()将DataFrame转换一下
        df2_sqlcom_Z_star_e2_g = np.array(df1_sqlcom_Z_star_e2_g)  # 先使用array()将DataFrame转换一下

        df3_sqlcom_location_star_e2_g = df2_sqlcom_location_star_e2_g.tolist()
        df3_sqlcom_Z_star_e2_g = df2_sqlcom_Z_star_e2_g.tolist()

        # print(df3_sqlcom_location_star_e2_g)
        # print(df3_sqlcom_Z_star_e2_g)

        # ra1和g
        sqlcom_location_star_ra1_g = 'select location_star_ra1_g from star_ra1_g'
        sqlcom_Z_star_ra1_g = 'select Z_star_ra1_g from star_ra1_g'

        df1_sqlcom_location_star_ra1_g = pd.read_sql(sqlcom_location_star_ra1_g, con)
        df1_sqlcom_Z_star_ra1_g = pd.read_sql(sqlcom_Z_star_ra1_g, con)

        df2_sqlcom_location_star_ra1_g = np.array(df1_sqlcom_location_star_ra1_g)  # 先使用array()将DataFrame转换一下
        df2_sqlcom_Z_star_ra1_g = np.array(df1_sqlcom_Z_star_ra1_g)  # 先使用array()将DataFrame转换一下

        df3_sqlcom_location_star_ra1_g = df2_sqlcom_location_star_ra1_g.tolist()
        df3_sqlcom_Z_star_ra1_g = df2_sqlcom_Z_star_ra1_g.tolist()

        # print(df3_sqlcom_location_star_ra1_g)
        # print(df3_sqlcom_Z_star_ra1_g)

        # ra3和g
        sqlcom_location_star_ra3_g = 'select location_star_ra3_g from star_ra3_g'
        sqlcom_Z_star_ra3_g = 'select Z_star_ra3_g from star_ra3_g'

        df1_sqlcom_location_star_ra3_g = pd.read_sql(sqlcom_location_star_ra3_g, con)
        df1_sqlcom_Z_star_ra3_g = pd.read_sql(sqlcom_Z_star_ra3_g, con)

        df2_sqlcom_location_star_ra3_g = np.array(df1_sqlcom_location_star_ra3_g)  # 先使用array()将DataFrame转换一下
        df2_sqlcom_Z_star_ra3_g = np.array(df1_sqlcom_Z_star_ra3_g)  # 先使用array()将DataFrame转换一下

        df3_sqlcom_location_star_ra3_g = df2_sqlcom_location_star_ra3_g.tolist()
        df3_sqlcom_Z_star_ra3_g = df2_sqlcom_Z_star_ra1_g.tolist()

        # print(df3_sqlcom_location_star_ra1_g)
        # print(df3_sqlcom_Z_star_ra1_g)

        # 机车
        # sqlcom_1_locomotive = 'select names_star_locomotive from star_locomotive'
        sqlcom_1_locomotive = 'select locomotive1_star_locomotive from star_locomotive'
        sqlcom_2_locomotive = 'select locomotive2_star_locomotive from star_locomotive'
        sqlcom_3_locomotive = 'select locomotive3_star_locomotive from star_locomotive'
        sqlcom_4_locomotive = 'select locomotive4_star_locomotive from star_locomotive'
        sqlcom_5_locomotive = 'select locomotive5_star_locomotive from star_locomotive'
        sqlcom_attribute_locomotive = 'select names_star_locomotive from star_locomotive'
        # sqlcom_Harmonic_content_locomotive = 'select Harmonic_content_locomotive from star_locomotive'
        # sqlcom_location_locomotive = 'select location_locomotive from star_locomotive'

        df1_sqlcom_1_locomotive = pd.read_sql(sqlcom_1_locomotive, con)
        df1_sqlcom_2_locomotive = pd.read_sql(sqlcom_2_locomotive, con)
        df1_sqlcom_3_locomotive = pd.read_sql(sqlcom_3_locomotive, con)
        df1_sqlcom_4_locomotive = pd.read_sql(sqlcom_4_locomotive, con)
        df1_sqlcom_5_locomotive = pd.read_sql(sqlcom_5_locomotive, con)
        df1_sqlcom_5_locomotive = pd.read_sql(sqlcom_5_locomotive, con)
        # df1_sqlcom_location_locomotive = pd.read_sql(sqlcom_location_locomotive,con)
        df1_sqlcom_attribute_locomotive = pd.read_sql(sqlcom_attribute_locomotive, con)

        df2_sqlcom_1_locomotive = np.array(df1_sqlcom_1_locomotive)  # 先使用array()将DataFrame转换一下
        df2_sqlcom_2_locomotive = np.array(df1_sqlcom_2_locomotive)  # 先使用array()将DataFrame转换一下
        df2_sqlcom_3_locomotive = np.array(df1_sqlcom_3_locomotive)  # 先使用array()将DataFrame转换一下
        df2_sqlcom_4_locomotive = np.array(df1_sqlcom_4_locomotive)  # 先使用array()将DataFrame转换一下
        df2_sqlcom_5_locomotive = np.array(df1_sqlcom_5_locomotive)  # 先使用array()将DataFrame转换一下
        df2_sqlcom_attribute_locomotive = np.array(df1_sqlcom_attribute_locomotive)
        # df2_sqlcom_location_locomotive = np.array(df1_sqlcom_location_locomotive) #先使用array()将DataFrame转换一下

        # df3_sqlcom_1_locomotive = df2_sqlcom_1_locomotive.tolist()
        # df3_sqlcom_2_locomotive = df2_sqlcom_2_locomotive.tolist()
        # df3_sqlcom_3_locomotive = df2_sqlcom_3_locomotive.tolist()
        # df3_sqlcom_4_locomotive = df2_sqlcom_4_locomotive.tolist()
        # df3_sqlcom_5_locomotive = df2_sqlcom_5_locomotive.tolist()
        # df3_sqlcom_location_locomotive = df2_sqlcom_location_locomotive.tolist()
        # print(df2_sqlcom_1_locomotive)
        # print(df2_sqlcom_1_locomotive.shape)

        dff_locomotive = np.hstack((df2_sqlcom_1_locomotive, df2_sqlcom_2_locomotive))
        dff_locomotive = np.hstack((dff_locomotive, df2_sqlcom_3_locomotive))
        dff_locomotive = np.hstack((dff_locomotive, df2_sqlcom_4_locomotive))
        dff_locomotive = np.hstack((dff_locomotive, df2_sqlcom_5_locomotive))
        # print(dff_locomotive)
        # print(dff_locomotive.shape[0])
        # print(df3_sqlcom_model_locomotive)
        # print(df3_sqlcom_upanddown_locomotive)
        # print(df3_sqlcom_loadcurrent_locomotive)
        # print(df3_sqlcom_Harmonic_frequency_locomotive)
        # print(df3_sqlcom_Harmonic_content_locomotive)
        # print(df3_sqlcom_location_locomotive)

        #####导线数据填充#######################################################################################

        if self.lines_system == "AT":
            lines_total = ['cw1', 'mw1', 'pf1', 'ra1', 'ra2', 'pw1', 'e1', 'cw2', 'mw2', 'pf2', 'ra3', 'ra4', 'pw2',
                           'e2']
            for i in range(len(lines_total)):
                simple_line = Line(name=lines_total[i], radius=lines_q_r[i], equivalent_radius=lines_q_r[i],
                                   rho=lines_rho[i], mu_r=lines_mu_r[i], coordinate_x=lines_axis_x[i],
                                   coordinate_y=lines_axis_y[i], resistance=lines_resistance[i])
                self.lines.append(simple_line)
        elif self.lines_system == "DT":
            lines_total = ['cw1', 'mw1', 'ra1', 'ra2', 'e1', 'cw2', 'mw2', 'ra3', 'ra4', 'e2']
            for i in range(len(lines_total)):
                simple_line = Line(name=lines_total[i], radius=lines_q_r[i], equivalent_radius=lines_q_r[i],
                                   rho=lines_rho[i], mu_r=lines_mu_r[i], coordinate_x=lines_axis_x[i],
                                   coordinate_y=lines_axis_y[i], resistance=lines_resistance[i])
                self.lines.append(simple_line)

        #######对traction_transformer对象赋值############################################
        tractiontransformer_num = len(df3_sqlcom_location_qianyin)
        print('牵引变压器的数量=' + str(tractiontransformer_num))
        tractiontransformer_list = []
        for i in range(0, tractiontransformer_num):
            tractiontransformer_list.append(str(i))  # 根据对象的数量形成'代号’列表
        for i in range(0, tractiontransformer_num):
            tractiontransformer_list[i] = TractionTransformer()
            tractiontransformer_list[i].name = df2_sqlcom_name_qianyin[i][0]
            tractiontransformer_list[i].alias_name = df3_sqlcom_model_qianyin[i][0]
            tractiontransformer_list[i].zs = df3_sqlcom_neizukang_qianyin_real[i][0] + 1j * \
                                             df3_sqlcom_neizukang_qianyin_imag[i][0]
            tractiontransformer_list[i].location = df3_sqlcom_location_qianyin[i][0]
            self.traction_transformer.append(tractiontransformer_list[i])
        ######对auto_transformers对象赋值#############################################
        if self.lines_system == "AT":
            auto_transformer_num = len(df3_sqlcom_location_AT)
            print('AT变压器的数量=' + str(auto_transformer_num))
            auto_transformer_list = []
            for i in range(0, auto_transformer_num):
                auto_transformer_list.append(str(i))  # 根据对象的数量形成'代号’列表
            for i in range(0, auto_transformer_num):
                auto_transformer_list[i] = AutoTransformer()
                auto_transformer_list[i].name = df3_sqlcom_name_AT[i][0]
                auto_transformer_list[i].alias_name = df3_sqlcom_model_AT[i][0]
                auto_transformer_list[i].zs = df3_sqlcom_lou_AT_real[i][0] + 1j * df3_sqlcom_lou_AT_imag[i][0]
                auto_transformer_list[i].location = df3_sqlcom_location_AT[i][0]
                self.auto_transformers.append(auto_transformer_list[i])
        ########对cross_connections对象赋值###############################
        Crossconnections = CrossConnection()
        ######e1_ra1属性###############
        cross_connections_e1_ra1_num = len(df3_sqlcom_location_star_e1_ra1)
        print('e1与ra1连接线的数量=' + str(cross_connections_e1_ra1_num))
        for i in range(0, cross_connections_e1_ra1_num):
            Crossconnections.e1_ra1.append(df3_sqlcom_location_star_e1_ra1[i][0])
        ####对e1_g属性##################################################
        cross_connections_e1_g_num = len(df3_sqlcom_location_star_e1_g)
        print('e1与g连接线的数量=' + str(cross_connections_e1_g_num))
        for i in range(0, cross_connections_e1_g_num):
            Crossconnections.e1_g[df3_sqlcom_location_star_e1_g[i][0]] = df3_sqlcom_Z_star_e1_g[i][0]
        ##对e2_g属性##############################################
        cross_connections_e2_g_num = len(df3_sqlcom_location_star_e2_g)
        print('e2与g连接线的数量=' + str(cross_connections_e2_g_num))
        for i in range(0, cross_connections_e2_g_num):
            Crossconnections.e2_g[df3_sqlcom_location_star_e2_g[i][0]] = df3_sqlcom_Z_star_e2_g[i][0]
        #####对ra1_g属性#################################################
        cross_connections_ra1_g_num = len(df3_sqlcom_location_star_ra1_g)
        print('ra1与g连接线的数量=' + str(cross_connections_ra1_g_num))
        for i in range(0, cross_connections_ra1_g_num):
            Crossconnections.ra1_g[df3_sqlcom_location_star_ra1_g[i][0]] = df3_sqlcom_Z_star_ra1_g[i][0]
        #######对ra3_g属性##############################################
        cross_connections_ra3_g_num = len(df3_sqlcom_location_star_ra3_g)
        print('ra3与g连接线的数量=' + str(cross_connections_ra3_g_num))
        for i in range(0, cross_connections_ra3_g_num):
            Crossconnections.ra3_g[df3_sqlcom_location_star_ra3_g[i][0]] = df3_sqlcom_Z_star_ra3_g[i][0]
        #######################
        self.cross_connections.append(Crossconnections)
        #########对机车locomotive对象赋值##########################################################
        locomotive_num = 0
        for i in range(5):
            if dff_locomotive[0][i] != 0:
                locomotive_num = locomotive_num + 1
            else:
                continue
        print("机车的数量=" + str(locomotive_num))
        locomotive_list = []
        for i in range(locomotive_num):
            locomotive_list.append(str(i))  # 根据对象的数量形成'代号’列表

        for i in range(locomotive_num):
            locomotive_list[i] = Locomotive(name='机车' + str(i + 1))
        for i in range(0, locomotive_num):
            locomotive_list[i].location = dff_locomotive[0][i]
            locomotive_list[i].load = dff_locomotive[1][i]
            locomotive_list[i].at_upline = dff_locomotive[2][i]  # 对每个机车的位置上下行负荷电流赋值

        harmonic_num = []
        for i in range(3, dff_locomotive.shape[0]):
            harmonic_num.append(df2_sqlcom_attribute_locomotive[i][0])

        for i in range(0, locomotive_num):
            harmonic_percent = []
            for j in range(3, dff_locomotive.shape[0]):
                harmonic_percent.append(dff_locomotive[j][i])
            for k in range(0, len(harmonic_num)):
                locomotive_list[i].harmonic[harmonic_num[k]] = harmonic_percent[k]  # 对每个机车的谐波含量及次数赋值

        for i in range(locomotive_num):
            self.locomotive.append(locomotive_list[i])  # 对topology类中的locomotive对象赋值填充


topology = Topology(name="测试供电臂")
#############################################################################################
topology.set_topology(db_file_name="DT-system.db")
############测试lines对象##################################################
print('====================================================================================')
print('依次为：导线名称、直流电阻、计算半径、等效半径、电阻率、磁导率、x坐标、y坐标')
##判断AT和DT
if topology.lines_system == "AT":
    N = 14
elif topology.lines_system == "DT":
    N = 10
for i in range(N):
    print(topology.lines[i].name, topology.lines[i].type_name, topology.lines[i].resistance, topology.lines[i].radius,
          topology.lines[i].equivalent_radius, topology.lines[i].rho, topology.lines[i].mu_r,
          topology.lines[i].coordinate_x, topology.lines[i].coordinate_y)
    # print(type(topology.lines[i].coordinate_x))
print('====================================================================================')
###########测试tractiontransformers对象##################################
print(topology.traction_transformer[0].zs)
print('====================================================================================')
############测试auto_transformers对象#####################################
if topology.lines_system == "AT":
    for i in range(2):
        print(topology.auto_transformers[i].name, topology.auto_transformers[i].alias_name,
              topology.auto_transformers[i].zs)
elif topology.lines_system == "DT":
    print(topology.auto_transformers)
print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
##########测试crossconnection对象####################################
print(topology.cross_connections[0].ra3_g)
print('*************************************************')
print(topology.cross_connections[0].e1_ra1)
print('*************************************************')
print(topology.cross_connections[0].e1_g)
print('====================================================================================')
#########测试机车locomotive对象#############################################
for i in range(1):
    print(topology.locomotive[i].harmonic, topology.locomotive[i].name, topology.locomotive[i].load,
          topology.locomotive[i].location)