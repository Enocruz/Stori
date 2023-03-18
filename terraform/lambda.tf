resource "aws_iam_role" "transactions_lambda" {
  name = "transaction_lambda_role"

  assume_role_policy = <<POLICY
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": ["sts:AssumeRole"]
    }
  ]
}
POLICY
}

resource "aws_iam_role_policy_attachment" "lambda_policy" {
  role       = aws_iam_role.transactions_lambda.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_lambda_function" "transaction_lambda" {
  function_name = "transaction_lambda"

  s3_bucket = aws_s3_bucket.lambda_bucket.id
  s3_key    = aws_s3_object.transactions_lambda.key

  runtime = "python3.8"
  handler = "handler.handler"

  source_code_hash = data.archive_file.transactions_lambda_zip.output_base64sha256

  role = aws_iam_role.transactions_lambda.arn
}

resource "aws_cloudwatch_log_group" "transaction_lambda" {
  name = "/aws/lambda/${aws_lambda_function.transaction_lambda.function_name}"

  retention_in_days = 7
}

data "archive_file" "transactions_lambda_zip" {
  type = "zip"

  source_dir  = "../../${path.module}/Stori/src"
  output_path = "../../${path.module}/Stori.zip"
}

resource "aws_s3_object" "transactions_lambda" {
  bucket = aws_s3_bucket.lambda_bucket.id

  key    = "Stori.zip"
  source = data.archive_file.transactions_lambda_zip.output_path

  etag = filemd5(data.archive_file.transactions_lambda_zip.output_path)
}


data "aws_iam_policy_document" "s3_policy_document" {
  statement {
    effect    = "Allow"
    actions   = ["s3:Put*", "s3:Get*"]
    resources = ["*"]
  }
}

resource "aws_iam_policy" "policy" {
  name        = "s3-policy"
  description = "Read-write s3 policy"
  policy      = data.aws_iam_policy_document.s3_policy_document.json
}

resource "aws_iam_role_policy_attachment" "s3_policy_attachment" {
  role       = aws_iam_role.transactions_lambda.name
  policy_arn = aws_iam_policy.policy.arn
}
