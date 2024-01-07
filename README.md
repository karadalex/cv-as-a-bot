CV-as-a-bot
===========

Examples of valid answers: <br>
![](./img/query1.png)
![](./img/query2.png)
![](./img/query3.png)<br>
More open-ended question:<br>
![](./img/query4.png)

Ask this RAG LLM chatbot anything you want to learn about my Curriculum Vitae

```bash
virtualenv . -p /usr/bin/python3.8
source bin/activate
pip install -r requirements.txt
streamlit run main.py
```

Features:

- [x] Langchain
- [x] OpenAI ChatGPT
- [x] Streamlit UI for quick prototyping
- [ ] Supabase project & pgvector
- [ ] NextJS production project & deployment at Vercel
- [x] Load Github profile
- [x] Github repositories load
- [x] Load CV PDF
- [ ] Load any PDF
- [ ] Load personal website
- [ ] Load LinkedIn profile
- [ ] Mistral LLM example
- [ ] Phi2 small LM example
- [ ] Do an internet search about this name (?)
- [ ] Better cleaning of data

