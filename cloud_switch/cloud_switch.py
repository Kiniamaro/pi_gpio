#!/usr/bin/python
import time
import sys

from flask import Flask, request, jsonify, redirect
import RPi.GPIO as GPIO


app = Flask(__name__)
state = False


@app.route('/api/toggle', methods=['GET'])
def toggle_switch():
    global state
    if state:
        GPIO.output(app.config['SWITCH_PIN'], GPIO.HIGH)
        print('[Output] : HIGH')
    else:
        GPIO.output(app.config['SWITCH_PIN'], GPIO.LOW)
        print('[Output] : LOW')
    state = not state

    return jsonify(state=state)


if __name__ == "__main__":
    app.config.from_pyfile('config/default_config.py')
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(app.config['SWITCH_PIN'], GPIO.OUT)

    if len(sys.argv) == 2:
        conf = sys.argv[1]
        print('Loading additional config %s...', conf)
        app.config.from_pyfile('config/' + conf + '_config.py')
app.run()
