from wordcloud import WordCloud
import io
from reportlab.pdfgen import canvas

def make_wordcloud_image(words):
    wc = WordCloud(width=600, height=300, background_color="white")
    img = wc.generate(" ".join(words))
    buf = io.BytesIO()
    img.to_image().save(buf, format="PNG")
    return buf.getvalue()

def generate_insights_text(raw_count, processed_count, topics_df, sentiment, summary):
    return f"""
TEXT ANALYSIS REPORT

Raw Words: {raw_count}
Processed Words: {processed_count}

Topics Identified:
{topics_df}

Average Sentiment Score: {sentiment}

Summary:
{summary}
"""

def make_pdf_bytes(text):
    buf = io.BytesIO()
    c = canvas.Canvas(buf)
    for i, line in enumerate(text.split("\n")):
        c.drawString(40, 800 - i*14, line)
    c.save()
    buf.seek(0)
    return buf