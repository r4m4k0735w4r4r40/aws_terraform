resource "aws_api_gateway_rest_api" "booking" {
  name        = "MyDemoAPI"
  description = "This is my API for demonstration purposes"
}

resource "aws_api_gateway_resource" "signup_resource" {
  rest_api_id = aws_api_gateway_rest_api.booking.id
  parent_id   = aws_api_gateway_rest_api.booking.root_resource_id
  path_part   = "signup"
}

resource "aws_api_gateway_method" "signup_method" {
  rest_api_id   = aws_api_gateway_rest_api.booking.id
  resource_id   = aws_api_gateway_resource.signup_resource.id
  http_method   = "POST"
  authorization = "NONE"
}
resource "aws_api_gateway_integration" "signup_integration" {
  rest_api_id             = aws_api_gateway_rest_api.booking.id
  resource_id             = aws_api_gateway_resource.signup_resource.id
  http_method             = aws_api_gateway_method.signup_method.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.signup_lambda.invoke_arn
}

resource "aws_api_gateway_resource" "signin_resource" {
  rest_api_id = aws_api_gateway_rest_api.booking.id
  parent_id   = aws_api_gateway_rest_api.booking.root_resource_id
  path_part   = "signin"
}

resource "aws_api_gateway_method" "signin_method" {
  rest_api_id   = aws_api_gateway_rest_api.booking.id
  resource_id   = aws_api_gateway_resource.signin_resource.id
  http_method   = "POST"
  authorization = "NONE"
}
resource "aws_api_gateway_integration" "signin_integration" {
  rest_api_id             = aws_api_gateway_rest_api.booking.id
  resource_id             = aws_api_gateway_resource.signin_resource.id
  http_method             = aws_api_gateway_method.signin_method.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.signin_lambda.invoke_arn
}

resource "aws_api_gateway_resource" "booking_resource" {
  rest_api_id = aws_api_gateway_rest_api.booking.id
  parent_id   = aws_api_gateway_rest_api.booking.root_resource_id
  path_part   = "booking"
}

resource "aws_api_gateway_method" "booking_method" {
  rest_api_id   = aws_api_gateway_rest_api.booking.id
  resource_id   = aws_api_gateway_resource.booking_resource.id
  http_method   = "POST"
  authorization = "NONE"
}
resource "aws_api_gateway_integration" "booking_integration" {
  rest_api_id             = aws_api_gateway_rest_api.booking.id
  resource_id             = aws_api_gateway_resource.booking_resource.id
  http_method             = aws_api_gateway_method.booking_method.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.booking_lambda.invoke_arn
}

resource "aws_api_gateway_resource" "booking_his_resource" {
  rest_api_id = aws_api_gateway_rest_api.booking.id
  parent_id   = aws_api_gateway_rest_api.booking.root_resource_id
  path_part   = "booking-history"
}

resource "aws_api_gateway_method" "booking_his_method" {
  rest_api_id   = aws_api_gateway_rest_api.booking.id
  resource_id   = aws_api_gateway_resource.booking_his_resource.id
  http_method   = "GET"
  authorization = "NONE"
}
resource "aws_api_gateway_integration" "booking_his_integration" {
  rest_api_id             = aws_api_gateway_rest_api.booking.id
  resource_id             = aws_api_gateway_resource.booking_his_resource.id
  http_method             = aws_api_gateway_method.booking_his_method.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.booking_his_lambda.invoke_arn
}
resource "aws_api_gateway_deployment" "dev" {
  rest_api_id = aws_api_gateway_rest_api.booking.id

  triggers = {
    redeployment = sha1(jsonencode([
      aws_api_gateway_resource.signup_resource.id,
      aws_api_gateway_method.signup_method.id,
      aws_api_gateway_integration.signup_integration.id,
      aws_api_gateway_resource.signin_resource.id,
      aws_api_gateway_method.signin_method.id,
      aws_api_gateway_integration.signin_integration.id,
      aws_api_gateway_resource.booking_resource,
      aws_api_gateway_method.booking_method,
      aws_api_gateway_integration.booking_integration,
      aws_api_gateway_resource.booking_his_resource,
      aws_api_gateway_method.booking_his_method,
      aws_api_gateway_integration.booking_his_integration
    ]))
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_api_gateway_stage" "example" {
  deployment_id = aws_api_gateway_deployment.dev.id
  rest_api_id   = aws_api_gateway_rest_api.booking.id
  stage_name    = "dev"
}