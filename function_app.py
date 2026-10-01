import logging
import urllib.request
import time
import azure.functions as func

app = func.FunctionApp()

@app.function_name(name="WebMonitorTimer")
@app.timer_trigger(
    schedule="0 */5 * * * *",
    arg_name="timer",
    run_on_startup=False
)
def web_monitor(timer: func.TimerRequest):

    url = "https://www.microsoft.com"

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

        logging.info(
            f"Website={url} "
            f"Status={response.status} "
            f"LatencyMs={latency}"
        )

    except Exception as ex:

        logging.error(
            f"Error={str(ex)}"
        )
