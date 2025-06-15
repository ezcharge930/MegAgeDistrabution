import pandas as pd
from pathlib import Path

data_dir = Path('./data')
data_dir.mkdir(exist_ok=True)

class PatientAgeAnalyzer:
    
    def __init__(self,patient_df):
        self.df = patient_df.copy()
        self._calculate_age()
    
    def _calculate_age(self):
        clean_df = self.df.copy()
        DATE_FORMATS = [
            '%Y-%m-%d',       # 国际标准
            '%Y/%m/%d',       # 常用格式
            '%Y%m%d',         # 紧凑格式
            '%d/%m/%Y',       # 欧洲格式
            '%m/%d/%Y',       # 北美格式
            '%Y年%m月%d日',    # 中文格式
            '%d-%b-%Y',       # 15-Jan-2023
            '%b %d, %Y'       # Jan 15, 2023
        ]
        
        # === 第一步：净化出生日期列 ===
        if clean_df['birth_date'].dtype == 'object':
            print("🧹 净化出生日期列...")
            clean_df['birth_date'] = pd.to_datetime(
                clean_df['birth_date'],
                errors='coerce',        # 错误转为NaT
                format='mixed',          # Pandas 2.0+ 智能识别
                infer_datetime_format=True
            )
        
        # === 第二步：双重保险时间转换 ===
        def universal_converter(date_series):
            """通用时间净化术式"""
            # 优先尝试Pandas自动转换
            temp_col = pd.to_datetime(date_series, errors='coerce')
            
            # 寻找失败案例（NaT）
            failed_mask = temp_col.isna()
            
            # 手动尝试各种格式
            for fmt in DATE_FORMATS:
                # 仅处理失败案例
                failed_dates = date_series[failed_mask]
                if len(failed_dates) == 0:
                    break
                    
                try:
                    # 使用datetime精确转换
                    converted = pd.to_datetime(
                        failed_dates, 
                        format=fmt, 
                        errors='coerce'
                    )
                    # 更新成功转换的值
                    temp_col[failed_mask] = converted
                    # 更新失败掩码
                    failed_mask = temp_col.isna()
                    
                    print(f"✨ 使用 {fmt} 格式成功转换 {len(converted) - sum(converted.isna())} 条日期")
                except:
                    continue
                
            
                    
            return temp_col
        
        
        

        # === 第三步：执行时间圣战 ===
        print("🔥 启动时间统一战场...")
        clean_df['birth_date'] = universal_converter(clean_df['birth_date'])
        clean_df['diagnosis_date'] = universal_converter(clean_df['diagnosis_date'])  


        
        first_diagnosis = self.df.groupby('medical_record_no')['diagnosis_date'].min()

        clean_df = self.df.drop_duplicates('medical_record_no').set_index('medical_record_no')

        clean_df['first_diagnosis'] = first_diagnosis
                
        clean_df['diagnosis_age'] = (
            (clean_df['first_diagnosis'] - clean_df['birth_date']).dt.days / 365.25
        ).round(1)

        self.df = clean_df.query('0<=diagnosis_age<=120').reset_index()
        
        return clean_df
    
    def analyze_age_distribution(self,bins=None,labels=None):
        bins = bins or [0, 18, 35, 60, 100]
        labels = labels or ['青少年', '青年', '中年', '老年']
        
        self.df['age_group'] = pd.cut(
            self.df['diagnosis_age'],
            bins = bins,
            labels = labels,
            include_lowest = True
        )
        
        self.age_distribution = self.df['age_group'].value_counts().sort_index()

        return self
    
    def generate_report(self,output_path=data_dir / 'reports.txt'):
        
        from datetime import datetime
        
        Path(output_path).parent.mkdir(parents=True,exist_ok=True)
        
        report_time = datetime.now().strftime("%Y-%m-%d %H:%M")

        with open(output_path,'w',encoding='utf-8') as f:
            f.write('年龄分布分析报告')
            f.write(f'生成时间:{report_time}\n\n')
            f.write(f'总例叔:{len(self.df)}\n\n')
            f.write('年龄分布:\n')
            
            for group,count in self.age_distribution.items():
                percent = count / len(self.df)* 100
                f.write(f'- {group}:{count}人({percent:.1f}%)\n')
                
            f.write('以上')
        return output_path
