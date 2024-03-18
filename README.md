## Introduction

SocioSim is currently the experimental framework for our work in competeai. The construction of this framework is based on the following fundamental ideas:

- Most sociological experiments can be decomposed into several scenes, where various agents interact in a certain order within each scene.
  - For example, in the competeai experiment, it can be broken down into scenes such as restaurant management, customer group discussions, customer dining, and feedback. In the first scene of restaurant management, the agent playing the role of the boss needs to modify each restaurant module in sequence. In the second scene of customer group discussions, the customers need to speak in a certain order, and so on.
- Currently, many multi-agent frameworks do not allow agents to complete tasks within a scene based solely on the initial prompt settings. Therefore, it is necessary to add prompts at several nodes in the simulation to guide the agents in completing this part of the simulation.
  - For instance, in restaurant management, if only a few management tasks (e.g., chef management, menu management) are mentioned at the beginning, agents cannot successfully complete these tasks without prompts guiding their actions before each management task.

The reason for naming it SocioSim is because we want to unify sociological simulation experiments into a single framework from both theoretical and code design perspectives. Currently, competeai is the only instance under this framework.

## Installation

**Note: the framework has only been tested on linux.**

First, clone the repo:

```bash
git clone https://github.com/microsoft/SocioSim
```

Then

```bash
cd SocioSim
```

To install the required packages, you can create a conda environment:

```powershell
conda create --name sociosim python=3.10
```

then use pip to install required packages:

```bash
pip install -r requirements.txt
```

## How to run

First, launch Django database server

```bash
./database.sh restart
```

Then, open a new terminal, input the following command: 

```bash
python run.py <exp_name>
```

The result will save into `logs/<exp_name>`

## The structure of framework

```bash
.
├── database                       <- Database management system for restaurant simulation
├── database.sh                    <- Script file for operating the database
├── logs                           <- Where all experiment results are recorded, part of the pipeline
├── README.md                      <- You are here
├── run.py                         <- Entry point for the program
├── SocioSim                       <- Core folder
│   ├── agent                     <- Core component of the framework: agent. Allows for setting up more complex agent structures
│   │   ├── agent.py               <- Completes agent observation, reaction, and execution model (essentially the process of inputting a prompt and outputting a response)
│   │   ├── backends               <- Different large models can simulate an agent, but gpt4 is generally used
│   │   │   ├── openai.py
|   |   |   └── ...
│   │   └── __init__.py
│   ├── config.py
│   ├── examples                   <- Each simulation experiment needs such a configuration file, specifying the participating agents, their roles, and the supporting LLMs
│   │   ├── group.yaml
│   │   └── restaurant.yaml
│   ├── globals.py
│   ├── image.py
│   ├── __init__.py
│   ├── message.py                 <- Core component of the framework: message. Every response made by an agent counts as a message, which includes the content of the response, the owner (agent) of the message, who can see the message, etc.
│   ├── prompt_template            <- Core component of the framework: prompt template. Prompts needed in the interaction process are given to agents at appropriate times to guide their actions
│   │   ├── dine
│   │   │   ├── comment.txt
│   │   │   ├── feeling.txt
│   │   │   └── order.txt
│   │   ├── group_dine
│   │   │   └── ...
│   │   └── restaurant_design
│   │       └── ...
│   ├── relationship.yaml
│   ├── scene                     <- Core component of the framework: scene. Each scene implements a sequence of agent interactions, such as a discussion phase among multiple customers.
│   │   ├── base.py
│   │   ├── dine.py
│   │   ├── group_dine.py
│   │   ├── __init__.py
│   │   └── restaurant_design.py
│   ├── simul.py                  <- Core file: responsible for coordinating multiple scenes to run, allowing scenes to run in any order
│   └── utils                     <- Some tools
│       ├── analysis.py
│       ├── database.py
│       ├── draw.py
│       ├── image.py
│       ├── __init__.py
│       ├── log.py
│       ├── prompt_template.py
└── test                          <- Unit test files
    ├── get_base64.py
    └── ...
```

## Acknowledgements

This project, SociosSim , is built upon the ChatArena framework. We extend our gratitude to the developers and contributors of ChatArena for providing the foundational architecture that made this project possible. For more information on ChatArena, visit [ChatArena's GitHub repository](https://github.com/Farama-Foundation/chatarena).

We adhere to the licensing terms of ChatArena, and we encourage our users to familiarize themselves with it to understand the guidelines governing the use and modification of this repo.

## Contributing

This project welcomes contributions and suggestions.  Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit https://cla.opensource.microsoft.com.

When you submit a pull request, a CLA bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., status check, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

## Trademarks

This project may contain trademarks or logos for projects, products, or services. Authorized use of Microsoft 
trademarks or logos is subject to and must follow 
[Microsoft's Trademark & Brand Guidelines](https://www.microsoft.com/en-us/legal/intellectualproperty/trademarks/usage/general).
Use of Microsoft trademarks or logos in modified versions of this project must not cause confusion or imply Microsoft sponsorship.
Any use of third-party trademarks or logos are subject to those third-party's policies.
