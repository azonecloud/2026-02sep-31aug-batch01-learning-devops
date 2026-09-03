resource "aws_s3_bucket" "my_bucket" {
  bucket = <<PLACE_WHAT_EVER_NAME_YOU_WANT_TO_USE_FOR_YOUR_BUCKET>>
  #bucket = var.bucket_name
  
  tags = {
    Name        = "My bucket"
    Environment = "Dev"
  }
}

resource "aws_s3_bucket" "my_bucket" {
  bucket = "xmainbt-usin-tf-and-jenkins"

}