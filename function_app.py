import logging
import azure.functions as func
import requests

app = func.FunctionApp()

@app.function_name(name="WebMonitorTimer")
@app.timer_trigger(
    schedule="0 */5 * * * *",
    arg_name="timer",
    run_on_startup=False
)
def web_monitor(timer: func.TimerRequest) -> None:

    logging.info("Starting test")

    response = requests.get(
        "https://www.microsoft.com",
        timeout=10
    )

    logging.info(
        f"Status={response.status_code}"
    )
