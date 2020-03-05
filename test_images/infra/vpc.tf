resource "aws_eip" "nat-gateway" {
  vpc = true

  tags = merge(
    local.common_tags,
    {
      Name = "${var.project}-nat-gateway-${var.environment}"
    }
  )
}

resource "aws_vpc" "this" {
  cidr_block           = var.vpc_cidr
  instance_tenancy     = "default"
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = merge(
    local.common_tags,
    {
      Name = "${var.project}-main-${var.environment}"
    }
  )
}

resource "aws_subnet" "public" {
  count = 1

  vpc_id            = aws_vpc.this.id
  cidr_block        = var.public_subnet_cidrs[count.index]
  availability_zone = data.aws_availability_zones.available.names[count.index]

  tags = merge(
    local.common_tags,
    {
      Name = "${var.project}-public${count.index + 1}-${var.environment}"
    }
  )
}

resource "aws_subnet" "private" {
  count = 1

  vpc_id            = aws_vpc.this.id
  cidr_block        = var.private_subnet_cidrs[count.index]
  availability_zone = data.aws_availability_zones.available.names[count.index]

  tags = merge(
    local.common_tags,
    {
      Name = "${var.project}-private${count.index + 1}-${var.environment}"
    }
  )
}

resource "aws_internet_gateway" "this" {
  vpc_id = aws_vpc.this.id

  tags = merge(
    local.common_tags,
    {
      Name = "${var.project}-main-${var.environment}"
    }
  )
}

resource "aws_nat_gateway" "this" {
  subnet_id     = aws_subnet.public[0].id
  allocation_id = aws_eip.nat-gateway.id

  tags = merge(
    local.common_tags,
    {
      Name = "${var.project}-main-${var.environment}"
    }
  )
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.this.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.this.id
  }

  tags = merge(
    local.common_tags,
    {
      Name = "${var.project}-public-${var.environment}"
    }
  )
}

resource "aws_route_table_association" "pubic" {
  count = 1

  subnet_id      = aws_subnet.public[count.index].id
  route_table_id = aws_route_table.public.id
}

resource "aws_route_table" "private" {
  vpc_id = aws_vpc.this.id

  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.this.id
  }

  tags = merge(
    local.common_tags,
    {
      Name = "${var.project}-private-${var.environment}"
    }
  )
}

resource "aws_route_table_association" "private" {
  count = 1

  subnet_id      = aws_subnet.private[count.index].id
  route_table_id = aws_route_table.private.id
}
