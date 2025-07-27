# 1) Defina aqui as frases originais para cada grupo

$sentencesA = @(
  "O céu estrelado refletia na água calma do lago, criando um panorama sereno que acalmava a alma de quem contemplava a paisagem.",
  "Uma criança curiosa tocava as pétalas macias das rosas no jardim, enquanto pássaros cantavam alegremente ao amanhecer em perfeita harmonia.",
  "O trem apitou na estação antiga, anunciando a partida dos passageiros, que carregavam malas coloridas e esperanças renovadas para novas jornadas emocionantes.",
  "Nas montanhas cobertas de neve, alpinistas experientes ajustavam seus equipamentos e respiravam fundo antes de conquistar o cume gelado sob um céu azul intenso.",
  "Ao som das ondas quebrando na praia deserta, um pescador solitário puxava suas redes, esperando capturar peixes frescos para o almoço do dia."
)

$sentencesB = @(
  "Em uma manhã ensolarada, moradores do bairro se reuniram na praça central para celebrar a inauguração de um espaço cultural renovado. Crianças correram entre quiosques coloridos oferecendo livros, artesanato e música ao vivo, enquanto voluntários distribuíam lanches e sucos. A prefeita local discursou sobre a importância de promover a cultura na comunidade e incentivar o convívio social. Ao som de violão e risadas, o evento ganhou vida e aproximou vizinhos de diferentes idades e origens.",
  "A startup inovadora lançou uma plataforma online que conecta agricultores familiares a consumidores urbanos em busca de alimentos frescos e sustentáveis. Por meio de um aplicativo intuitivo, é possível acompanhar o cultivo, a colheita e o transporte dos produtos, garantindo transparência e rastreabilidade. Os produtores recebem feedback imediato sobre demandas e preços, enquanto os compradores apoiam a economia local e reduzem o desperdício de alimentos. A iniciativa combina tecnologia, agricultura e responsabilidade socioambiental durante todo o ano.",
  "Durante o semestre letivo, professores e alunos de diferentes disciplinas colaboraram em um projeto interativo de aprendizado baseado em Jogos Sérios. A proposta envolveu o desenvolvimento de protótipos digitais, testes de usabilidade e apresentação de resultados em feiras acadêmicas. Os estudantes adquiriram competências de programação, design e comunicação, enquanto os docentes avaliaram o impacto pedagógico dessas tecnologias no engajamento e na retenção de conteúdo. A experiência foi documentada em relatórios e artigos científicos para futuras pesquisas.",
  "Em hospitais públicos e privados, a telemedicina tornou-se uma ferramenta essencial para ampliar o acesso a consultas médicas em regiões remotas. Pacientes podem enviar registros de sintomas, exames laboratoriais e imagens por plataformas seguras, recebendo pareceres de especialistas em poucas horas. A prática reduz filas, otimiza recursos e minimiza riscos de contágio em períodos de epidemias. Além disso, treinamentos online para profissionais de saúde garantem atualização contínua sobre protocolos e melhores práticas clínicas, eficazes e seguras.",
  "Em áreas devastadas pelo desmatamento, projetos de reflorestamento comunitário mobilizam voluntários e instituições para restaurar ecossistemas. Mudas nativas são cultivadas em viveiros, distribuídas e plantadas em terrenos previamente preparados, respeitando características do solo e do clima. Durante meses, equipes monitoram o crescimento das plantas, registrando dados sobre taxa de sobrevivência e biodiversidade local. A iniciativa promove educação ambiental, gera emprego comunitário e contribui para a mitigação das mudanças climáticas em escala regional, durante vários anos."
)

$sentencesC = @(
  "Com o crescimento acelerado das cidades, tem-se observado um aumento significativo no congestionamento do trânsito urbano e na emissão de poluentes associados aos veículos. Para enfrentar esses desafios, diversas metrópoles estão investindo em sistemas de transporte público eficientes e sustentáveis, incluindo ônibus elétricos, trens metropolitanos e ciclovias integradas. Além disso, tecnologias de gestão do tráfego, como semáforos inteligentes e aplicativos de carona compartilhada, auxiliam na otimização das rotas e na redução do tempo de deslocamento. Pesquisas recentes indicam que a adoção de políticas de restrição de veículos em áreas centrais, combinada com incentivos ao uso de bicicletas e ao transporte coletivo, pode diminuir em até 30 % as emissões de carbono. A integração de dados em tempo real e a participação ativa da comunidade são fundamentais para o sucesso dessas iniciativas, promovendo mobilidade mais ágil e qualidade de vida.",
  "Nos últimos anos, a inteligência artificial (IA) tem ganhado espaço em diversas áreas do conhecimento, desde a medicina e transporte até a educação e entretenimento. Algoritmos de aprendizado profundo permitem o reconhecimento de padrões em grandes volumes de dados, auxiliando no diagnóstico precoce de doenças e na previsão de falhas em sistemas industriais. Em paralelo, modelos generativos, como redes adversárias (GANs) e transformadores, são capazes de criar imagens, textos e músicas com qualidade impressionante. Apesar dos avanços, ainda existem desafios relacionados à interpretabilidade, segurança e viés algorítmico, que podem comprometer a ética e a transparência das aplicações. Pesquisadores buscam desenvolver frameworks regulatórios e metodologias de auditoria para garantir o uso responsável da IA, equilibrando inovação e proteção dos direitos humanos.",
  "A economia circular propõe um modelo de produção e consumo baseado na redução, reutilização e reciclagem de recursos, visando minimizar o desperdício e prolongar o ciclo de vida dos produtos. Iniciativas de upcycling transformam resíduos industriais e materiais descartados em novos itens de alto valor, enquanto programas de logística reversa incentivam consumidores a devolver embalagens e equipamentos usados. Empresas de diversos setores implementam plataformas digitais para rastrear componentes ao longo da cadeia de suprimentos, garantindo transparência e otimizando a recuperação de materiais. Estudos de caso demonstram que práticas circulares podem gerar economia de custo de até 20 % e reduzir drasticamente as emissões de carbono. Políticas públicas e incentivos fiscais desempenham papel crucial para estimular a adoção em larga escala, promovendo inovação e sustentabilidade.",
  "A promoção da saúde mental tem se tornado uma prioridade em políticas de saúde pública, especialmente em virtude dos impactos psicológicos resultantes de crises econômicas, pandemias e mudanças climáticas. Centros de acolhimento e linhas de apoio oferecem suporte remoto e presencial, combinando terapia cognitivo‑comportamental e grupos de apoio peer‑to‑peer. Tecnologias digitais, como aplicativos de meditação guiada e chatbots terapêuticos, auxiliam no monitoramento de humor e na identificação precoce de transtornos. Programas de prevenção em escolas e ambientes de trabalho visam reduzir o estigma e ensinar estratégias de enfrentamento. Pesquisas indicam que abordagens integradas, que combinam exercícios físicos, terapia e suporte social, resultam em melhora significativa no bem‑estar e na redução de sintomas de ansiedade e depressão.",
  "Nos ambientes de educação a distância, a interação entre estudantes e professores depende de plataformas virtuais que oferecem aulas gravadas, fóruns de discussão e ferramentas de avaliação online. A eficácia desse formato é influenciada pela usabilidade da interface, qualidade dos materiais didáticos e engajamento dos alunos. Estudos mostram que a inclusão de recursos multimídia, como vídeos interativos, quizzes e simulações, aumenta a retenção de conteúdo e a motivação. Além disso, sistemas de aprendizagem adaptativa utilizam algoritmos para personalizar o ritmo de estudo, identificando áreas de dificuldade e sugerindo atividades complementares. Desafios comuns incluem a necessidade de conectividade estável, autonomia do estudante e capacitação docente em metodologias virtuais. Políticas educacionais e investimentos em infraestrutura digital são essenciais para democratizar o acesso e garantir a continuidade da aprendizagem."
)

# 2) Defina os 3 grupos de referências com seus paths dentro do container
$groups = @(
  @{ Key = 'A'; Sentences = $sentencesA; Files = @(
        "/refs/thomaz_a1.wav","/refs/thomaz_a2.wav",
        "/refs/thomaz_a3.wav","/refs/thomaz_a4.wav",
        "/refs/thomaz_a5.wav"
    )
  },
  @{ Key = 'B'; Sentences = $sentencesB; Files = @(
        "/refs/thomaz_b1.wav","/refs/thomaz_b2.wav",
        "/refs/thomaz_b3.wav","/refs/thomaz_b4.wav",
        "/refs/thomaz_b5.wav"
    )
  },
  @{ Key = 'C'; Sentences = $sentencesC; Files = @(
        "/refs/thomaz_c1.wav","/refs/thomaz_c2.wav",
        "/refs/thomaz_c3.wav","/refs/thomaz_c4.wav",
        "/refs/thomaz_c5.wav"
    )
  }
)

# 3) Loop principal: para cada grupo e cada sentença, gera um WAV,
#    mas o nome do arquivo de saída usa apenas o índice

foreach ($group in $groups) {
  $tag       = $group.Key
  $sentences = $group.Sentences
  $files     = $group.Files

  for ($i = 0; $i -lt $sentences.Count; $i++) {
    $index   = $i + 1
    $sent    = $sentences[$i]
    $outFile = "/output/xtts_${tag}${index}.wav"

    Write-Host "[$tag$index] Gerando: $outFile"

    docker run --rm -it `
      --gpus all `
      -e TTS_HOME=/root/.cache/tts `
      -v "E:/coqui tts cache:/root/.cache/tts" `
      -v "E:/tts_output:/output" `
      -v "E:/tts_refs:/refs" `
      ghcr.io/coqui-ai/tts:latest `
        --model_name tts_models/multilingual/multi-dataset/xtts_v2 `
        --speaker_wav $($files -join ' ') `
        --language_idx pt `
        --text "$sent" `
        --out_path "$outFile"
  }
}
