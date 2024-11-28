import requests
from bs4 import BeautifulSoup
from langchain_openai.chat_models.azure import AzureChatOpenAI

def extract_text_from_url(url):
	response = requests.get(url)

	if response.status_code == 200:
		soup = BeautifulSoup(response.text, 'html.parser')

		for script_or_style in soup(["script", "style"]):
			script_or_style.decompose()

		texto = soup.get_text(separator=' ')
		# limpar texto
		linhas = (line.strip() for line in texto.splitlines())
		parts = (phrase.strip() for line in linhas for phrase in line.split(" "))
		texto_limpo = '\n'.join(part for part in parts if part)
		texto_limpo = texto_limpo[:1000]
		return texto_limpo
	else:
		print(f"Failed to fetch URL. Status code: {response.status_code}")
		return None

client = AzureChatOpenAI(
	azure_endpoint="put your endpoint here",
	api_key="put your key here",
	api_version="2024-02-15-preview",
	deployment_name="gpt-4o-mini",
	max_retries=0
)

def translate_article(text, lang):
	messages = [
		("system", "Você atua como tradutor de textos"),
		("user", f"Traduza o {text} para o idioma {lang} e responda em markdown")
	]

	response = client.invoke(messages)
	print(response.content)
	return response.content

url = "https://dev.to/kenakamu/azure-open-ai-in-vnet-3alo"
text = extract_text_from_url(url)
article = translate_article(text, "pt-br")

print(article)
