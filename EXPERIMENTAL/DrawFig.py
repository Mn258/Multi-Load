import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import pickle
import matplotlib.ticker as ticker
from matplotlib.ticker import FixedLocator

# matplotlib.rcParams['ps.useafm'] = True
# matplotlib.rcParams['pdf.use14corefonts'] = True
# matplotlib.rcParams['text.usetex'] = True

matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

# matplotlib.rcParams['text.usetex'] = True

file_name = "EXPERIMENTAL/repositioning.xlsx.pkl"
# file_name = "result_data.xlsx.pkl"

with open(file_name, 'rb') as file:
    result_data = pickle.load(file)

# 打印读取的数据
print(result_data)

# map_name = ["map_1", "map_2", "map_3", "map_4", "map_5", "map_6", "map_8"]
# metric = ["Processing Time", "Average Number of Conflict", "Sum of Costs", "Makespan", "Success Rate"]
# metric_name = ["PT", "ANC", "SC", "MS", "SR"]
# algorithms = ["EPEA*", "MC-CBS", "MC-CBS-MS", "GPLU", "GPLU-S", "GPLU-L", "GPLU-SL"]
# colors = ["black", "gray", "#1874CD", "#9ACD32", "#F4A445", "#00BEC0", "#D82323"]
# markers = ['$\Lambda$', '$\Delta$', '$\Psi$', '$\Phi$', '$\Theta$', "$\mho$", '$\Omega$']

map_name = ["agentNum", "taskNum", "capacity"]
metric = ["Service Time", "Makespan", "Processing Time"] # , "Completion Ratio"
metric_name = ["ST", "MS", "PT"] # , "CR"
algorithms1 = ["nCAR", "IIG", "MAKM", "TGA"]
# algorithms2 = ["PR", "PR-CBS", "MWM", "FDR-M"]
colors = ["gray", "#1874CD", "#9ACD32", "red"]
markers = ['$\Lambda$', '$\Delta$', '$\Psi$', '$\Phi$', '$\Theta$']

for first_element in map_name[0:]:
    for each_metric in metric:
        algorithms = algorithms1
        # if first_element == "T" or each_metric == "Processing Time":
        #     algorithms = algorithms2

        # plt.rcParams['font.sans-serif'] = ['Times New Roman']  # 如果要显示中文字体，则在此处设为：SimHei

        key_name = first_element + each_metric
        print(key_name, "???????")

        print(result_data[key_name], "??????????????")
        current_data = result_data[key_name]
        x = list(current_data["coordinate"])  # x轴刻度
        x_temp = []

        for i in range(len(x)):
            x_temp.append(i)

        # 基础设置
        # 绘制折线图
        plt.figure(figsize=(10, 8))  # 设置图形大小
        if each_metric == "Processing Time":
            plt.yscale('log')
        plt.yticks(fontsize=30)
        # plt.xlim(2, 34)
        print(x_temp, int(len(x_temp)/2), "????????")
        plt.xticks(x_temp, x, fontsize=30)  # 默认字体大小为30

        # 生成七组随机数据，每组数据长度不等
        data = []
        # for i in range(7):
        #     data.append(np.random.rand(np.random.randint(5, 15)))

        for each_algorithm in algorithms:
            data.append(current_data[each_algorithm])

        for i, dataset in enumerate(data):
            plt.plot(dataset, label=algorithms[i], color=colors[i], linewidth=5, marker=markers[i],  markersize=18, clip_on=False)  # 绘制每组数据的折线

        # plt.title(metric)
        if first_element == "agentNum":
            plt.xlabel("Agents", fontsize=30)
        elif first_element == "taskNum":
            plt.xlabel("Tasks", fontsize=30)
        else:
            plt.xlabel("Capacity", fontsize=30)
            

        if each_metric == "Processing Time":
            plt.ylabel("Processing Time (ms)", fontsize=30)
            ax=plt.gca()
            # plt.ylim(10**1, 2*10**2)
            # ax.yaxis.set_major_locator(FixedLocator([10**1, 10**2]))
        elif each_metric == "Service Time":
            num = 10000
            plt.ylabel("Service Time"+" (x"+r'$10^4$'+")", fontsize=30)
            plt.locator_params(axis='y', nbins=5)
        elif each_metric == "Makespan":
            num = 1000
            plt.ylabel("Makespan"+" (x"+r'$10^3$'+")", fontsize=30)
            plt.locator_params(axis='y', nbins=5)
        else:
            plt.ylabel(each_metric, fontsize=30)

        # if first_element == "taskNum":
        #     plt.xlim("1k", "5k")

        if len(x_temp) >= 0:
            # plt.locator_params(axis="x", nbins=int(len(x_temp)/2 + 1))
            plt.locator_params(axis='x', nbins=5)

        if each_metric != "Processing Time" and each_metric != "Service Time" and each_metric != "Makespan":
            plt.locator_params(axis="y", nbins=5)
        # plt.legend()  # 添加图例

        plt.legend( numpoints=1, handlelength=2, frameon=False, ncol=1)
        leg = plt.gca().get_legend()
        ltext = leg.get_texts()
        plt.setp(ltext, fontsize=30)  # 设置图例字体的大小和粗细

        # plt.grid(True)  # 显示网格
        plt.tight_layout()  # 自动调整布局，防止标签重叠

        save_name = first_element + metric_name[metric.index(each_metric)]
        save_location = "Thesis/Fig/" + save_name + '.eps'
        plt.savefig(save_location)  # 建议保存为svg格式，再用inkscape转为矢量图emf后插入word中
        plt.show()
    # assert 1 == 2