output "backenddsp_url" {
  description = "URL to access the deployed container"
  value       = "http://${aws_lb.backenddsp.dns_name}"
}
