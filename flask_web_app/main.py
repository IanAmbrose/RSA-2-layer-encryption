from website import create_app

app = create_app()

#can only be ran from the file if inside the main file
if __name__ == '__main__': 
    app.run(debug=True)
