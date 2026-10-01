import logging
import urllib.request
import time
import ssl
import socket
from datetime import datetime

import azure.functions as func

app = func.FunctionApp()

URLS = [
    "https://www.microsoft.com",
    "https://github.com",
    "https://portal.azure.com"
]

@app.function_name(name="WebMonitorTimer")
@app.timer_trigger(
    schedule="0 */5 * * * *",
    arg_name="timer",
    run_on_startup=False
)
def web_monitor(timer: func.TimerRequest):

    for url in URLS:

        try:

            start = time.time()

            response = urllib.request.urlopen(
                url,
                timeout=10
            )

            latency = round(
                (time.time() - start) * 1000,
                2
            )

            hostname = url.replace("https://", "")

            cert = ssl.get_server_certificate(
                (hostname, 443)
            )

            x509 = ssl.PEM_cert_to_DER_cert(cert)

            ssl_info = ssl._ssl._test_decode_cert(
                ssl.get_default_verify_paths().cafile
            )

            logging.info(
                f"Website={url} "
                f"Status={response.status} "
                f"LatencyMs={latency}"
            )

        except Exception as ex:

            logging.error(
                f"Website={url} "
                f"Error={str(ex)}"
            )
