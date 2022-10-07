resource "aws_glue_catalog_database" "customer_data" {
  name = "customer_data"
}
resource "aws_glue_catalog_database" "aws_glue_catalog_database" {
  name = "my_catalog_database"

  target_database {
    catalog_id    = "131069340413"
    database_name = "customer_data"
  }
}