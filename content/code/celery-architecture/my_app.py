from celery import Celery

app = Celery(
    "my_app",
    backend="rpc://",
    broker="amqp://guest@localhost//",
)


@app.task()
def add(a: int, b: int) -> int:
    return a + b


if __name__ == "__main__":
    # Request that the tasks run and capture their async results.
    asyncresult_1 = add.delay(1, 2)
    asyncresult_2 = add.delay(3, 4)

    result_1 = asyncresult_1.get()
    result_2 = asyncresult_2.get()
    # Should result in 3, 7.
    print(f"Results: {result_1}, {result_2}")
