# Terraform

![Terraform](https://img.shields.io/badge/terraform-%235835CC.svg?style=for-the-badge&logo=terraform&logoColor=white)

## Tutorial

- The core **Terraform** workflow consists of **3 MAIN STEPS** after you have written your `*.tf` files:

    - **Init**: Prepares your workspace to apply your configuration;
    - **Plan**: Allows you to preview the changes will be made before you apply them;
    - **Apply**: Makes the changes defined by your **Plan** to create, update, or destroy resources.

So, to execute each step, go to `terraform` folder with:

```bash
cd to/folder/path/terraform
```

### 1. Initialize your configuration

- In order to generate your execution plan, **Terraform** needs to install the *providers* and *modules* referenced by your configurations. For this, you should execute the following command:

```bash
AWS_ACCESS_KEY_ID={{YOUR_AWS_ACCESS_KEY_ID}} \
AWS_SECRET_ACCESS_KEY={{YOUR_AWS_SECRET_ACCESS_KEY}} \
terraform init -backend-config "key=production/{{PROJECT_NAME}}/terraform.tfstate"
```

### 2. Validate modifications

- In order to ensure the required actions, a `validate` step is executed to check when a configuration is *syntactically valid* and *internally consistent*. It is primarily useful for general verification of reusable modules, including correctness of attribute names and value types. To check this, you can basically run:

```bash
terraform validate
```

### 3. Create a plan

- After that, **Terraform** can create a **Plan**, consisting of a set of changes that will make your resources match your configuration. This lets you preview the actions would take to modify your infrastructure before applying them. To generate a `plan`, just execute:

```bash
terraform plan -out tfplan.out
```

### 4. Apply

- Finally, you must `apply` the proposed changes according to what was visualized in the **Plan** phase. To do this, simply run the following:

```bash
terraform apply -auto-approve tfplan.out
```
