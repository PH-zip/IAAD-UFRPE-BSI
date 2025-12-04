🏥 Sistema de Gestão de Consultas Médicas

Este repositório documenta a implementação do banco de dados ConsultasMedicas utilizando o modelo NoSQL orientado a documentos, contrastando com a implementação relacional em MySQL.

📋 Sobre o Projeto

O objetivo é simular o mesmo sistema de consultas médicas, focando agora nas diferenças de arquitetura e na flexibilidade que o modelo de documentos oferece em comparação com o modelo relacional rígido.
🚀 Tecnologias Utilizadas
Categoria	Tecnologia	Uso no Projeto
Banco NoSQL	MongoDB 6.0+	Armazenamento de dados no formato BSON/JSON.
Interface	MongoDB Compass	Ferramenta gráfica para gestão, CRUD e Aggregation Framework.
Linguagem	JSON	Formato dos documentos e scripts de carga.

🎯 Como Começar - GUIA RÁPIDO (MongoDB)

Para carregar o banco de dados MongoDB, você utilizará o utilitário de linha de comando mongoimport ou a interface gráfica do Compass.

1️⃣ Importar os Arquivos JSON

Navegue até o diretório onde você salvou os arquivos .json exportados e use o terminal para carregar cada coleção.
Bash

# Exemplo para a coleção pacientes
mongoimport --db ConsultasMedicas --collection pacientes --file ConsultasMedicas.Pacientes.json --jsonArray
Repita o comando para as coleções medicos, consultas e clinicas.

2️⃣ Verificar os Dados

Abra o MongoDB Compass, conecte-se ao seu servidor local e selecione o banco de dados ConsultasMedicas. Verifique se as quatro coleções estão listadas e contêm documentos.


3️⃣ Testar as Operações

Utilize a interface do Compass para realizar as operações CRUD e as consultas avançadas.
📁 Estrutura dos Arquivos (NoSQL)

O código-fonte no GitHub para a parte NoSQL foca nos scripts de carga e na documentação do modelo.
Pasta/Arquivo	Descrição
scripts/	Contém os arquivos .json de todas as coleções (medicos.json, pacientes.json, etc.) para a carga inicial.
documentacao/	Inclui o diagrama conceitual do modelo de referência e as instruções de importação.
comandos_mongodb.txt	Script com os comandos CRUD e de Agregação utilizados na apresentação.

⚙️ Parte 2: Análise e Implementação MongoDB

Nesta seção, o foco é a análise comparativa e a implementação das estruturas no modelo orientado a documentos.

🗄️ Estrutura do Banco de Dados (Documentos)

O banco ConsultasMedicas é composto pelas seguintes Coleções (equivalentes às Tabelas do MySQL):

    clinicas: Informações sobre as unidades.

    medico: Dados dos profissionais.

    paciente: Informações pessoais dos pacientes.

    consulta: Agendamentos. Este documento utiliza a estratégia de Referência, contendo apenas os IDs do médico e do paciente.

    log_auditoria (Conceitual): No MongoDB, o log é geralmente implementado com uma coleção separada ou embutido como um array de logs dentro do próprio documento principal (Ex: no documento consulta).

📊 Estatísticas do Dataset (Baseado nos Arquivos JSON)

O banco de dados do MongoDB está populado com os mesmos dados da Atividade 1, garantindo um volume suficiente para a demonstração do CRUD:
Coleção	Contagem (Aproximada)
Pacientes	4 documentos
Médicos	5 documentos
Clínicas	2 documentos
Consultas	7 documentos
Total	18 documentos
🛠️ Diferenciais e Pontos de Análise

    CRUD completo: As operações são realizadas diretamente nos documentos JSON via Compass.

    Controle de Integridade (Diferencial!): No MongoDB, não há Chaves Estrangeiras (FKs) ou deleção em cascata nativa. A responsabilidade pela integridade referencial (impedir a exclusão de um paciente que tem consultas) é transferida para a aplicação (o código Python/Streamlit).

    Triggers (Diferencial!): O MongoDB não suporta triggers. A funcionalidade de auditoria (registro de logs) deve ser implementada na camada da aplicação ou através de Change Streams (monitoramento de alterações), e não pelo banco de dados.

    Consultas Avançadas: Consultas complexas (JOINs, GROUP BY) são realizadas utilizando o Aggregation Framework (operadores como $lookup e $group), não o SQL.
