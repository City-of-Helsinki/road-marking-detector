resource "aws_security_group" "server" {
  name        = "${var.project}-server-${var.environment}"
  description = "Allow traffict to and from server"
  vpc_id      = aws_vpc.this.id

  ingress {
    from_port   = var.ec2_server_port
    to_port     = var.ec2_server_port
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = -1
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(
    local.common_tags,
    {
      Name = "${var.project}-server-${var.environment}"
    }
  )
}
