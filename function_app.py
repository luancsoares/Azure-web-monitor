import logging
import azure.functions as func

app = func.FunctionApp()

@app.function_name(name="WebMonitorTimer")
@app.timer_trigger(
    schedule="0 */5 * * * *",
    arg_name="timer",
    run_on_startup=False
)
def web_monitor(timer: func.TimerRequest) -> None:

    url = "https://www.microsoft.com"

    logging.info(
        f"Checking {url}"
    )
