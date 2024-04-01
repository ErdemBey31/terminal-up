import subprocess
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
terminals = []

@app.route('/')
def index():
    return render_template('index.html', terminals=terminals)

@app.route('/new_terminal', methods=['POST'])
def new_terminal():
    terminal_id = len(terminals) + 1
    terminal = {
        'id': terminal_id,
        'output': '',
        'process': None
    }
    terminals.append(terminal)
    return redirect(url_for('terminal', terminal_id=terminal_id))

@app.route('/terminal/<int:terminal_id>')
def terminal(terminal_id):
    terminal = get_terminal(terminal_id)
    if terminal:
        return render_template('terminal.html', terminal=terminal)
    return redirect(url_for('index'))

@app.route('/command', methods=['POST'])
def command():
    terminal_id = int(request.form['terminal_id'])
    command = request.form['command']
    terminal = get_terminal(terminal_id)
    if terminal and command:
        run_command(terminal, command)
    return redirect(url_for('terminal', terminal_id=terminal_id))

@app.route('/delete_terminal/<int:terminal_id>')
def delete_terminal(terminal_id):
    terminal = get_terminal(terminal_id)
    if terminal:
        terminals.remove(terminal)
    return redirect(url_for('index'))

def run_command(terminal, command):
    if terminal['process'] is None:
        terminal['process'] = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
    else:
        terminal['process'].stdin.write(command + '\n')
        terminal['process'].stdin.flush()

    while terminal['process'].poll() is None:
        output = terminal['process'].stdout.readline()
        terminal['output'] += output

    terminal['process'] = None

def get_terminal(terminal_id):
    for terminal in terminals:
        if terminal['id'] == terminal_id:
            return terminal
    return None

if __name__ == '__main__':
    app.run(debug=True)
