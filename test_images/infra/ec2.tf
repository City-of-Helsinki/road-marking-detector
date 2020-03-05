resource "aws_key_pair" "this" {
  key_name   = "${var.project}-default-${var.environment}"
  public_key = file("${path.module}/instance-public.key")
}

resource "aws_instance" "server" {
  count         = var.ec2_instance_count
  ami           = data.aws_ami.ubuntu-18_04-ml.id
  instance_type = var.ec2_instance_type
  key_name      = aws_key_pair.this.key_name
  subnet_id     = aws_subnet.public[0].id

  vpc_security_group_ids = [
    aws_security_group.server.id
  ]

  associate_public_ip_address = true

  tags = merge(
    local.common_tags,
    {
      Name = "${var.project}-server-${var.environment}"
      OS   = "Ubuntu Linux"
    }
  )
}

data "template_file" "jupyter-service" {
  template = file("provision/jupyter-notebook.service")
  vars = {
    jupyter_port = var.ec2_server_port
  }
}

resource "null_resource" "provisioner" {
  count = var.ec2_instance_count

  connection {
    host        = aws_eip.server[count.index].public_ip
    type        = "ssh"
    user        = "ubuntu"
    private_key = file("${path.module}/instance-private.key")
  }

  triggers = {
    init_sha1    = sha1(file("provision/server-init.sh"))
    service_sha1 = sha1(file("provision/jupyter-notebook.service"))
  }

  provisioner "file" {
    content     = data.template_file.jupyter-service.rendered
    destination = "/tmp/jupyter-notebook.service"
  }

  provisioner "remote-exec" {
    script = "provision/server-init.sh"
  }
}

resource "aws_eip" "server" {
  count    = var.ec2_instance_count
  vpc      = true
  instance = aws_instance.server[count.index].id

  tags = merge(
    local.common_tags,
    {
      Name = "${var.project}-server-${var.environment}"
    }
  )
}

output "ec2_public_ip" {
  description = "Public IP of the Web server"
  value       = aws_eip.server.*.public_ip
}

output "ec2_public_dns" {
  description = "Public DNS of the Web server"
  value       = aws_eip.server.*.public_dns
}
