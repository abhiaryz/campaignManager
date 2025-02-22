output "backend_url" {
  description = "URL to access the deployed container"
  value       = "http://${aws_lb.backend.dns_name}"
}
