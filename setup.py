import os

dirs = [
    'src',      ## 源代码
    'tests',    ## 单元测试
    'docs',     ## 文档
    'data',     ## 样本数据
    'reports',  ## 生产报告
    '.github'
]

# 创建目录

for dir in dirs:
    os.makedirs(dir,exist_ok = True)
    print(f"Created directory:{dir}")

# 创建README.md
with open("README.md",'w') as f:
    f.write("MedAgeStats 项目\n\n医保数据分析工具")

# 创建requirements.txt

with open('requirements.txt','w') as f:
    f.write('pandas\nmatplotlib\nopenpyxl\nnumpy')

print('\n项目初始化')
