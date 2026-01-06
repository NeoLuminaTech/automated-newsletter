from jinja2 import Environment, FileSystemLoader
from fetch_news import fetch_news

env = Environment(loader=FileSystemLoader("templates"))
template = env.get_template("newsletter.html")

def build_html():
    articles = fetch_news()
    html = template.render(articles=articles)
    with open("newsletter_output.html", "w", encoding="utf-8") as f:
        f.write(html)
    return html

if __name__ == "__main__":
    build_html()
