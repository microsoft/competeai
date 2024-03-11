### 一、终极目的

构建成一个可以模拟任何实验的统一框架，但是由于每个模拟实验之间需要不同的prompt，不同的流程，该目的尚未实现。

### 二、基本假定

Agent模拟实验可以视为若干基础的scenes以某种序列串行/并行运行实现。每个scene中有若干agent以某种序列进行交互。

### 三、问题

Agent不懂得如何输出规定的数据格式，Agent在长期交互中忘记规定程序。

因此需要持续输入prompt进行引导。

### 四、框架结构

```python
.
├── database                       <- 饭店模拟中的饭店管理系统
├── database.sh                    <- 操作数据库的脚本文件
├── logs                           <- 所有实验结果记录于此，pipeline的一环
├── README.md                      <- 你在这里
├── run.py                         <- 程序运行入口
├── SocioSim                     <- 核心文件夹
│   ├── agent                     <- 框架核心组件： agent。 在其中可以设置更加负责的agent结构
│   │   ├── agent.py               <- 完成agent观测，反应，执行模型（本质上就是输入prompt，输出response的过程）
│   │   ├── backends               <- 可以用不同的大模型模拟agent，但是一般用gpt4
│   │   │   ├── openai.py
|   |   |   └── ... 
│   │   └── __init__.py
│   ├── config.py           
│   ├── examples                   <- 每个模拟实验都需要有这样一个配置文件，其中规定了参与的agent，他们扮演的角色，支持他们的LLM
│   │   ├── group.yaml
│   │   └── restaurant.yaml
│   ├── globals.py
│   ├── image.py
│   ├── __init__.py
│   ├── message.py                 <- 框架核心组件：message。每一次agent做出的response都算一个message，message除了包含response内容，还包含该message的主人（agent）,该信息可以由谁看到等等
│   ├── prompt_template            <- 框架核心组件：prompt template。在交互过程中需要用到的prompt，在适当时候输给agent，指导他们的行动
│   │   ├── dine
│   │   │   ├── comment.txt
│   │   │   ├── feeling.txt
│   │   │   └── order.txt
│   │   ├── group_dine
│   │   │   └── ...
│   │   └── restaurant_design
│   │       └── ...
│   ├── relationship.yaml   
│   ├── scene                     <- *框架核心组件：scene。每个scene中实现了一个agent交互序列，例如多个顾客讨论环节。
│   │   ├── base.py
│   │   ├── dine.py
│   │   ├── group_dine.py
│   │   ├── __init__.py
│   │   └── restaurant_design.py
│   ├── simul.py                  <- 核心文件：负责协调多个scene运行，实现scene以任意顺序运行
│   └── utils                     <- 一些工具
│       ├── analysis.py
│       ├── database.py
│       ├── draw.py
│       ├── image.py
│       ├── __init__.py
│       ├── log.py
│       ├── prompt_template.py
└── test                          <- 单元测试文件
    ├── get_base64.py
    └── ...
```

### 五、针对斯坦福实验的设计

1. 设置global prompt
2. 确定参与的agent（狱警和囚犯），设置他们的背景
3. 确定需要的scene，以及他们之间运行先后顺序。
4. 确定每个scene需要输入的prompt和输入时机
5. 确定在实验过程中需要记录的信息（起床时间，行动集等）




