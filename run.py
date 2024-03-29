from gazprom_test_task_jokes.gazprom_test_task_jokes import app

if __name__ == "__main__":
    app.run(
        host=app.config.SERVER_HOST,
        port=app.config.SERVER_PORT,
        workers=app.config.WORKERS,
        debug=app.config.DEBUG,
        access_log=app.config.ACCESS_LOG,
        auto_reload=app.config.AUTO_RELOAD,
        )
