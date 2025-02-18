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
}

resource "aws_security_group" "backenddsp" {
  name        = "backenddsp-sg"
  description = "Security group for backenddsp ECS service"
  vpc_id      = var.vpc_id

  ingress {
    from_port   = 8000
    to_port     = 8000
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

# CloudWatch Log Group
resource "aws_cloudwatch_log_group" "backenddsp" {
  name = "backenddsp"
}

# ECS Cluster
resource "aws_ecs_cluster" "backenddsp" {
  name = "backenddsp"
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

# Attach Execution Policy to IAM Role
resource "aws_iam_policy_attachment" "ecs_task_execution_policy_attachment" {
  name       = "ecs_task_execution_policy_attachment"
  roles      = [aws_iam_role.backenddsp.name]
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

# ECS Task Definition using ECR image
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
      containerPort = 8000
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

# ECS Service to run the task
resource "aws_ecs_service" "backenddsp" {
  name            = "backenddsp"
  cluster         = aws_ecs_cluster.backenddsp.id
  task_definition = aws_ecs_task_definition.backenddsp.arn
  desired_count   = 1
  launch_type     = "FARGATE"
  force_new_deployment = true

  load_balancer {
    target_group_arn = aws_lb_target_group.backenddsp.arn
    container_name   = "backenddsp"
    container_port   = 8000
  }
  network_configuration {
    subnets         = var.subnets
    security_groups = [aws_security_group.backenddsp.id]
    assign_public_ip = true
  }

  lifecycle {
    create_before_destroy = true
  }
}

# Define the Load Balancer (example)
resource "aws_lb" "backenddsp" {
  name               = "backenddsp-lb"
  internal           = false
  load_balancer_type = "application"
  security_groups   = [aws_security_group.backenddsp.id]
  subnets            = var.subnets
  enable_deletion_protection = false
}

# Define the Load Balancer Target Group
resource "aws_lb_target_group" "backenddsp" {
  name     = "backenddsp-tg"
  port     = 8000
  protocol = "HTTP"
  vpc_id   = var.vpc_id
  target_type = "ip"
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

