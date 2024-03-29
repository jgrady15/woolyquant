package main

import (
	"database/sql"
	"log"
	"main/internal/database"
	"net/http"
	"os"

	"github.com/go-chi/chi/v5"
	"github.com/go-chi/cors"
	"github.com/jackc/pgx/v5/pgxpool"
	"github.com/joho/godotenv"

	// Force package to be imported and initialized
	_ "github.com/lib/pq"
)

// Uppercase ApiConfig allows you to export the struct
// This is useful for testing, and also useful to maintain
// separate files for different parts of the feature
type apiConfig struct {
	Queries *database.Queries
	Pool    *pgxpool.Pool
}

// TODO: Implement pgx/v5 and then use the pgx marshaller in order to resolve the struct bug
func main() {
	godotenv.Load()
	var (
		portString string       = ""
		dbURL      string       = ""
		conn       *sql.DB      = nil
		sqlErr     error        = nil
		apiConf    apiConfig    // MUST BE DEFINED WITHIN FUNC
		router     *chi.Mux     = chi.NewRouter()
		v1Router   *chi.Mux     = chi.NewRouter()
		server     *http.Server // MUST BE DEFINED WITHIN FUNC
		serverErr  error        // MUST BE DEFINED WITHIN FUNC
	)

	portString = os.Getenv("PORT")
	if portString == "" {
		log.Fatal("PORT must be set in .env file")
	}

	dbURL = os.Getenv("DB_URL")
	if dbURL == "" {
		log.Fatal("DB_URL must be set in .env file")
	}

	conn, sqlErr = sql.Open("postgres", dbURL) // Returns (*sql.DB, error)
	if sqlErr != nil {
		log.Fatal(sqlErr)
	}

	apiConf = apiConfig{
		Queries: database.New(conn),
	}

	router.Use(cors.Handler(cors.Options{
		AllowedOrigins:   []string{"http://*", "https://*"},
		AllowedMethods:   []string{"GET", "POST", "PUT", "DELETE", "OPTIONS"},
		AllowedHeaders:   []string{"Accept", "Authorization", "Content-Type", "X-CSRF-Token"},
		ExposedHeaders:   []string{"Link"},
		AllowCredentials: true,
		MaxAge:           300, // Maximum value not ignored by any of major browsers
	}))

	// v1Router acts as middleware for route patterns that begin with /v1
	// Checks health of router patterns
	v1Router.Get("/healthz", HandlerReadiness)
	v1Router.Get("/err", HandlerErr)

	v1Router.Post("/trading-bot", apiConf.HandlerCreateBot)
	v1Router.Get("/trading-bot", apiConf.MiddlewareAuth(apiConf.HandlerGetBotByAPIKey))

	// Creates a new router path using /v1 as a prefix for /healthz
	// This means that /v1/healthz will be the endpoint for the handlerReadiness function
	router.Mount("/v1", v1Router)

	server = &http.Server{
		Handler: router,
		Addr:    ":" + portString,
	}

	log.Printf("Server started on %s", server.Addr)
	serverErr = server.ListenAndServe()
	if serverErr != nil {
		log.Fatal(serverErr)
	}
}
