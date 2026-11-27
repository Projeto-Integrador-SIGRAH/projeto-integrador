
# ==========================================
# Ubuntu 24.04 LTS
# ==========================================

data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"]

  filter {
    name = "name"

    values = [
      "ubuntu/images/hvm-ssd-gp3/ubuntu-noble-24.04-amd64-server-*"
    ]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  filter {
    name   = "root-device-type"
    values = ["ebs"]
  }
}

# ==========================================
# SSH Key Pair
# ==========================================

resource "aws_key_pair" "project" {
  key_name = "${var.project_name}-key"

  public_key = file(
    pathexpand(var.public_key_path)
  )

  tags = {
    Name = "${var.project_name}-key"
  }
}

# ==========================================
# Security Group
# ==========================================

resource "aws_security_group" "project" {
  name        = "${var.project_name}-sg"
  description = "Security Group do Projeto Integrador"

  # SSH - somente IP autorizado
  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # HTTP
  ingress {
    description = "HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # HTTPS
  ingress {
    description = "HTTPS"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Django - acesso temporário para testes
  ingress {
    description = "Django application - temporary"
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Saída para internet
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.project_name}-sg"
  }
}

# ==========================================
# EC2 Instance
# ==========================================

resource "aws_instance" "project" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = var.instance_type

  key_name = aws_key_pair.project.key_name

  vpc_security_group_ids = [
    aws_security_group.project.id
  ]

  associate_public_ip_address = true

  root_block_device {
    volume_size           = var.volume_size
    volume_type           = "gp3"
    encrypted             = true
    delete_on_termination = true
  }

  user_data = <<-EOF
    #!/bin/bash

    set -euxo pipefail

    # Atualiza pacotes
    apt-get update -y

    # Instala dependências
    apt-get install -y ca-certificates curl

    # Configura repositório oficial do Docker
    install -m 0755 -d /etc/apt/keyrings

    curl -fsSL https://download.docker.com/linux/ubuntu/gpg \
      -o /etc/apt/keyrings/docker.asc

    chmod a+r /etc/apt/keyrings/docker.asc

    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
      $(. /etc/os-release && echo "$${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" \
      > /etc/apt/sources.list.d/docker.list

    # Instala Docker Engine e Compose
    apt-get update -y

    apt-get install -y \
      docker-ce \
      docker-ce-cli \
      containerd.io \
      docker-buildx-plugin \
      docker-compose-plugin

    # Habilita Docker
    systemctl enable docker
    systemctl start docker

    # Permite que o usuário ubuntu execute Docker
    usermod -aG docker ubuntu

    # Cria diretório de deploy
    mkdir -p /opt/projeto-integrador

    chown -R ubuntu:ubuntu /opt/projeto-integrador

    # Finaliza
    docker --version
    docker compose version
  EOF

  tags = {
    Name        = var.project_name
    Environment = "production"
    ManagedBy   = "Terraform"
  }

  depends_on = [
    aws_key_pair.project,
    aws_security_group.project
  ]
}
