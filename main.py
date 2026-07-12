from Website import create_app

app = create_app()
if __name__ == '__main__': # Runs web server
    app.run(debug=True)    # Re-runs web server every time a change is made