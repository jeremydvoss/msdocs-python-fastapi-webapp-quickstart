# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License in the project root for
# license information.
# --------------------------------------------------------------------------

from os import environ
from opentelemetry import trace
import logging
import requests

import fastapi
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import uvicorn

app = fastapi.FastAPI()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

@app.get("/")
async def server_request():
    logger.info("request page")
    return {"message": "FastAPI App"}

@app.get("/dependencies")
async def dependencies_request():
    requests.get('https://learn.microsoft.com/en-us/azure/azure-monitor/app/opentelemetry-enable?tabs=python')
    return {"message": "dependencies"}

@app.get("/exceptions")
async def exception_request():
    logger.info("request page")
    try:
        raise Exception('Test Error')
    except Exception as e:
        logger.error(e)
    try:
        raise Exception('Test Exception')
    except Exception as e:
        logger.exception(e)
    # Use these manual events until events exporter is added.
    produce_trace_and_exception_events()
    requests.get('https://httpstat.us/400')
    return JSONResponse(status_code=500, content=jsonable_encoder({"code": 500, "msg": "Internal Server Error"}))

def test_import_attach_dependencies():
    import asgiref
    import certifi
    import charset_normalizer
    import deprecated
    import fixedint
    import idna
    import importlib_metadata
    import isodate
    import msrest
    import oauthlib
    import packaging
    import psutil
    import requests
    import six
    import typing_extensions
    import urllib3
    import wrapt
    import zipp

def produce_trace_and_exception_events():
    tracer = trace.get_tracer(__name__)

    # Trace message events
    with tracer.start_as_current_span("hello") as span:
        span.add_event("Custom event", {"test": "attributes"})
    
    # Exception events
    try:
        with tracer.start_as_current_span("hello") as span:
            raise Exception("Custom exception message.")
    except Exception:
        print("Exception raised")

if __name__ == "__main__":
    test_import_attach_dependencies()
    port = environ["PYTHON_TEST_APP_PORT"]
    print("Server running at port: %s" % port)
    uvicorn.run("test_app:app", port=port, reload=True)
