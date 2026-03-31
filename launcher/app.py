import json
import os
import subprocess
from pathlib import Path
from typing import Any

from flask import Flask, Response, jsonify, render_template, request
from flask.typing import ResponseReturnValue

app = Flask(__name__)

BASE_DIR = Path(__file__).parent
MODULES_FILE = BASE_DIR / "modules.json"


def load_modules() -> list[dict[str, Any]]:
    with open(MODULES_FILE) as f:
        return json.load(f)["modules"]


def get_module(module_id: str) -> dict[str, Any] | None:
    return next((m for m in load_modules() if m["id"] == module_id), None)


def module_path(module: dict[str, Any]) -> Path:
    return (BASE_DIR / module["path"]).resolve()


def running_containers(module: dict[str, Any]) -> list[str]:
    result = subprocess.run(
        ["docker-compose", "ps", "--services"],
        cwd=module_path(module),
        capture_output=True,
        text=True,
    )
    return [s.strip() for s in result.stdout.splitlines() if s.strip()]


def write_env_file(module: dict[str, Any], selected_vulns: set[str]) -> None:
    env_path = module_path(module) / ".env"
    lines: list[str] = []
    for container in module["containers"]:
        for vuln in container["vulnerabilities"]:
            val = "true" if vuln["id"] in selected_vulns else "false"
            lines.append(f'{vuln["id"]}={val}')
    env_path.write_text("\n".join(lines) + "\n")


@app.route("/")
def index() -> ResponseReturnValue:
    modules = load_modules()
    statuses: dict[str, list[str]] = {
        m["id"]: running_containers(m) for m in modules
    }
    return render_template("index.html", modules=modules, statuses=statuses)


@app.route("/launch/<module_id>", methods=["POST"])
def launch(module_id: str) -> ResponseReturnValue:
    module = get_module(module_id)
    if not module:
        return jsonify({"error": "Module not found"}), 404

    selected_vulns: set[str] = set(request.form.getlist("vulns"))
    write_env_file(module, selected_vulns)

    subprocess.Popen(
        ["docker-compose", "up", "--build", "-d"],
        cwd=module_path(module),
    )

    return jsonify({"status": "launching"}), 200


@app.route("/stop/<module_id>", methods=["POST"])
def stop(module_id: str) -> ResponseReturnValue:
    module = get_module(module_id)
    if not module:
        return jsonify({"error": "Module not found"}), 404

    subprocess.Popen(
        ["docker-compose", "down"],
        cwd=module_path(module),
    )

    return jsonify({"status": "stopping"}), 200


@app.route("/reset/<module_id>", methods=["POST"])
def reset(module_id: str) -> ResponseReturnValue:
    module = get_module(module_id)
    if not module:
        return jsonify({"error": "Module not found"}), 404

    subprocess.Popen(
        ["bash", "-c", "docker-compose down --volumes --remove-orphans && docker volume prune -f"],
        cwd=module_path(module),
    )

    return jsonify({"status": "resetting"}), 200


@app.route("/status/<module_id>")
def status(module_id: str) -> ResponseReturnValue:
    module = get_module(module_id)
    if not module:
        return jsonify({"error": "Module not found"}), 404

    return jsonify({"running": running_containers(module)}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=False)