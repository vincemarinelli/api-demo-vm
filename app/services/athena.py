from pyathena import connect
from config import settings

def get_athena_conn():
    return connect(
        profile_name=settings.aws_profile,
        region_name=settings.aws_region,
        s3_staging_dir=settings.athena_s3_staging_dir,
        schema_name=settings.athena_database,
        verify=settings.ssl_flag,
    )