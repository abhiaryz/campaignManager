output "backenddsp_url" {
  description = "URL to access the deployed container"
  value       = "http://${aws_lb.backenddsp.dns_name}"
}

output "frontend_url" {
  description = "URL to access the deployed container"
  value       = "http://${aws_lb.frontend.dns_name}"
}
