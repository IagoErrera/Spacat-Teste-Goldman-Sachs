# Projeto FastAPI

Este projeto é uma API desenvolvida com FastAPI para gerenciar transações financeiras. Ele inclui funcionalidades como depósito, retirada e consulta de saldos.

## Configuração do Ambiente

Certifique-se de ter o Python instalado. Instale a dependência do fastapi.

```bash
pip install fastapi
pip install uvicorn
```

## Executando a API

Para executar a API, use o seguinte comando:

```bash
uvicorn main:app --reload
```

A API agora estará rodando em `http://localhost:8000`.

## Acessando o Swagger UI

O Swagger UI é uma ferramenta que permite interagir com a API de maneira visual. Para acessá-lo, visite `http://localhost:8000/docs` no seu navegador. Aqui, você pode ver todos os endpoints disponíveis, suas descrições e experimentar enviando requisições diretamente do navegador.

### Para que serve o Swagger UI?

O Swagger UI é uma interface gráfica que facilita a compreensão e o uso da API. Ele fornece:

- Documentação interativa da API: Veja todos os endpoints disponíveis, incluindo os métodos HTTP, parâmetros esperados e formatos de resposta.
- Teste de Endpoints: Envie requisições para a API diretamente do navegador e veja as respostas em tempo real. Isso é útil para testar e debugar sua API.

## Testando a API

Após acessar o Swagger UI, você pode testar as diferentes funcionalidades da API:

- Crie usuários e contas
- Crie transações de depósito e retirada.
- Consulte o saldo das contas.
- Veja o histórico de transações.

Siga as instruções na interface do Swagger para enviar requisições e receber respostas.
