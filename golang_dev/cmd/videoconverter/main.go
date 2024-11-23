package main

import (
	"database/sql"
	"fmt"
	"log/slog"
	"os"

	"github.com/developersoftwarebrazil/fullstack-fullcycle-microservices-contebras/internal/converter"
	"github.com/developersoftwarebrazil/fullstack-fullcycle-microservices-contebras/internal/rabbitmq"
	"github.com/streadway/amqp"

	_ "github.com/lib/pq"
)

// connectPostgres establishes a connection with PostgreSQL using environment variables for configuration.
func connectPostgres() (*sql.DB, error) {
	user := getEnvOrDefault("POSTGRES_USER", "user")
	password := getEnvOrDefault("POSTGRES_PASSWORD", "password")
	dbname := getEnvOrDefault("POSTGRES_DB", "converter")
	host := getEnvOrDefault("POSTGRES_HOST", "host.docker.internal")
	sslmode := getEnvOrDefault("POSTGRES_SSL_MODE", "disable")

	connStr := fmt.Sprintf("user=%s password=%s dbname=%s host=%s sslmode=%s", user, password, dbname, host, sslmode)
	db, err := sql.Open("postgres", connStr)
	if err != nil {
		slog.Error("Failed to connect to PostgreSQL", slog.String("error", err.Error()))
		return nil, err
	}

	err = db.Ping()
	if err != nil {
		slog.Error("Failed to ping PostgreSQL", slog.String("error", err.Error()))
		return nil, err
	}

	slog.Info("Connected to PostgreSQL successfully")
	return db, nil
}

// getEnvOrDefault fetches the value of an environment variable or returns a default value if it's not set.
func getEnvOrDefault(key, defaultValue string) string {
	if value, exists := os.LookupEnv(key); exists {
		return value
	}
	return defaultValue
}

func main() {

	rabbitMQURL := getEnvOrDefault("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/")
	rabbitClient, err := rabbitmq.NewRabbitClient(rabbitMQURL)
	if err != nil {
		slog.Error("Failed to connect to RabbitMQ", slog.String("error", err.Error()))
		return
	}
	defer rabbitClient.Close()

	conversionExch := getEnvOrDefault("CONVERSION_EXCHANGE", "convertion_exchange")
	queueName := getEnvOrDefault("QUEUE_NAME", "video_convertion_queue")
	conversionKey := getEnvOrDefault("CONVERSION_KEY", "conversion")
	confirmationKey := getEnvOrDefault("CONFIRMATION_KEY", "finish-conversion")
	// rootPath := getEnvOrDefault("VIDEO_ROOT_PATH", "./media/uploads")
	confirmationQueue := "video_confirmation_queue" // Nome da fila de confirmação

	db, err := connectPostgres()
	if err != nil {
		return
	}
	defer db.Close()

	vc := converter.NewVideoConverter(rabbitClient, db)
	// vc.HandleMessage([]byte(`{"video_id":1,"path":"/media/uploads/1"}`))

	msgs, err := rabbitClient.ConsumeMessages(conversionExch, conversionKey, queueName)
	if err != nil {
		slog.Error("failed to consume messages: %v", slog.String("error", err.Error()))
	}

	for d := range msgs {
		go func(delivery amqp.Delivery) {
			vc.HandleMessage(delivery, conversionExch, confirmationKey, confirmationQueue)
		}(d)
	}

}
