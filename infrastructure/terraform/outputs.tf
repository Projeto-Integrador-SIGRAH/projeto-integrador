
output "instance_id" {
  description = "ID da instância EC2"
  value       = aws_instance.project.id
}

output "public_ip" {
  description = "IP público da EC2"
  value       = aws_instance.project.public_ip
}

output "public_dns" {
  description = "DNS público da EC2"
  value       = aws_instance.project.public_dns
}

output "ssh_command" {
  description = "Comando para acessar a EC2"
  value       = "ssh -i ~/.ssh/projeto-integrador-aws ubuntu@${aws_instance.project.public_ip}"
}

output "application_url" {
  description = "URL temporária da aplicação"
  value       = "http://${aws_instance.project.public_ip}:8000"
}
