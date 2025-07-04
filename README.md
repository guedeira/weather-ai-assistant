# Assistente de Clima com IA
Este é um projeto que fiz para estudo, ele é conectado com a OpenAI e OpenWeather, onde a IA irá receber uma pergunta sobre o clima em uma cidade, e com base nisso vai chamar uma função para coletar os dados em tempo real daquela cidade, e retornar os dados ao usuário com dicas úteis do que vestir e se ele precisa sair com guarda-chuvas de casa naquele dia.

# Melhorias para o futuro (se houver kkk)
- [ ] Filtrar a resposta da API para retornar apenas os dados necessários. (Economizar tokens!)
- [ ] O lint tá dando alguns alertas por conta dos tipos de alguns parâmetros, precisa ajustar.
- [ ] Alterar a API da OpenAI de Chat Completions para Response (versão mais atual).
    - [Link do Guia](https://platform.openai.com/docs/guides/responses-vs-chat-completions)

## Como Executar o Projeto
Siga os passos abaixo para configurar e executar a aplicação.

1.  **Clonar o Repositório:**
    ```bash
    git clone <url-do-seu-repositorio>
    cd weather-ai-assistant
    ```
2.  **Criar e Ativar um Ambiente Virtual:**
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```
3.  **Instalar as Dependências:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Configurar as Variáveis de Ambiente:**
    Renomeie o arquivo chamado `.env.exemple` para `.env` na raiz do projeto e adicione suas chaves de API:
    ```
    OPENAI_API_KEY="sua_chave_da_openai"
    OPENWEATHER_API_KEY="sua_chave_da_openweather"

    # Opcional: Ative o modo de depuração para ver o fluxo de chamadas
    DEBUG=False
    ```
5.  **Executar a Aplicação:**
    ```bash
    python main.py
    ```

## Fluxo Lógico Central
A interação do usuário com a IA segue um ciclo orquestrado em `main.py`:

1.  **Input do Usuário:** O usuário digita uma pergunta, como "Qual o clima em São Paulo?".
2.  **Primeira Chamada à IA:** O `main.py` envia a pergunta do usuário para o `OpenAIClient`, junto com uma lista de ferramentas disponíveis (neste caso, a função `get_weather`). A IA é instruída a usar essas ferramentas quando necessário.
3.  **Decisão da IA (Function Calling):** O modelo da OpenAI analisa a pergunta e, em vez de responder diretamente, decide que precisa de informações externas. Ele retorna uma mensagem especial indicando que deseja chamar a função `get_weather` e fornece os argumentos extraídos da pergunta do usuário (ex: `{"city": "São Paulo"}`).
4.  **Execução da Ferramenta:** O `main.py` detecta essa intenção. Ele chama a função correspondente no `WeatherClient`, que executa a requisição HTTP para a API OpenWeather e obtém os dados do clima.
5.  **Segunda Chamada à IA:** O resultado obtido da ferramenta (os dados do clima em formato JSON) é enviado de volta para a IA em uma nova chamada. A mensagem agora inclui o histórico da conversa e o resultado da ferramenta.
6.  **Resposta Final ao Usuário:** Com os dados concretos em mãos, a IA gera uma resposta final em linguagem natural (Português do Brasil), informando a temperatura, o clima e adicionando uma recomendação útil, como "A temperatura é de 14°C com chuva leve. Recomendo levar um guarda-chuva e vestir roupas quentes."

## Decisões de Arquitetura
O projeto foi estruturado para manter o código organizado e manutenável (eu tentei, juro, mas acho que ficou bom!).

-   **`main.py` (Orquestração e Interface):**
    -   **Responsabilidade:** É o ponto de entrada da aplicação. Controla o loop de interação com o usuário (CLI) e orquestra o fluxo de chamadas entre os diferentes clientes. Não contém lógica de negócio, apenas coordenação.
-   **`src/clients/` (Comunicação Externa):**
    -   **`openai_client.py`:** Abstrai toda a complexidade da comunicação com a API da OpenAI. Sua única responsabilidade é montar e enviar as requisições de chat, facilitando o uso no `main.py`.
    -   **`weather_client.py`:** Isola a lógica de chamada à API OpenWeather. Se a API mudasse ou precisássemos adicionar outra fonte de dados, apenas este arquivo seria modificado.
-   **`src/config/settings.py` (Configuração Centralizada):**
    -   **Responsabilidade:** Carrega todas as configurações e segredos (API keys) a partir de um arquivo `.env`. Isso segue a boa prática de **externalizar a configuração**, evitando que dados sensíveis sejam escritos diretamente no código.
-   **Modo de Depuração (`DEBUG`):**
    -   A inclusão de uma flag `DEBUG` foi uma funcionalidade criada para facilitar o aprendizado e a manutenção. Quando ativada permite visualizar em tempo real a "decisão" da IA de chamar a ferramenta, os argumentos que ela usa e os dados que recebe de volta. É uma ferramenta para entender o mecanismo de **function calling**.

> Olha, não vou falar que eu codei sozinho, foi eu e umas IAs (atualmente to testando o Gemini CLI mas as algumas vezes chamei o Claude também kkkk), o importante é que eu entendi toda a lógica e acredito que no quesito arquitetura e organização esteja OK também.
