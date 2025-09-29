from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import numpy as np

# Sample telemetry data
telemetry = [
    {"region":"apac","service":"payments","latency_ms":136.78,"uptime_pct":97.449,"timestamp":20250301},
    {"region":"apac","service":"recommendations","latency_ms":154.31,"uptime_pct":98.656,"timestamp":20250302},
    {"region":"apac","service":"analytics","latency_ms":206.55,"uptime_pct":97.976,"timestamp":20250303},
    {"region":"apac","service":"catalog","latency_ms":188.11,"uptime_pct":98.974,"timestamp":20250304},
    {"region":"apac","service":"catalog","latency_ms":131.02,"uptime_pct":98.427,"timestamp":20250305},
    {"region":"apac","service":"support","latency_ms":120.73,"uptime_pct":98.365,"timestamp":20250306},
    {"region":"apac","service":"recommendations","latency_ms":126.8,"uptime_pct":97.793,"timestamp":20250307},
    {"region":"apac","service":"analytics","latency_ms":138.81,"uptime_pct":97.368,"timestamp":20250308},
    {"region":"apac","service":"recommendations","latency_ms":154.63,"uptime_pct":98.223,"timestamp":20250309},
    {"region":"apac","service":"support","latency_ms":208.37,"uptime_pct":98.684,"timestamp":20250310},
    {"region":"apac","service":"catalog","latency_ms":206.54,"uptime_pct":99.474,"timestamp":20250311},
    {"region":"apac","service":"payments","latency_ms":229.9,"uptime_pct":99.17,"timestamp":20250312},
    {"region":"emea","service":"checkout","latency_ms":166.2,"uptime_pct":99.014,"timestamp":20250301},
    {"region":"emea","service":"analytics","latency_ms":141.09,"uptime_pct":97.727,"timestamp":20250302},
    {"region":"emea","service":"analytics","latency_ms":191.31,"uptime_pct":99.183,"timestamp":20250303},
    {"region":"emea","service":"catalog","latency_ms":153.25,"uptime_pct":98.518,"timestamp":20250304},
    {"region":"emea","service":"analytics","latency_ms":234.03,"uptime_pct":97.113,"timestamp":20250305},
    {"region":"emea","service":"catalog","latency_ms":184.55,"uptime_pct":97.396,"timestamp":20250306},
    {"region":"emea","service":"checkout","latency_ms":174.84,"uptime_pct":98.07,"timestamp":20250307},
    {"region":"emea","service":"checkout","latency_ms":137.65,"uptime_pct":99.299,"timestamp":20250308},
    {"region":"emea","service":"analytics","latency_ms":194.84,"uptime_pct":98.538,"timestamp":20250309},
    {"region":"emea","service":"analytics","latency_ms":129.13,"uptime_pct":97.872,"timestamp":20250310},
    {"region":"emea","service":"support","latency_ms":227.85,"uptime_pct":98.346,"timestamp":20250311},
    {"region":"emea","service":"checkout","latency_ms":235.14,"uptime_pct":97.564,"timestamp":20250312},
    {"region":"amer","service":"payments","latency_ms":164.91,"uptime_pct":98.174,"timestamp":20250301},
    {"region":"amer","service":"recommendations","latency_ms":182.43,"uptime_pct":97.911,"timestamp":20250302},
    {"region":"amer","service":"checkout","latency_ms":144.06,"uptime_pct":98.39,"timestamp":20250303},
    {"region":"amer","service":"catalog","latency_ms":183.74,"uptime_pct":99.074,"timestamp":20250304},
    {"region":"amer","service":"support","latency_ms":166,"uptime_pct":99.154,"timestamp":20250305},
    {"region":"amer","service":"support","latency_ms":223.77,"uptime_pct":98.291,"timestamp":20250306},
    {"region":"amer","service":"analytics","latency_ms":170.51,"uptime_pct":98.044,"timestamp":20250307},
    {"region":"amer","service":"analytics","latency_ms":169.17,"uptime_pct":97.655,"timestamp":20250308},
    {"region":"amer","service":"support","latency_ms":189.55,"uptime_pct":99.379,"timestamp":20250309},
    {"region":"amer","service":"catalog","latency_ms":183,"uptime_pct":97.688,"timestamp":20250310},
    {"region":"amer","service":"support","latency_ms":227.63,"uptime_pct":97.119,"timestamp":20250311},
    {"region":"amer","service":"catalog","latency_ms":199.46,"uptime_pct":99.133,"timestamp":20250312},
]

app = FastAPI()


class TelemetryRequest(BaseModel):
    regions: List[str]
    threshold_ms: int

@app.post("/api/ping")
async def ping(request: TelemetryRequest):
    response = {}
    for region in request.regions:
        region_data = [r for r in telemetry if r["region"] == region]
        if not region_data:
            response[region] = {
                "avg_latency": None,
                "p95_latency": None,
                "avg_uptime": None,
                "breaches": 0
            }
            continue
        latencies = [r["latency_ms"] for r in region_data]
        uptimes = [r["uptime_pct"] for r in region_data]
        response[region] = {
            "avg_latency": float(np.mean(latencies)),
            "p95_latency": float(np.percentile(latencies, 95)),
            "avg_uptime": float(np.mean(uptimes)),
            "breaches": sum(1 for l in latencies if l > request.threshold_ms)
        }
    return response
