import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Script generated for node last_names
last_names_node1743868546324 = glueContext.create_dynamic_frame.from_options(format_options={"quoteChar": "\"", "withHeader": True, "separator": ",", "optimizePerformance": False}, connection_type="s3", format="csv", connection_options={"paths": ["s3://329645823635-data-engineering/inputs/first_names.csv"]}, transformation_ctx="last_names_node1743868546324")

# Script generated for node first_names
first_names_node1743868925726 = glueContext.create_dynamic_frame.from_options(format_options={"quoteChar": "\"", "withHeader": True, "separator": ",", "optimizePerformance": False}, connection_type="s3", format="csv", connection_options={"paths": ["s3://329645823635-data-engineering/inputs/last_names.csv"]}, transformation_ctx="first_names_node1743868925726")

# Script generated for node Join
Join_node1743868968197 = Join.apply(frame1=first_names_node1743868925726, frame2=last_names_node1743868546324, keys1=["id"], keys2=["id"], transformation_ctx="Join_node1743868968197")

# Script generated for node drop_fields
drop_fields_node1743869088314 = ApplyMapping.apply(frame=Join_node1743868968197, mappings=[("lname", "string", "lname", "string"), ("fname", "string", "fname", "string"), ("id", "string", "id", "string")], transformation_ctx="drop_fields_node1743869088314")

# Script generated for node save_data
save_data_node1743869125682 = glueContext.write_dynamic_frame.from_options(frame=drop_fields_node1743869088314, connection_type="s3", format="glueparquet", connection_options={"path": "s3://329645823635-data-engineering/outputs/", "partitionKeys": []}, format_options={"compression": "snappy"}, transformation_ctx="save_data_node1743869125682")

job.commit()