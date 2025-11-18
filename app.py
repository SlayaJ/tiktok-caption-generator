# filename: app.py
from flask import Flask, request, render_template_string
import random
import openai  # you'll use Grok API or OpenRouter later to save costs
import os

app = Flask(__name__)

# Put your API key here (or use environment variable)
openai.api_key = os.getenv("OPENAI_API_KEY")  # works with Grok via OpenRouter too

# Hundreds of proven caption templates (add more for variety)
CAPTION_TEMPLATES = [
    "POV: You finally {topic} after {struggle} 😭👇",
    "This {topic} hack changed everything for me ✅",
    "99% of people get {topic} wrong… here’s the truth 👀",
    "Do THIS if you want {topic} in 2025 🔥",
    "The {topic} secret the algorithm doesn’t want you to know 🤫",
    "Day {number} of {topic} until I go viral 📈",
    "If you scroll past this {topic} tip, I’m judging you 😤",
    "Watch until the end if you want {topic} 💯",
]

# Trending hashtag packs by niche (expand this list!)
HASHTAG_PACKS = {
    "default": "#fyp #foryou #viral #trending #tiktok #explore #fypシ #xyzbca",
    "fitness": "#fitness #gym #workout #fit #motivation #gymtok #fitnessmotivation",
    "beauty": "#makeup #beauty #skincare #makeuptutorial #beautytok #grwm",
    "food": "#food #foodtok #recipe #easyrecipe #cooking #tiktokfood",
    "business": "#sidehustle #money #entrepreneur #business #finance #wealth",
}

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        topic = request.form["topic"].strip()
        niche = request.form.get("niche", "default")

        # Option 1: Use OpenAI/Grok for dynamic captions (best quality)
        try:
            response = openai.ChatCompletion.create(
                model="grok-beta",  # works via OpenRouter or change to gpt-3.5-turbo
                messages=[{"role": "user", "content": f"Write 10 short, viral TikTok captions about {topic}. Max 15 words each. Hook heavy."}],
                max_tokens=300
            )
            captions = response.choices[0].message.content.strip().split("\n")
            captions = [c for c in captions if c and not c.lower().startswith("here are")]
        except:
            # Fallback: use templates if API down or you want $0 cost
            captions = [t.format(topic=topic, struggle=random.choice(["months of trying","wasting money","failing"]),
                                  number=random.randint(1,100)) for t in random.sample(CAPTION_TEMPLATES, 8)]

        hashtags = HASHTAG_PACKS.get(niche, HASHTAG_PACKS["default"]) + " #" + topic.replace(" ", "")

        return render_template_string(TEMPLATE, captions=captions[:10], hashtags=hashtags, topic=topic)

    return render_template_string(TEMPLATE, captions=[], hashtags="", topic="")

TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Viral TikTok Caption Generator</title>
    <style>
        body { font-family: system-ui; max-width: 700px; margin: 40px auto; padding: 20px; background: #000; color: #fff; }
        input, select, button { padding: 12px; margin: 10px 0; width: 100%; border-radius: 8px; border: none; font-size: 16px; }
        button { background: #ff0050; color: white; cursor: pointer; font-weight: bold; }
        .caption { background: #1a1a1a; padding: 15px; margin: 10px 0; border-radius: 10px; border-left: 4px solid #ff0050; }
        .hashtags { background: #1a1a1a; padding: 15px; border-radius: 10px; word-wrap: break-word; }
    </style>
</head>
<body>
    <h1>✨ Viral TikTok Caption + Hashtag Generator</h1>
    <form method="post">
        <input type="text" name="topic" placeholder="Your video topic (e.g. morning routine, gym tips)" required>
        <select name="niche">
            <option value="default">General / Viral</option>
            <option value="fitness">Fitness</option>
            <option value="beauty">Beauty / Makeup</option>
            <option value="food">Food / Recipes</option>
            <option value="business">Money / Side Hustle</option>
        </select>
        <button type="submit">Generate Captions</button>
    </form>

    {% if captions %}
        <h2>10 Viral Captions</h2>
        {% for cap in captions %}
            <div class="caption" onclick="copy(this)">{{ cap }}</div>
        {% endfor %}
        <h2>Best Hashtags (Copy & Paste)</h2>
        <div class="hashtags" onclick="copy(this)">{{ hashtags }}</div>
    {% endif %}

    <script>
        function copy(el) {
            navigator.clipboard.writeText(el.innerText);
            alert("Copied!");
        }
    </script>
</body>
</html>
"""

if __name__ == "__main__":
    app.run(debug=True)
