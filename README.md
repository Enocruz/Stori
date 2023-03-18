# Installation

This project is setup with Terraform, in order to deploy this code manually into an AWS account, make sure to have installed terraform and AWS CLI.
The terraform will create the following services:

- Lambda
- IAM Roles and Policies
- S3 buckets
- SES configuration

So make sure that your credentials have these access to run these services locally with TF.

## AWS CLI

```bash
aws version
```

The output should look something like this:

```bash
aws-cli/2.10.4 Python/3.9.11 Darwin/22.3.0 exe/x86_64 prompt/off
```

## Terraform

```bash
terraform --version
```

```bash
Terraform v1.3.9
on darwin_arm64
```

In the root folder run the following command:

```bash
terraform -chdir=terraform/ init
```

Or change to the terraform folder and execute:

```bash
cd terraform
terraform init
```

## Setup AWS Credentials

For this to work, you need an Access Key and a Secret Key that you can get from the AWS console. To configure AWS CLI run:

```bash
aws configure
```

You will be asked to fill the information:

```bash
AWS Access Key ID [None]: {ACCESS_KEY}
AWS Secret Access Key [None]: {SECRET_KEY}
Default region name [None]: us-west-2
Default output format [None]: json
```

## Python Setup

Make sure that you have python ^3.9 installed.

```bash
python3 --version
```

If you have python installed, create a virtual environment.

```bash
python3 -m venv venv
```

This will create a folder `venv` in the root. Make sure to activate the virtual environment using:

```bash
source venv/bin/activate
```

Once in the virtual environment, install the dependencies:

```bash
pip install -r dev-requirements.txt
```

We will only use the dev requirements to run the project locally.

# Deploying to AWS

Once you have setup your AWS credentials, in order to deploy this changes to AWS move to the terraform folder:

```bash
cd terraform
```

And run:

```bash
terraform plan -out=tfplan
```

The output will have all the changes to be applied by the TF file. To apply the changes run:

```bash
terraform apply tfplan
```

This will ask you for confirmation. Type `yes` to apply the changes. If you want to apply the changes
inmediatelly, run this.

```bash
terraform apply -auto-approve -input=false tfplan
```

There will be an output for the API GW URL created in the console

# Testing locally

You need to create all the resources with TF in order to test locally.

The file `event.json` provides an example of the body that the lambda requires.

```bash
python-lambda-local src/handler.py event_post.json
```

# Important notes

- Remember that you need to apply the TF file in order to execute the lambda locally
- You might need to change bucket names and public files (The image logo is stored in a public bucket)
- You need to add the file into the bucket with the image logo
- In the `terraform/ses.tf` there are two emails, which belong to the author. Since SES is configured in sandbox mode in AWS, we require at least two emails to make tests. Make sure
  to change these emails. When you run the TF file, you will get an email to confirm that you have access to these emails
- If you plan and apply the changes within you machine you can delete this part from the `terraform/provider.tf` file.

```json
backend "s3" {
    bucket = "terraform-cruz-test"
    key    = "state"
    region = "us-west-2"
}
```
