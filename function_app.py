import logging
import azure.functions as func
import time

app = func.FunctionApp()

@app.function_name(name="WebMonitorTimer")
@app.timer_trigger(
    schedule="0 */5 * * * *",
    arg_name="timer",
    run_on_startup=False
)
def web_monitor(timer: func.TimerRequest):

    logging.info("Timer working")

    start = time.time()

    latency = round(
        (time.time() - start) * 1000,
        2
    )

    logging.info(f"Latency={latency}")
