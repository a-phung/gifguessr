from flask import Flask, render_template, url_for
import pika, os

app = Flask(__name__)


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/play")
def play():
    # - Producer - Send a message to RabbitMQ
    url = "amqps://tjybwijb:ljZM5GMaLrZtrc3K9OS0WGN6gWL3pmtB@jaguar.rmq.cloudamqp.com/tjybwijb"
    params = pika.URLParameters(url)
    connection = pika.BlockingConnection(params)
    # Send message to fetch image from image microservice
    channel = connection.channel()  # Start a channel

    channel.exchange_declare("test_exchange")  # Declare exchange
    channel.queue_declare(queue="test_queue")  # Declare queue
    channel.queue_bind("test_queue", "test_exchange", "tests")  # Create binding between queue and exchange

    # Produce message
    channel.basic_publish(
        body="Fetching new image...",
        exchange="test_exchange",
        routing_key="tests"
    )
    print("Message sent.")
    channel.close()  # Close channel

    # - Consumer - Open new channel to listen for image message to consume
    channel = connection.channel()  # Start a channel
    channel.queue_declare(queue="image_queue")  # Declare queue

    # Initialize array to hold message body
    image_array = []

    # Get the message from RabbitMQ and display image
    def callback(ch, method, properties, body):
        print(" [x] Received " + body.decode())
        image_array.append(body.decode())
        channel.close()

    channel.basic_consume(
        "image_queue",
        callback,
        auto_ack=True
    )

    print(" [*] Waiting for messages: ")
    channel.start_consuming()
    connection.close()  # Close the connection

    image_url = image_array[0]
    return render_template("play.html", image_url=image_url)


if __name__ == "__main__":
    app.run(debug=True)
