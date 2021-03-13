from flask import Flask, render_template

from blockchain import blockchain

app = Flask(__name__)

cycoin = blockchain.Blockchain()


@app.template_filter()
def datetimefilter(value, format="%Y/%m/%d %H:%M"):
    """convert a datetime to a different format."""
    return value.strftime(format)


app.jinja_env.filters["datetimefilter"] = datetimefilter


@app.route("/")
@app.route("/block")
def home():
    return render_template(
        "home.html",
        title="Home",
        chain=cycoin.get_chain(),
        active_block=None,
        transactions=[],
    )


@app.route("/block/<hash>")
def block(hash):
    return render_template(
        "home.html",
        title="Blocks on chain",
        chain=cycoin.get_chain(),
        active_block=hash,
        transactions=cycoin.get_transactions(hash),
    )


@app.route("/settings")
def settings():
    return render_template("settings.html", title="Settings",)


@app.route("/new")
def new():
    return render_template("create_transaction.html", title="Create transaction",)


@app.route("/new/pending")
def pending():
    return render_template("pending_transactions.html", title="Pending transactions")


if __name__ == "__main__":
    app.run(debug=True)
