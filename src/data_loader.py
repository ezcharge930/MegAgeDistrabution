import pandas as pd
import numpy as np
from pathlib import Path

def load_core_data():
        
    data_dir = Path('./data')
    data_dir.mkdir(exist_ok=True)

    # column_mapping = {
    #     "HZJBXX_HZJBXX_XB": "gender",         # 性别
    #     "HZJBXX_HZJBXX_CSRQ": "birth_date",   # 出生日期
    #     "ZYBASY_CYRQSJ": "diagnosis_date",    # 诊断日期
    #     "ZXHZ_ID": "medical_record_no"        # 病案号
    # }

    source_path = r'D:\下载\食管癌数据\out_put\访视(住院就诊).csv'
    # 潜入数据内部侦查
    # print("🗡️ 列名侦察模式启动...")
    # header_df = pd.read_csv(source_path, nrows=2, encoding='utf-8')
    # print(f"第1行(中文):\n{header_df.columns.values}")
    # print(f"第2行(英文):\n{header_df.iloc[0].values}")
    
    header_df = ['ZXHZ_ID', 'HZJBXX_HZJBXX_CSRQ', 'HZJBXX_HZJBXX_XB', 'ZYBASY_CYRQSJ']
    name_list = ['medical_record_no','birth_date','gender','diagnosis_date']

    df = pd.read_csv(
        source_path,
        skiprows=1,
        header=0,
        usecols=header_df,
        # names = name_list,
        dtype={"ZXHZ_ID": "string"},
        parse_dates=["HZJBXX_HZJBXX_CSRQ", "ZYBASY_CYRQSJ"],
        encoding='GB18030',
        engine='python'
    )
    
    df = df.rename(columns=dict(zip(header_df, name_list)))

    df.to_csv(data_dir / r'MedAge.csv', index=False, encoding='utf-8')

    return df



