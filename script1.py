from flask import Flask, request, render_template_string
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

x = sp.symbols('x')

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Equation Plotter</title>
</head>
<body style="font-family: Arial; text-align:center;">
    <h2>Equation Plotter</h2>
    <form method="post">
        <input type="text" name="equation" placeholder="Enter equation in x"
               value="{{ equation }}" style="width:300px;">
        <br><br>
        <button type="submit">Plot</button>
    </form>
    <br>
    {% if plot %}
        <img src="data:image/png;base64,{{ plot }}">
    {% endif %}
    {% if error %}
        <p style="color:red;">{{ error }}</p>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    plot = None
    error = None
    equation = ""

    if request.method == "POST":
        equation = request.form.get("equation", "")
        try:
            expr = sp.sympify(equation)
            f = sp.lambdify(x, expr, modules=["numpy"])

            x_vals = np.linspace(-10, 10, 400)
            y_vals = f(x_vals)

            fig, ax = plt.subplots()
            ax.plot(x_vals, y_vals)
            ax.set_title(f"y = {equation}")
            ax.set_xlabel("x")
            ax.set_ylabel("y")
            ax.grid(True)

            buf = io.BytesIO()
            plt.savefig(buf, format="png")
            buf.seek(0)
            plot = base64.b64encode(buf.getvalue()).decode()
            plt.close(fig)

        except Exception as e:
            error = str(e)

    return render_template_string(HTML, plot=plot, error=error, equation=equation)

if __name__ == "__main__":
    app.run()
