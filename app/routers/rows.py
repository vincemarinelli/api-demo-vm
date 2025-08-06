from datetime import date, datetime
from decimal import Decimal
from fastapi import APIRouter, HTTPException
from services.athena import get_athena_conn
import boto3
from config import settings


router = APIRouter()

def _cast_and_clean(val):

    if val is None:
        return None
    
    if isinstance(val, Decimal):
        return int(val) if val == val.to_integral() else float(val)
    
    if isinstance(val, (date, datetime)):
        return val.isoformat()
    
    if isinstance(val, bytes):
        val = val.decode("utf-8")

    if isinstance(val, str):
        return val.strip('"')
    
    return val


@router.get("/rows")
def read_rows(limit: int = 10):
    sql = f"SELECT * FROM {settings.athena_database}.{settings.athena_table} LIMIT {limit}"
    conn = get_athena_conn()
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    cols = [col[0] for col in cursor.description]
    rows = cursor.fetchall()

    results = []
    for row in rows:
        record = {}
        for col, val in zip(cols, row):
            record[col] = _cast_and_clean(val)
        results.append(record)

        
    return results


# @router.get("/buckets")
# def list_buckets():
#     session = boto3.Session(
#         profile_name=settings.aws_profile,
#         region_name=settings.aws_region
#     )
#     s3 = session.client("s3")
#     resp = s3.list_buckets()
#     return [b["Name"] for b in resp.get("Buckets", [])]

# @router.get("/databases")
# def list_databases():
#     cur = get_athena_conn().cursor()
#     cur.execute("SHOW DATABASES")
#     return [row[0] for row in cur.fetchall()]

# @router.get("/tables/{database}")
# def list_tables(database: str):
#     cur = get_athena_conn().cursor()
#     cur.execute(f"SHOW TABLES IN {database}")
#     return [row[0] for row in cur.fetchall()]