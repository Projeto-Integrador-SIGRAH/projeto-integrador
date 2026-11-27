
variable "aws_region" {
  description = "Região AWS onde a infraestrutura será criada"
  type        = string
  default     = "sa-east-1"
}

variable "project_name" {
  description = "Nome do projeto"
  type        = string
  default     = "projeto-integrador"
}

variable "instance_type" {
  description = "Tipo da instância EC2"
  type        = string
  default     = "t3.small"
}

variable "admin_cidr" {
  description = "IP público autorizado a acessar SSH"
  type        = string
}

variable "public_key_path" {
  description = "Caminho da chave pública SSH"
  type        = string
  default     = "~/.ssh/projeto-integrador-aws.pub"
}

variable "volume_size" {
  description = "Tamanho do volume EBS em GB"
  type        = number
  default     = 20
}
