# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2021/5/4 18:11
Desc: 问财-热门股票排名
http://www.iwencai.com/unifiedwap/home/index
"""
import os

import pandas as pd
import requests
from py_mini_racer import py_mini_racer


def _get_js_path_ths(name: str = None, module_file: str = None) -> str:
    """
    获取 JS 文件的路径(从模块所在目录查找)
    :param name: 文件名
    :type name: str
    :param module_file: 模块路径
    :type module_file: str
    :return: 路径
    :rtype: str
    """
    module_folder = os.path.abspath(os.path.dirname(os.path.dirname(module_file)))
    module_json_path = os.path.join(module_folder, "stock_feature", name)
    return module_json_path


def _get_file_content_ths(file_name: str = "ase.min.js") -> str:
    """
    获取 JS 文件的内容
    :param file_name:  JS 文件名
    :type file_name: str
    :return: 文件内容
    :rtype: str
    """
    setting_file_name = file_name
    setting_file_path = _get_js_path_ths(setting_file_name, __file__)
    with open(setting_file_path) as f:
        file_data = f.read()
    return file_data


def stock_wc_hot_rank() -> pd.DataFrame:
    """
    问财-热门股票排名
    http://www.iwencai.com/unifiedwap/home/index
    :return: 热门股票排名
    :rtype: pandas.DataFrame
    """
    url = "http://www.iwencai.com/unifiedwap/unified-wap/v2/result/get-robot-data"
    js_code = py_mini_racer.MiniRacer()
    js_content = _get_file_content_ths("ths.js")
    js_code.eval(js_content)
    v_code = js_code.call("v")
    headers = {
        "hexin-v": v_code,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
    }
    params = {
        "question": "热门5000股票",
        "perpage": "5000",
        "page": "1",
        "secondary_intent": "",
        "log_info": '{"input_type":"click"}',
        "source": "Ths_iwencai_Xuangu",
        "version": "2.0",
        "query_area": "",
        "block_list": "",
        "add_info": '{"urp":{"scene":1,"company":1,"business":1},"contentType":"json"}',
    }
    r = requests.post(url, data=params, headers=headers)
    data_json = r.json()
    temp_df = pd.DataFrame(
        data_json["data"]["answer"][0]["txt"][0]["content"]["components"][0]["data"][
            "datas"
        ]
    )
    temp_df.reset_index(inplace=True)
    temp_df["index"] = range(1, len(temp_df) + 1)
    temp_df.columns = [
        "序号",
        "个股热度排名",
        "股票代码",
        "个股热度排名名次",
        "个股热度",
        "股票简称",
        "现价",
        "涨跌幅",
        "个股热度排名基数",
        "_",
        "_",
    ]
    temp_df = temp_df[
        [
            "序号",
            "股票代码",
            "股票简称",
            "现价",
            "涨跌幅",
            "个股热度",
            "个股热度排名名次",
            "个股热度排名",
            "个股热度排名基数",
        ]
    ]
    temp_df["涨跌幅"] = round(temp_df["涨跌幅"].astype(float), 2)
    return temp_df


if __name__ == "__main__":
    stock_wc_hot_rank_df = stock_wc_hot_rank()
    print(stock_wc_hot_rank_df)
