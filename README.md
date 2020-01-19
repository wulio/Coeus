# Coeus

Coeus：
  Coeus was one of the Titans, son of Uranus and Gaia. His name means questioning.
  
  if we need import android sdk,we maybe have some questions about the sdk,like sercurity/permissions/policy/info
  
  Coeus project will help you do this . you can see report.xml in report dir.

  
# Try
Try your first Coeus scan:
    
    python coeus.py xxx.aar


# CH

## 0x01 项目地址

项目地址：
	https://github.com/wulio/Coeus

## 0x02 依赖环境

​	python 3.x / java	

## 0x03 安装使用教程

  - 安装 ：
      git clone https://github.com/wulio/Coeus.git
  - 一键扫描：
      python coeus.py xxx.aar

## 0x04 相关说明

-   相关政策代码及隐私代码检测策略，均在scrpit文件夹中，json格式便于添加与修改

- 	相应的工具也存储在tool文件夹下

- 	具体代码逻辑均可在项目组查看。

- 	生成的扫描文件，输出在result文件夹下,分别有对应的log文件和输出的report.xml文件。


## 0x05 使用示例

    python ceous.py ./test/getui_2.13.3.0-gisdk_3.1.9.1-gssdk_2.3.0.0.aar	

# Authors

- deff

# License

Coeus support [Apache License 2.0](https://github.com/baidu/AdvBox/blob/master/LICENSE)

# Email
  deffingh@gmail.com

# Issues
  welcome star or issues!

# Plan

- [x] - more-sdk-info         2019.12.30
- [ ] - script-update    2019.1.15
- [ ] - apk-support      2019.2.7
- [ ] - dynamicscannner  2019.3
- [ ] - fuzz            2020.4
- [ ] - 
- [ ] - 
- [ ] -

# Project
version : v1.0.1
time :2019-12-30
1. 更新部分script规则
2. 更新支持输入文件为相对路径
3. 更新url展示，过滤其中相同url地址
4. 添加部分工具，如adb/dex2jar等工具

