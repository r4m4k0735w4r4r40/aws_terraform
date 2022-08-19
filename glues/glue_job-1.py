import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

args = getResolvedOptions(sys.argv, ["JOB_NAME"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# Script generated for node Data Source
DataSource_node1660717439184 = glueContext.create_dynamic_frame.from_catalog(
    database="customer_data",
    table_name="data",
    transformation_ctx="DataSource_node1660717439184",
)

# Script generated for node Mapping Data
MappingData_node1660717467477 = ApplyMapping.apply(
    frame=DataSource_node1660717439184,
    mappings=[
        ("customerid", "long", "customerid", "long"),
        ("namestyle", "boolean", "namestyle", "boolean"),
        ("title", "string", "title", "string"),
        ("firstname", "string", "firstname", "string"),
        ("middlename", "string", "middlename", "string"),
        ("lastname", "string", "lastname", "string"),
        ("suffix", "string", "suffix", "string"),
        ("companyname", "string", "companyname", "string"),
        ("salesperson", "string", "salesperson", "string"),
        ("emailaddress", "string", "emailaddress", "string"),
        ("phone", "string", "phone", "string"),
        ("passwordhash", "string", "passwordhash", "string"),
        ("passwordsalt", "string", "passwordsalt", "string"),
        ("rowguid", "string", "rowguid", "string"),
        ("modifieddate", "string", "modifieddate", "string"),
    ],
    transformation_ctx="MappingData_node1660717467477",
)

glueContext.write_dynamic_frame_from_options(
    frame=MappingData_node1660717467477,
    connection_type="dynamodb",
    connection_options={
        "dynamodb.output.tableName": "glue-table-1",
        "dynamodb.throughput.write.percent": "1.0"
    }
)
# glueContext.write_dynamic_frame.from_options(
#     frame =DynamicFrame.fromDF(df, glueContext, "final_df"),
#     connection_type = "dynamodb",
#     connection_options = {"tableName": "glue_table"})

job.commit()
