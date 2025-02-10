resource "null_resource" "docker_build" {
  triggers = {
    always_run = "${timestamp()}"
  }

  provisioner "local-exec" {
    command = "DOCKER_DEFAULT_PLATFORM='linux/amd64' docker build -t backenddsp:latest -f ../backend/Dockerfile .."
  }

  provisioner "local-exec" {
    command = "aws ecr get-login-password --region ${var.region} --profile ${var.aws_profile} | docker login --username AWS --password-stdin 851725641206.dkr.ecr.ap-south-1.amazonaws.com"
  }

  provisioner "local-exec" {
    command = "docker tag backenddsp:latest ${aws_ecr_repository.backenddsp.repository_url}:latest"
  }

  provisioner "local-exec" {
    command = "docker push ${aws_ecr_repository.backenddsp.repository_url}:latest"
  }
}

resource "aws_ecr_repository" "backenddsp" {
  name                 = "backenddsp"
  image_tag_mutability = "MUTABLE"
  force_delete         = true
}

resource "aws_cloudwatch_log_group" "backenddsp" {
  name = "backenddsp"
}

resource "aws_ecs_cluster" "backenddsp" {
  name = "backenddsp"
}

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

resource "aws_iam_policy_attachment" "ecs_task_execution_policy_attachment" {
  name       = "ecs_task_execution_policy_attachment"
  roles      = [aws_iam_role.backenddsp.name]
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

data "aws_ecr_image" "backenddsp" {
  repository_name = aws_ecr_repository.backenddsp.name
  image_tag       = "latest"
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
    image     = "${aws_ecr_repository.backenddsp.repository_url}@${data.aws_ecr_image.backenddsp.image_digest}"
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

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.backenddsp.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.backenddsp.arn
  }
}
