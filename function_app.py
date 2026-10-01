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
    schedule="* */5 * * * *",
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

            # Performance rating
            if latency < 200:
                performance = "GOOD"
            elif latency < 500:
                performance = "WARNING"
            else:
                performance = "CRITICAL"

            # SSL validation
            hostname = url.replace("https://", "")

            context = ssl.create_default_context()

            with socket.create_connection(
                (hostname, 443),
                timeout=10
            ) as sock:

                with context.wrap_socket(
                    sock,
                    server_hostname=hostname
                ) as ssock:

                    cert = ssock.getpeercert()

            expiry_date = datetime.strptime(
                cert["notAfter"],
                "%b %d %H:%M:%S %Y %Z"
            )

            days_remaining = (
                expiry_date - datetime.utcnow()
            ).days

            ssl_status = "VALID"

            if days_remaining < 30:
                ssl_status = "EXPIRING_SOON"

            if days_remaining < 7:
                ssl_status = "CRITICAL"

            logging.info(
                f"Website={url} "
                f"Status={response.status} "
                f"LatencyMs={latency} "
                f"Performance={performance} "
                f"SSLDaysRemaining={days_remaining} "
                f"SSLStatus={ssl_status}"
            )

            if latency > 1000:

                logging.warning(
                    f"Website={url} "
                    f"HighLatency={latency}"
                )

            if days_remaining < 30:

                logging.warning(
                    f"Website={url} "
                    f"SSL expires in {days_remaining} days"
                )

        except Exception as ex:

            logging.error(
                f"Website={url} "
                f"Error={str(ex)}"
            )
