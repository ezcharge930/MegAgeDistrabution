
from pathlib import Path
import os,sys

current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

from data_loader import load_core_data
from analysis import PatientAgeAnalyzer

def main():
    print('医疗患者年龄数据分析')
    patient_data = load_core_data()
    print(f'加载{len(patient_data)}条患者')

    print('年龄分布')
    analyzer = PatientAgeAnalyzer(patient_data)
    analyzer.analyze_age_distribution(
        bins=[0, 18, 30, 45, 65, 100],  # 定制分组
        labels=['未成年', '青年', '壮年', '中年', '老年']
    )
    print('分析完成')
    
    report_path = r'D:\Python\MedAgeStats\reports\age_distribution_report.txt'
    analyzer.generate_report(report_path)
    
    print('关键分布预览')
    print(analyzer.age_distribution)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f'异常:{e}')
    finally:
        print('结束')
