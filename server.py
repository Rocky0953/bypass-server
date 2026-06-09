from flask import Flask, request, jsonify
from playwright.sync_api import sync_playwright

app = Flask(__name__)

@app.route("/bypass")
def bypass():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "No URL"}), 400
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, wait_until="networkidle", timeout=30000)
            for btn in ["Skip", "Continue", "Get Link", "Proceed"]:
                try:
                    page.click(f"text={btn}", timeout=3000)
                    page.wait_for_timeout(2000)
                except:
                    pass
            final = page.url
            browser.close()
            if final != url:
                return jsonify({"final_url": final})
            return jsonify({"error": "Same URL"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/")
def home():
    return "Bypass Server Running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
