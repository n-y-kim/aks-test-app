from fastapi import FastAPI
from opencensus.ext.azure.trace_exporter import AzureExporter
from opencensus.trace.samplers import ProbabilitySampler
from opencensus.trace.tracer import Tracer
import os

app = FastAPI()

#Get Instrumentation Key from environment variable
ikey = os.environ.get('APPINSIGHTS_INSTRUMENTATION_KEY')

tracer = Tracer(exporter=AzureExporter(connection_string=ikey), sampler=ProbabilitySampler(1.0))

#Write a simple GET method that returns 'Hello World' text
@app.get("/")
def root_get():
    with tracer.span(name="root_get") as span:
        return {"message": "Hello World"}