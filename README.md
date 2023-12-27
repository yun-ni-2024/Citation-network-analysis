# Citation-network-analysis---Python-course-project
2023-Fall NJU

文件夹结构如下，其中带*的文件或目录为程序运行时生成的额外数据或日志文件，在提交版本中为节省空间已删去

      |- main
            |- source # Python源代码文件
                  |- request.py # 爬取数据的程序
                  |- chart.py # 生成图表的程序
            |-data
                  |- lab_1 # 不同爬虫工作的独立工作空间
                        |- data.json # 爬取的数据文件
                        |- run # 运行时存放数据的文件夹，运行request.py时自动生成
                              |- queue.txt
                              |- vis.txt
                        |- *save # 保存备份数据的文件夹，运行request.py时自动生成
                              |- ...
                        |- *log # 存放日志文件的文件夹，运行request.py时自动生成
                              |- *run.log
                  |- lab_2
                        |- ...
                  |- ...
            |- result # 存放生成图表的文件夹，运行chart.py时自动生成
                  |- ...
            |- README.md # 说明文档
