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
    logging.info("Web Monitor Timer Executed")
