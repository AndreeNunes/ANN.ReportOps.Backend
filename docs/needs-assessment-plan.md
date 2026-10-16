# Plano de desenvolvimento: Levantamento de necessidade

## Objetivo e decisões de modelo

Adicionar o tipo `NEEDS_ASSESSMENT` à tabela `REPORT` e criar a tabela específica
`NEEDS_ASSESSMENT`. O `REPORT.id_reference` aponta para o ID do levantamento.
Cada levantamento pertence à empresa definida no momento de criar o relatório
e referencia o equipamento cadastrado por `id_equipament`, seguindo o padrão da
Ordem de Serviço. A empresa é exibida como dado do relatório, sem campo de
seleção na tela de equipamento. Não há assinatura neste tipo.

Campos propostos para `NEEDS_ASSESSMENT`:

| Campo | Tipo/uso |
| --- | --- |
| `id` | UUID, chave primária, mesmo valor de `REPORT.id_reference` |
| `id_company`, `id_equipament` | Referências aos cadastros existentes, como em `ORDEM_SERVICE`; usar os tipos e collations reais das tabelas |
| `external_compressor_notes`, `internal_compressor_notes` | Texto opcional de identificação |
| `air_filter`, `oil_filter`, `air_oil_separator`, `pre_coalescing`, `post_coalescing`, `belts`, `hoses` | `TINYINT(1) NULL`: sim, não ou ainda não respondido |
| `created_at`, `updated_at` | Datas de criação e alteração |

A migração usa `CHAR(36)` para IDs. O banco recusou a FK para `COMPANY.id`
porque essa coluna não é uma chave única isolada. O levantamento guarda os IDs
sem FKs; a API valida a empresa do cliente e o vínculo do equipamento com ela
antes de salvar. Conferir os tipos em outro ambiente antes de aplicar. Neste esquema, `REPORT.type` é `VARCHAR(30)`, portanto aceita `NEEDS_ASSESSMENT` sem alteração. O envio usa duas chamadas já existentes: primeiro `REPORT` e depois o registro específico. Ambas são idempotentes; se a segunda falhar, uma nova tentativa retoma o mesmo ID.

## Seções e categorias de fotos

1. Dados do equipamento: listar somente os equipamentos da empresa já vinculada ao relatório, selecionar um cadastrado e persistir seu `id_equipament`.
2. Compressor externo: fotos em `external_compressor`.
3. Compressor interno: fotos em `internal_compressor`.
4. Insumos: as sete respostas acima; fotos por item somente quando `Sim`.
5. Plaquetas: grupos `compressor_nameplate`, `dryer_nameplate`,
   `motor_nameplate`, `lubrication_nameplate`, `unit_nameplate`.

Para as fotos, reutilizar `REPORT_MEDIA` com `media_group VARCHAR(64) NULL` e validação de grupos no backend. O índice já existente em `report_reference_id` atende as consultas atuais; não há consulta por grupo no banco. `NULL`
preserva as fotos antigas de Ordem de Serviço; todo registro de foto do novo tipo
exige grupo. Uma foto pode ter nota, ID estável, tipo MIME e tamanho. As pastas do
bucket são prefixos de chave, por exemplo:

`clients/{clientId}/reports/{assessmentId}/needs-assessment/{mediaGroup}/{photoId}.jpg`

Limitar tamanho e formato, gerar URLs assinadas no backend e nunca colocar as
credenciais do bucket no app. Processar mais de 30 fotos em lotes, pois esse é o
limite atual do DTO de mídia por requisição. Ao trocar um insumo de `Sim` para
`Não`, solicitar confirmação antes de remover suas fotos locais; a exclusão
remota acontece na sincronização seguinte.

## Aplicativo e funcionamento offline

- Adicionar o cartão **Levantamento de necessidade** em Adicionar relatório e
  distinguir os tipos na lista, na navegação, na duplicação e na exclusão.
- Criar modelo e armazenamento locais próprios para o levantamento, usando IDs
  UUID gerados no aparelho. Reutilizar o fluxo visual de seleção de equipamento,
  salvando `id_equipament` no relatório. Ao criar o relatório, persistir
  `id_company` recebido do fluxo existente de seleção da empresa; não repetir
  essa seleção na tela de equipamento. A lista de equipamentos deve ser filtrada
  por `id_company`, inclusive no cache offline, e o equipamento selecionado deve
  pertencer a essa empresa. Usar o cadastro em cache para selecionar e exibir
  o equipamento offline. Definir uma preparação inicial de dados para quem
  abrir o app offline pela primeira vez.
- Salvar cada campo ao editar. Copiar fotos da câmera/galeria para o diretório
  privado do app, em `reports/{assessmentId}/{mediaGroup}/{photoId}.jpg`, e
  persistir metadados separados dos arquivos.
- Exibir uma galeria por grupo, com observações, remoção, estado de envio e
  visualização sem rede. Não guardar URL assinada como URI permanente.
- Ao baixar relatórios em outro aparelho, baixar cada arquivo ausente ou alterado
  uma única vez para o cache privado. Usar ID da mídia mais versão, checksum ou
  ETag para detectar alteração; reutilizar os arquivos já válidos nas próximas
  sincronizações. Retomar downloads interrompidos e mostrar progresso.
- Para não transmitir fotos desnecessariamente, separar atualização de metadados
  e downloads: a sincronização pode baixar apenas mídias novas/alteradas, em
  lotes com concorrência limitada. O PDF offline usa o arquivo local, não uma URL
  temporária. Se faltar arquivo após uma falha, indicar quais fotos ainda não
  estão disponíveis offline.

## API e sincronização

1. Estender `TypesReport`, DTOs, model, repository e service para criar/atualizar
   `NEEDS_ASSESSMENT` por `id_reference`, validando propriedade pelo `client_id`.
2. Expor o levantamento no contrato atual de `/v1/report/reference` ou em rotas
   específicas versionadas; manter o `report_id` e o `assessment_id` distintos.
3. Generalizar as rotas de mídia para aceitar o tipo do relatório e o grupo.
   `upload-urls` retorna chave e PUT assinado; `complete` confirma somente
   objetos existentes e persiste o manifesto; `GET` devolve metadados e URLs
   temporárias de leitura.
4. Adaptar `/v1/report/get-sync`: hoje usa `INNER JOIN ORDEM_SERVICE` e, assim,
   omite qualquer novo tipo. Paginar `REPORT` primeiro e buscar os detalhes por
   tipo, preservando total e ordem. Retornar `{ report, reference, media_manifest }`
   com IDs, grupos e versões das mídias; emitir URLs assinadas somente para os
   arquivos que o aparelho precisar baixar.
5. No app, sincronizar em ordem: registro `REPORT`, dados específicos, fotos
   pendentes por grupo, confirmação da mídia. Marcar `sync: true` somente após
   concluir tudo. Repetir com os mesmos IDs deve ser seguro após interrupção.
6. Na volta do servidor, mesclar por ID e versão; preservar alterações locais
   ainda não enviadas e sinalizar conflito quando o mesmo levantamento for
   editado em dois aparelhos. Adaptar exclusão em lote para remover a tabela
   específica, metadados e objetos do bucket.

## PDF

Criar `needsAssessmentTemplate` separado do modelo de Ordem de Serviço, mas
reutilizar sua composição visual: logo e título no cabeçalho, linha de
identificação, tabelas de equipamento com bordas, faixas azuis para seções e
anexos de fotos em duas colunas com legendas. Incluir a empresa já vinculada ao
relatório e dados do equipamento resolvidos por `id_equipament` (ou pelo cadastro
em cache quando estiver offline), fotos externas/internas, respostas dos sete
insumos (com suas fotos quando `Sim`) e as cinco categorias de plaquetas.
Paginar fotos com legenda/observação e renderizar a partir de arquivos locais,
para funcionar sem internet. Não incluir bloco de assinatura. Antes de gerar,
validar a presença dos arquivos necessários e mostrar erro específico se uma
imagem ainda não foi disponibilizada offline.

## Sequência de entrega

1. Migração SQL e contratos de API, inclusive tipo novo e grupos de mídia.
2. CRUD do levantamento no backend e sincronização de leitura para múltiplos tipos.
3. Armazenamento offline e formulários das cinco seções no app.
4. Upload/download incremental de fotos e exclusão por grupo.
5. Template PDF e integração na tela do levantamento.
6. Testes em dois emuladores: criar e fotografar offline no A; enviar; buscar no
   B; abrir fotos e gerar PDF offline; editar/remover em B; reenviar; confirmar
   atualização no A. Incluir interrupção/retry e mais de 30 fotos.

## Critérios de aceite

- Um levantamento completo pode ser criado, editado, fotografado e exportado em
  PDF sem rede no aparelho de origem.
- Após sincronizar, o segundo aparelho recebe respostas e fotos nas categorias
  corretas; depois de baixá-las uma vez, abre tudo e gera PDF sem internet.
- Sincronizações repetidas não duplicam registros ou uploads válidos.
- Fotos removidas somem do manifesto e do bucket após sincronização concluída.
- Relatórios antigos de Ordem de Serviço continuam visíveis e sincronizáveis.

## Estado da implementação (2026-10-07)

- Backend: modelo, validação de empresa/equipamento por cliente, leitura e escrita,
  paginação mista de relatórios, grupos de mídia, URLs assinadas e controle de
  versão para respostas e fotos implementados. A migração está em
  `migrations/20261007_needs_assessment.sql` (tabela) e
  `migrations/20261007_needs_assessment_media.sql` (coluna de grupo e precisão
  de `updated_at`). Cada arquivo contém uma única instrução SQL para execução
  separada no DBeaver; ambos precisam ser aplicados antes de sincronizar.
- Aplicativo: formulários, galerias por grupo, cópia local das fotos, cache de
  downloads, sincronização e PDF offline implementados. O PDF usa os mesmos
  campos cadastrados de equipamento apresentados na Ordem de Serviço e logo
  incorporado ao bundle, sem buscar ativos pela rede.
- Verificado em um emulador: criação, seleção do equipamento da empresa,
  resposta de insumo, captura de foto e PDF com a foto sem depender do bucket.
  O bundle Android e os testes unitários do backend passaram.
- Pendente de validação integrada: aplicar a migração, subir backend atualizado
  e testar envio/recebimento em dois emuladores, incluindo conflitos e
  remoções. A exclusão de um levantamento inteiro com fotos devolve 409 para
  evitar deixar objetos órfãos; a limpeza completa do prefixo do bucket requer
  autorização específica porque a revisão automática bloqueou essa operação
  destrutiva. A remoção de fotos individuais via sincronização continua ativa.
