from flask import Flask, render_template, request, jsonify
from pathlib import Path
import shutil

app = Flask(__name__)

DEMO_FOLDER = Path(__file__).parent / "demo_files"
DEMO_FOLDER.mkdir(exist_ok=True)

CATEGORIES = {
    "Images": {".jpg", ".jpeg", ".png", ".gif", ".webp"},
    "Documents": {".doc", ".docx", ".txt"},
    "PDFs": {".pdf"},
    "Videos": {".mp4", ".mkv", ".avi", ".mov"},
    "Audio": {".mp3", ".wav", ".flac"},
    "Archives": {".zip", ".rar", ".7z"},
    "Code": {".py", ".c", ".cpp", ".java", ".js", ".html", ".css"},
}

def category(file):
    ext = file.suffix.lower()
    for name, extensions in CATEGORIES.items():
        if ext in extensions:
            return name
    return "Others"

def organize():
    count = 0
    for file in list(DEMO_FOLDER.iterdir()):
        if not file.is_file():
            continue
        folder = DEMO_FOLDER / category(file)
        folder.mkdir(exist_ok=True)
        destination = folder / file.name
        i = 1
        while destination.exists():
            destination = folder / f"{file.stem}_{i}{file.suffix}"
            i += 1
        shutil.move(str(file), str(destination))
        count += 1
    return count

def stats():
    result = {name: 0 for name in [*CATEGORIES.keys(), "Others"]}
    for file in DEMO_FOLDER.rglob("*"):
        if file.is_file():
            result[category(file)] += 1
    result["Total"] = sum(result.values())
    return result

def search_files(term):
    term = term.lower()
    results = []
    for file in DEMO_FOLDER.rglob("*"):
        if file.is_file() and term in file.name.lower():
            results.append(str(file.relative_to(DEMO_FOLDER)))
    return results

@app.route("/")
def home():
    return render_template("index.html", stats=stats())

@app.post("/organize")
def organize_route():
    return jsonify({"success": True, "count": organize(), "stats": stats()})

@app.get("/search")
def search_route():
    return jsonify({"results": search_files(request.args.get("q", ""))})

@app.get("/stats")
def stats_route():
    return jsonify(stats())

if __name__ == "__main__":
    app.run(debug=True)