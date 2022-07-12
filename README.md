## Project Directory

- The **app** directory is the main project directory
- Includes all py files within that directory
- main.py is the triggering py file
- run all other py files through main.py
- Include all libraries in requirements.txt with appropriate version

## Steps to run the project in LINUX

1. Install Docker (https://docs.docker.com/engine/install/)
2. Navigate to the terminal and run the following commands:
    - docker image build -t token_name .
    - docker run -e flag=task_string token_name
    
    (flag=task-string will is an argument will get passed to the main.py)
    (flag=model will invoke a certain function which might be used to create a BERT model)
    (flag=data will invoke a certain function which might be used to pull tweets)

## Note
- Windows and Mac users, please write commands to build/run the docker in respective system
