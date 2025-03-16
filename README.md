# Tactical Analysis AI

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Anaconda](https://img.shields.io/badge/Anaconda-%2344A833.svg?style=for-the-badge&logo=anaconda&logoColor=white)
![Poetry](https://img.shields.io/badge/Poetry-%233B82F6.svg?style=for-the-badge&logo=poetry&logoColor=0B3D8D)


## Python Versions

![](https://img.shields.io/badge/python-_>=3.10_|_<4.0_-blue)


### **Motivation**

   -

### **Main Goal**

   -

---

## Quickstart

### 1. Clone Github repository

   - Clone this repo using **HTTPS** or using **SSH**:

   ```bash
   # 1. With HTTPS
   git clone https://github.com/dark-theme-org/tactical_analysis_ai.git

   # 2. With SSH
   git clone git@github.com:dark-theme-org/tactical_analysis_ai.git
   ```

### 2. Virtual Environment

   - If you don't have [Miniconda](https://docs.conda.io/en/latest/miniconda.html#linux-installers) installed:

        ```bash
        bash Miniconda3-latest-Linux-x86_64.sh
        ```

   - Create a *virtual environment* using `conda create` and specify your **Python version** with an allowed one.

        ```bash
        cd path/to/github/tactical_analysis_ai
        conda create --name=tactical_aai_env python=3.13
        ```

   - Launch the venv

        ```bash
        conda activate tactical_aai_env
        ```

   - If necessary, configure *./src* folder as **PYTHONPATH** (for local development)

        ```bash
        export PYTHONPATH="$PWD/src"
        ```

### 3. Poetry

   - If don't have `poetry` already, [install it](https://python-poetry.org/docs/#osx--linux--bashonwindows-install-instructions). For this project, we're using `poetry-1.5.1`. Check your poetry version with `poetry --version` before... if version is different, then clear cache, update version and start development!

   ```bash
   poetry cache clear --all .
   poetry self update 1.5.1
   poetry lock --no-update
   rm -rf ~/Library/Caches/pypoetry/artifacts/
   rm -rf ~/Library/Caches/pypoetry/cache/
   rm -rf ~/Library/Caches/pypoetry/virtualenvs/
   poetry install
   ```

### 4. Pre-commit

   - This project uses `pre-commit` hooks in order to keep the code consistent and properly structured. After clonning the repo, check the next steps:

      - If you have a previous configuration, **uninstall** with:

      ```bash
      poetry run pre-commit uninstall
      ```

      - After that, **install** the project settings:

      ```bash
      poetry run pre-commit install --config .pre-commit-config.yaml --overwrite
      ```

      - To **clean** out pre-commit files, run:

      ```bash
      poetry run pre-commit clean
      ```

      - After it, execute **autoupdate** to update the latest repos' versions:

      ```bash
      poetry run pre-commit autoupdate
      ```

   #### 4.1 Run all hooks (without git commit):

   - You can run the pre-commit hooks **without the need to commit** to Github. For this, just execute the following command:

   ```bash
   poetry run pre-commit run --config .pre-commit-config.yaml --all-files
   ```

   #### 4.2 Run a specific hook:

   - If any hook is failing and you don't want to execute all the steps, you can run a **specific id** by accessing the [.pre-commit-config.yaml](/.pre-commit-config.yaml) file and execute the `entry` command in your terminal.

---