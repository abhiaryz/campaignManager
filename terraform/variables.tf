variable "region" {
  description = "AWS region"
  type        = string
  default     = "ap-south-1"
}

variable "aws_profile" {
  description = "Name of your AWS profile"
  type        = string
  default     = "aws-dsp"
}

variable "application_name" {
  description = "Name of the application"
  type        = string
  default     = "dsp-backend"
}


