# Placeholder for Kafka/Spark/Flink integration

def send_to_kafka(topic, data, kafka_host="localhost:9092"):
    # Use kafka-python or confluent-kafka
    print(f"[KAFKA] Topic: {topic}, Data: {data}")

# Example usage:
# send_to_kafka("crowdflow", {"active": 123}) 