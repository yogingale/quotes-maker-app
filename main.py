from flask import Flask, render_template
app = Flask(__name__)


@app.route("/")
def template():
    return render_template('index.html')

@app.route("/example")
def template_test():
    return render_template('index_example.html', my_string="Wheeeee!", my_list=[0,1,2,3,4,5])


if __name__ == '__main__':
    app.run(debug=True)
