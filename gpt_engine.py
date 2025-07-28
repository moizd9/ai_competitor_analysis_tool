import openai

def generate_swot_and_recommendations(data, api_key):
    try:
        client = openai.OpenAI(api_key=api_key)

        prompt = f"""
You are a marketing strategist. Based on this website SEO & business summary, provide:
1. SWOT analysis
2. Three actionable marketing growth recommendations

Website summary:
{data}

Output in markdown format.
"""

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert digital strategist."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"⚠️ GPT Error: {e}"
