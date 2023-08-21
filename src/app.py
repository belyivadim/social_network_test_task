import config

app = config.connex_app
app.add_api("swagger.yml")


@app.route("/", methods=["GET"])
def health_check():
    return "Server is running.", 200


if __name__ == "__main__":
    with app.app.app_context():
        # config.db.drop_all()
        config.db.create_all()
    app.run(host="0.0.0.0", port=8080, debug=True)
