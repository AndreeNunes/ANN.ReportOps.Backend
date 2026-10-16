# Railway Bucket

O backend usa o bucket somente pelo servidor. O aplicativo recebe URLs assinadas curtas e nunca recebe chaves de acesso.

## Variáveis no serviço do backend

No Railway, crie referências para o Bucket no serviço do backend:

    S3_ENDPOINT=${{Bucket.ENDPOINT}}
    S3_ACCESS_KEY_ID=${{Bucket.ACCESS_KEY_ID}}
    S3_SECRET_ACCESS_KEY=${{Bucket.SECRET_ACCESS_KEY}}
    S3_BUCKET=${{Bucket.BUCKET}}
    S3_REGION=${{Bucket.REGION}}
    S3_URL_STYLE=virtual

Use o nome real do serviço Bucket no lugar de Bucket se ele tiver outro nome.

## Banco

Aplique migrations/20261003_report_media.sql uma vez no banco usado pelo backend. Ela cria REPORT_MEDIA, que guarda a chave do objeto, tipo, tamanho e observação; URLs assinadas não são persistidas.

## Fluxo

1. A câmera e a galeria copiam a imagem para a área privada do aplicativo.
2. Ao sincronizar, o backend cria URLs de PUT para cada mídia ainda pendente.
3. O aplicativo envia os arquivos diretamente ao Railway Bucket e grava o progresso localmente.
4. O backend confirma que os objetos existem e persiste os metadados.
5. Ao abrir a galeria ou gerar um PDF de um relatório remoto, o aplicativo pede somente URLs temporárias das mídias necessárias.
