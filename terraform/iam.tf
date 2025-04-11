resource "aws_iam_user" "usr" {
    name = format("%s-user", var.project)
}

resource "aws_iam_access_key" "key" {
  user = aws_iam_user.usr.name
}

resource "aws_iam_user_policy" "policy" {
  name   = format("%s-policy", var.project)
  user   = aws_iam_user.usr.name
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        "Effect" = "Allow",
        "Action" = [
            "s3:*",
            "s3-object-lambda:*"
        ],
        Resource = [
            format("arn:aws:s3:::%s", var.project),
            format("arn:aws:s3:::%s/*", var.project)
        ]
      },
    ]
  })
}
