# Build and push Docker image to ECR
resource "null_resource" "docker_build" {
  triggers = {
    always_run = "${timestamp()}"
  }

  provisioner "local-exec" {
    command = "DOCKER_DEFAULT_PLATFORM='linux/amd64' docker build -t ${aws_ecr_repository.backenddsp.repository_url}:latest -f ../backend/Dockerfile ../backend"
  }

  provisioner "local-exec" {
    command = "aws ecr get-login-password --region ${var.region} --profile ${var.aws_profile} | docker login --username AWS --password-stdin ${aws_ecr_repository.backenddsp.repository_url}"
  }

  provisioner "local-exec" {
    command = "docker push ${aws_ecr_repository.backenddsp.repository_url}:latest"
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

resource "aws_security_group" "backenddsp" {
  name        = "backenddsp-sg"
  description = "Security group for backenddsp ECS service"
  vpc_id      = var.vpc_id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    from_port   = 3306
    to_port     = 3306
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
    description = "Allow backendmmr traffic"
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
    from_port   = 3000
    to_port     = 3000
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
    description = "Allow backendmmr traffic"
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
resource "aws_ecr_repository" "backenddsp" {
  name                 = "backenddsp"
  image_tag_mutability = "MUTABLE"
  force_delete         = true
}

resource "aws_ecr_repository" "frontend" {
  name                 = "frontend"
  image_tag_mutability = "MUTABLE"
  force_delete         = true
}

# CloudWatch Log Group
resource "aws_cloudwatch_log_group" "backenddsp" {
  name = "backenddsp"
}

resource "aws_cloudwatch_log_group" "frontend" {
  name = "frontend"
}

# ECS Cluster
resource "aws_ecs_cluster" "backenddsp" {
  name = "backenddsp"
}

resource "aws_ecs_cluster" "frontend" {
  name = "frontend"
}

resource "aws_iam_role" "frontend" {
  name               = "frontend"
  assume_role_policy = jsonencode({
    Version   = "2012-10-17",
    Statement = [{
      Effect    = "Allow",
      Principal = { Service = "ecs-tasks.amazonaws.com" },
      Action    = "sts:AssumeRole"
    }]
  })
}

# IAM Role for ECS Task Execution
resource "aws_iam_role" "backenddsp" {
  name               = "backenddsp"
  assume_role_policy = jsonencode({
    Version   = "2012-10-17",
    Statement = [{
      Effect    = "Allow",
      Principal = { Service = "ecs-tasks.amazonaws.com" },
      Action    = "sts:AssumeRole"
    }]
  })
}

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

# Attach the ECR policy to the backenddsp role - using role_policy_attachment instead of policy_attachment
resource "aws_iam_role_policy_attachment" "backenddsp_ecr_policy" {
  role       = aws_iam_role.backenddsp.name
  policy_arn = aws_iam_policy.ecr_policy.arn
}

# Attach the ECR policy to the frontend role
resource "aws_iam_role_policy_attachment" "frontend_ecr_policy" {
  role       = aws_iam_role.frontend.name
  policy_arn = aws_iam_policy.ecr_policy.arn
}

# Attach Execution Policy to IAM Roles - using role_policy_attachment instead of policy_attachment
resource "aws_iam_role_policy_attachment" "ecs_task_execution_policy_attachment" {
  role       = aws_iam_role.backenddsp.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

resource "aws_iam_role_policy_attachment" "ecs_task_execution_policy_attachment_frontend" {
  role       = aws_iam_role.frontend.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

resource "aws_ecs_task_definition" "backenddsp" {
  family                   = "backenddsp"
  execution_role_arn       = aws_iam_role.backenddsp.arn
  cpu                      = "1024"
  memory                   = "2048"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]

  container_definitions = jsonencode([{
    name      = "backenddsp"
    image     = "${aws_ecr_repository.backenddsp.repository_url}:latest"
    cpu       = 1024
    memory    = 2048
    essential = true
    portMappings = [{
      containerPort = 80
      hostPort      = 80
      protocol      = "tcp"
    }]
    logConfiguration = {
      logDriver = "awslogs",
      options = {
        awslogs-group         = aws_cloudwatch_log_group.backenddsp.name,
        awslogs-region        = var.region,
        awslogs-stream-prefix = "ecs"
      }
    }
  }])
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
      containerPort = 3000
      hostPort      = 3000
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
resource "aws_ecs_service" "backenddsp" {
  name                 = "backenddsp"
  cluster              = aws_ecs_cluster.backenddsp.id
  task_definition      = aws_ecs_task_definition.backenddsp.arn
  desired_count        = 1
  launch_type          = "FARGATE"
  force_new_deployment = true

  load_balancer {
    target_group_arn = aws_lb_target_group.backenddsp.arn
    container_name   = "backenddsp"
    container_port   = 80
  }
  network_configuration {
    subnets          = var.subnets
    security_groups  = [aws_security_group.backenddsp.id]
    assign_public_ip = true
  }

  lifecycle {
    create_before_destroy = true
  }
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
    container_port   = 3000
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
resource "aws_lb" "backenddsp" {
  name                       = "backenddsp-lb"
  internal                   = false
  load_balancer_type         = "application"
  security_groups            = [aws_security_group.backenddsp.id]
  subnets                    = var.subnets
  enable_deletion_protection = false
}

resource "aws_lb" "frontend" {
  name                       = "frontend-lb"
  internal                   = false
  load_balancer_type         = "application"
  security_groups            = [aws_security_group.frontend.id]
  subnets                    = var.subnets
  enable_deletion_protection = false
}

# Define the Load Balancer Target Group
resource "aws_lb_target_group" "backenddsp" {
  name        = "backenddsp-tg"
  port        = 80
  protocol    = "HTTP"
  vpc_id      = var.vpc_id
  target_type = "ip"

  health_check {
    path                = "/"
    protocol            = "HTTP"
    matcher             = "200-299"
    interval            = 30
    timeout             = 5
    healthy_threshold   = 3
    unhealthy_threshold = 3
  }
}

resource "aws_lb_target_group" "frontend" {
  name        = "frontend-tg"
  port        = 3000
  protocol    = "HTTP"
  vpc_id      = var.vpc_id
  target_type = "ip"

  health_check {
    path                = "/"
    protocol            = "HTTP"
    matcher             = "200-299"
    interval            = 30
    timeout             = 5
    healthy_threshold   = 3
    unhealthy_threshold = 3
  }
}

# Load Balancer Listener
resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.backenddsp.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.backenddsp.arn
  }
}

resource "aws_lb_listener" "frontend" {
  load_balancer_arn = aws_lb.frontend.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.frontend.arn
  }
}