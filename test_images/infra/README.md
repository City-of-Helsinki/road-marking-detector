# Infrastructure
This brings up an EC2 instance of AWS Deep Learning AMI (Ubuntu 18.04) with Tesla V100 GPU to train the ML model

## Setup
1. Clone the repository and go to `infra` folder.
2. Create a file called `terraform.tfvars` and put in it following information:
```
aws_region = "us-east-1"
aws_access_key = "<access_key>"
aws_secret_key = "<secret_key>"
```

Where `<access_key>` and `<secret_key>` are credentials of AWS IAM user which has been created and given to you (please ask Tekendra)

3. Run `terraform init`
4. NOTE: If you get errors with the above `terraform init` command, follow these steps:
* Open your AWS credentials file at `$HOME/.aws/credentials`
* Update it with following details:
```
[default]
aws_access_key_id = <access_key>
aws_secret_access_key = <secret_key>
```

where `<access_key>` and `<secret_key>` are the same ones above.
If you already have a default profile (e.g, with `[default]`), change it to something else, for example, `[personal]`) as we can have only one default profile.
* Repeat step 3.

## Instructions
* Get the DNS of the instance:
`echo aws_eip.server.*.public_dns | terraform console`.

* Open Jupyter notebook on the instance (make sure the instance is started):
`./jupyter-notebook.sh`. Use password: `HelPedestorML19`.

* SSH to the EC2 instance:
`./ssh.sh`
You can also run a command redirectly without entering the machine. For example:
`./ssh.sh ls /home/ubuntu/`

* Copy file/folder to instance:
`scp -i instance-private.key <source> ubuntu@<pubic_dns>:<target>`
For example, `scp -i instance-private.key /tmp/data.csv ubuntu@<public_dns>:/home/ubuntu`

* Start the instance:
`./start-instance.sh`

* Stop the instance:
`./stop-instance.sh`
It's recommended that you STOP the instance when you're not running the training to save cost.
