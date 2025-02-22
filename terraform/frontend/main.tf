resource "null_resource" "Frontend_build" {
  triggers = {
    sha1 = join("", [for f in fileset("../frontend", "**/*") : filesha1("../frontend/${f}")])
  }
  provisioner "local-exec" {
    command = "DOCKER_DEFAULT_PLATFORM='linux/amd64' docker build -t ${aws_ecr_repository.frontend.repository_url}:latest -f ../frontend/Dockerfile ../frontend"
  }

  provisioner "local-exec" {
    command = "aws ecr get-login-password --region ${var.region} --profile ${var.aws_profile} | docker login --username AWS --password-stdin ${aws_ecr_repository.frontend.repository_url}"
  }

  provisioner "local-exec" {
    command = "docker push ${aws_ecr_repository.frontend.repository_url}:latest"
  }
}

# Build and push Docker image to ECR

resource "aws_security_group" "frontend" {
  name        = "frontend-sg"
  description = "Security group for frontend ECS service"
  vpc_id      = var.vpc_id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    description = "Allow HTTPS traffic"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    description = "Allow frontend traffic"
    from_port   = 587
    to_port     = 587
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"  # All traffic
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# ECR Repository to store the Docker image

resource "aws_ecr_repository" "frontend" {
  name                 = "frontend"
  image_tag_mutability = "MUTABLE"
  force_delete         = true
}

# CloudWatch Log Group


resource "aws_cloudwatch_log_group" "frontend" {
  name = "frontend"
}

# ECS Cluster


resource "aws_ecs_cluster" "frontend" {
  name = "frontend"
}

resource "aws_iam_role" "frontend" {
  name = "frontend-ecs-role"
  path = "/"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "ecs-tasks.amazonaws.com"
      }
    }]
  })

  tags = {
    Name = "frontend-ecs-role"
    Environment = var.environment
  }

}

# IAM Role for ECS Task Execution


# Create an IAM policy for ECR access
resource "aws_iam_policy" "ecr_policy" {
  name = "ecr-access-policy"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "ecr:GetAuthorizationToken",
          "ecr:BatchCheckLayerAvailability",
          "ecr:GetDownloadUrlForLayer",
          "ecr:BatchGetImage"
        ]
        Resource = "*"
      }
    ]
  })
}



# Attach the ECR policy to the frontend role
resource "aws_iam_role_policy_attachment" "frontend_ecr_policy" {
  role       = aws_iam_role.frontend.name
  policy_arn = aws_iam_policy.ecr_policy.arn
}

# Attach Execution Policy to IAM Roles - using role_policy_attachment instead of policy_attachment


resource "aws_iam_role_policy_attachment" "ecs_task_execution_policy_attachment_frontend" {
  role       = aws_iam_role.frontend.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
  
  depends_on = [
    aws_iam_role.frontend
  ]
}


# Add additional required policies
resource "aws_iam_role_policy" "frontend_additional" {
  name = "frontend-additional"
  role = aws_iam_role.frontend.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "ecs:ListTasks",
          "ecs:DescribeTasks",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "*"
      }
    ]
  })

  depends_on = [
    aws_iam_role.frontend
  ]
}


resource "aws_ecs_task_definition" "frontend" {
  family                   = "frontend"
  execution_role_arn       = aws_iam_role.frontend.arn
  cpu                      = "1024"
  memory                   = "2048"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]

  container_definitions = jsonencode([{
    name      = "frontend"
    image     = "${aws_ecr_repository.frontend.repository_url}:latest"
    cpu       = 1024
    memory    = 2048
    essential = true
    environment = [
      {
        name  = "NEXT_PUBLIC_API_BASE_URL"
        value = "http://${aws_lb.backenddsp.dns_name}"
      }
    ]
    portMappings = [{
      containerPort = 80
      hostPort      = 80
      protocol      = "tcp"
    }]
    logConfiguration = {
      logDriver = "awslogs",
      options = {
        awslogs-group         = aws_cloudwatch_log_group.frontend.name,
        awslogs-region        = var.region,
        awslogs-stream-prefix = "ecs"
      }
    }
  }])
}

# ECS Service to run the task


resource "aws_iam_policy" "terraform_state" {
  name = "terraform-state-access"
  
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:ListBucket",
          "s3:GetObject",
          "s3:PutObject",
          "s3:DeleteObject"
        ]
        Resource = [
          "arn:aws:s3:::digiinflunecer-tf-state",
          "arn:aws:s3:::digiinflunecer-tf-state/*"
        ]
      },
      {
        Effect = "Allow"
        Action = [
          "dynamodb:GetItem",
          "dynamodb:PutItem",
          "dynamodb:DeleteItem"
        ]
        Resource = "arn:aws:dynamodb:*:*:table/terraform-lock"
      }
    ]
  })
}


resource "aws_ecs_service" "frontend" {
  name                 = "frontend"
  cluster              = aws_ecs_cluster.frontend.id
  task_definition      = aws_ecs_task_definition.frontend.arn
  desired_count        = 1
  launch_type          = "FARGATE"
  force_new_deployment = true

  load_balancer {
    target_group_arn = aws_lb_target_group.frontend.arn
    container_name   = "frontend"
    container_port   = 80
  }
  network_configuration {
    subnets          = var.subnets
    security_groups  = [aws_security_group.frontend.id]
    assign_public_ip = true
  }

  lifecycle {
    create_before_destroy = true
  }
}

# Define the Load Balancer


resource "aws_lb" "frontend" {
  name                       = "frontend-lb"
  internal                   = false
  load_balancer_type         = "application"
  security_groups            = [aws_security_group.frontend.id]
  subnets                    = var.subnets
  enable_deletion_protection = false
}

# Define the Load Balancer Target Group


resource "aws_lb_target_group" "frontend" {
  name        = "frontend-tg"
  port        = 80
  protocol    = "HTTP"
  vpc_id      = var.vpc_id
  target_type = "ip"

  health_check {
    enabled             = true
    path                = "/api/health"  # Create this endpoint in your Next.js app
    protocol            = "HTTP"
    matcher             = "200-399"      # Allow more status codes
    interval            = 60             # Check every 60 seconds
    timeout             = 30             # Wait up to 30 seconds
    healthy_threshold   = 2              # Number of consecutive successes
    unhealthy_threshold = 5              # Number of consecutive failures
  }

  lifecycle {
    create_before_destroy = true
  }
}

# Load Balancer Listener


resource "aws_lb_listener" "frontend" {
  load_balancer_arn = aws_lb.frontend.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.frontend.arn
  }
}