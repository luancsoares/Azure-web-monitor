import logging
import azure.functions as func
import urllib.request

app = func.FunctionApp()

@app.function_name(name="WebMonitorTimer")
@app.timer_trigger(
    schedule="0 */5 * * * *",
    arg_name="timer",
    run_on_startup=False
)
def web_monitor(timer: func.TimerRequest) -> None:

    try:

        response = urllib.request.urlopen(
            "https://www.microsoft.com",
            timeout=10
        )

        logging.info(
            f"Status={response.status}"
        )

    except Exception as ex:

        logging.error(
            f"Exception: {str(ex)}"
        )
