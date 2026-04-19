from flask import Flask, render_template, request, jsonify
import calculator

app = Flask(__name__)


def _parse_point(data, key):
    """Extract and validate a [x, y, z] list from request data."""
    val = data.get(key)
    if not isinstance(val, list) or len(val) != 3:
        raise ValueError(f"'{key}' must be a list of 3 numbers.")
    return [float(v) for v in val]


def _parse_float(data, key):
    val = data.get(key)
    if val is None:
        raise ValueError(f"Missing field '{key}'.")
    return float(val)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/parameterform', methods=['POST'])
def parameterform():
    try:
        data = request.get_json(force=True)
        p1 = _parse_point(data, 'p1')
        p2 = _parse_point(data, 'p2')
        p3 = _parse_point(data, 'p3')
        point = _parse_point(data, 'point')
    except (ValueError, TypeError) as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

    result = calculator.calculate_parameterform(p1, p2, p3, point)
    return jsonify(result)


@app.route('/api/koordinatenform', methods=['POST'])
def koordinatenform():
    try:
        data = request.get_json(force=True)
        a = _parse_float(data, 'a')
        b = _parse_float(data, 'b')
        c = _parse_float(data, 'c')
        d = _parse_float(data, 'd')
        point = _parse_point(data, 'point')
    except (ValueError, TypeError) as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

    result = calculator.calculate_koordinatenform(a, b, c, d, point)
    return jsonify(result)


@app.route('/api/normaleform', methods=['POST'])
def normaleform():
    try:
        data = request.get_json(force=True)
        normal = _parse_point(data, 'normal')
        plane_point = _parse_point(data, 'plane_point')
        point = _parse_point(data, 'point')
    except (ValueError, TypeError) as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

    result = calculator.calculate_normaleform(normal, plane_point, point)
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)
