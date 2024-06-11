import os
import re
import numpy as np

class ExperimentStatistics:
    def __init__(self, root_directory, keywords, output_file):
        """
        初始化实验统计器
        
        :param root_directory: 根目录路径
        :param keywords: 关键字列表，用于定位文件中的实验结果
        :param output_file: 输出文件路径
        """
        self.root_directory = root_directory
        self.keywords = keywords
        self.output_file = output_file

    def _extract_results(self, line):
        """
        从包含实验结果的行中提取结果值
        
        :param line: 文件中的一行
        :return: 关键字和提取的结果值
        """
        for keyword in self.keywords:
            if keyword in line:
                result = line.split(keyword)[1].strip()
                try:
                    return keyword, float(result)
                except ValueError:
                    return keyword, None
        return None, None

    def _process_file(self, file_path):
        """
        处理文件，提取实验结果
        
        :param file_path: 文件路径
        :return: 文件中所有关键字的结果字典
        """
        results = {keyword: [] for keyword in self.keywords}
        with open(file_path, 'r') as file:
            for line in file:
                keyword, result = self._extract_results(line)
                if result is not None:
                    results[keyword].append(result)
        return results

    def _dfs_traverse(self):
        """
        深度优先遍历目录，处理所有文件
        """
        all_results = {}
        for root, dirs, files in os.walk(self.root_directory):
            for file in files:
                if file.endswith('.log'):
                    file_path = os.path.join(root, file)
                    file_results = self._process_file(file_path)
                    all_results[file_path] = file_results
        return all_results

    def calculate_statistics(self):
        """
        计算所有实验结果的平均值和标准差
        """
        all_results = self._dfs_traverse()
        statistics = {}
        for file_path, results in all_results.items():
            statistics[file_path] = {}
            for keyword, values in results.items():
                if values:
                    mean = np.mean(values)
                    std_dev = np.std(values)
                    statistics[file_path][keyword] = (mean, std_dev)
        return statistics

    def write_statistics(self):
        """
        将统计结果写入文件
        """
        statistics = self.calculate_statistics()
        with open(self.output_file, 'a') as file:
            for file_path, keywords in statistics.items():
                for keyword, (mean, std_dev) in keywords.items():
                    file.write(f'{file_path} - {keyword}\n')
                    file.write(f'实验结果: {round(mean*100, 1)}±{round(std_dev*100, 1)}\n\n')

# 使用示例
if __name__ == "__main__":
    root_directory = "results/mettack"
    keywords = ["NoisyGCN Non Attacked Acc:", "NoisyGCN Attacked Acc:"]
    output_file = "statistics_output.txt"

    stats = ExperimentStatistics(root_directory, keywords, output_file)
    stats.write_statistics()